#!/usr/bin/env python3 -m pytest
from os import environ

from plextraktsync.factory import factory


def test_config_merge():
    config = factory.config()

    override = {
        "root": {
            "key1": "value1"
        }
    }
    config.merge(override, config)
    override = {
        "root": {
            "key2": "value2"
        }
    }
    config.merge(override, config)
    assert config["root"]["key1"] == "value1"
    assert config["root"]["key2"] == "value2"


def test_config():
    config = factory.config()

    config.save()
    config.initialized = False
    assert config["PLEX_TOKEN"] is None

    config.save()
    assert config["PLEX_TOKEN"] is None

    environ["PLEX_TOKEN"] = "Foo"
    config.initialized = False
    assert config["PLEX_TOKEN"] == "Foo"

    try:
        del environ["PLEX_TOKEN"]
    except KeyError:
        pass
    config.initialized = False
    assert config["PLEX_TOKEN"] is None

    environ["PLEX_TOKEN"] = "-"
    config.initialized = False
    assert config["PLEX_TOKEN"] is None

    environ["PLEX_TOKEN"] = "None"
    config.initialized = False
    assert config["PLEX_TOKEN"] is None
