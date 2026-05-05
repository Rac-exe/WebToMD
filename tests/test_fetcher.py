"""Tests for the fetch layer and fallback chain."""

import pytest


def test_is_valid_url_accepts_http():
    from webtomd.utils import is_valid_url
    assert is_valid_url("https://example.com") is True


def test_is_valid_url_rejects_bare_string():
    from webtomd.utils import is_valid_url
    assert is_valid_url("not-a-url") is False


def test_is_sparse_with_none():
    from webtomd.utils import is_sparse
    assert is_sparse(None) is True


def test_is_sparse_with_short_content():
    from webtomd.utils import is_sparse
    assert is_sparse("hi") is True


def test_is_sparse_with_real_content():
    from webtomd.utils import is_sparse
    assert is_sparse("a" * 300) is False


def test_url_to_filename():
    from webtomd.utils import url_to_filename
    assert url_to_filename("https://stripe.com/docs/api") == "stripe-com-docs-api"
