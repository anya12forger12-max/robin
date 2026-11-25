"""Regressions for onion URL validation and Tor-only scraping."""

from unittest.mock import MagicMock, patch

import pytest

from scrape import scrape_single
from url_safety import extract_onion_link, is_safe_onion_url


def test_userinfo_confusion_is_rejected():
    assert is_safe_onion_url('http://abc.onion@169.254.169.254/latest/meta-data/') is False
    assert is_safe_onion_url('http://abc.onion@127.0.0.1:8501/') is False
    assert is_safe_onion_url('http://abc.onion:8000/path') is True


def test_extract_onion_link_rejects_clearweb_and_bad_schemes():
    assert extract_onion_link('https://example.onion/a?b=1') == 'https://example.onion/a?b=1'
    assert extract_onion_link('http://abc.onion@internal.example/') is None
    assert extract_onion_link('file:///etc/passwd') is None
    assert extract_onion_link('http://127.0.0.1:5000/') is None


def test_scrape_single_never_uses_direct_session_for_userinfo_url():
    with patch('scrape._get_session') as get_session:
        result = scrape_single({
            'link': 'http://abc.onion@169.254.169.254/latest/meta-data/',
            'title': 'credentials dump',
        })
    get_session.assert_not_called()
    assert result == (
        'http://abc.onion@169.254.169.254/latest/meta-data/',
        'credentials dump',
    )


def test_scrape_single_rejects_clearnet_redirect():
    redirect = MagicMock(status_code=302, headers={'Location': 'http://169.254.169.254/latest/'})
    session = MagicMock()
    session.get.return_value = redirect
    with patch('scrape._get_session', return_value=session):
        result = scrape_single({'link': 'http://example.onion/page', 'title': 'leak'})
    assert result == ('http://example.onion/page', 'leak')
    session.get.assert_called_once()
    assert session.get.call_args.kwargs['allow_redirects'] is False


def test_scrape_single_follows_onion_redirect_through_tor():
    redirect = MagicMock(status_code=302, headers={'Location': 'http://other.onion/next'})
    ok = MagicMock(status_code=200, headers={'Content-Type': 'text/html'}, encoding='utf-8')
    ok.iter_content.return_value = [b'<html><body>hello</body></html>']
    session = MagicMock()
    session.get.side_effect = [redirect, ok]
    with patch('scrape._get_session', return_value=session):
        result = scrape_single({'link': 'http://example.onion/page', 'title': 'doc'})
    assert 'hello' in result[1]
    assert session.get.call_count == 2
