"""Tests for config loading and merging."""

import pytest


def test_config_loads_defaults():
    from webtomd.config import Config
    c = Config()
    assert c.copy is False
    assert c.silent is False
    assert c.metadata is False


def test_config_merge_cli_wins():
    from webtomd.config import Config, merge
    c = Config(copy=False)
    merged = merge(c, copy=True)
    assert merged.copy is True
