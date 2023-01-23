#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import Dict, Any

import pytest
from dom_toml.parser import BadConfigError

from sphinx_pyproject_poetry import ProjectParser, SphinxConfig


class TestSphinxConfig:
    def test_normal(self: TestSphinxConfig) -> None:
        config: SphinxConfig = SphinxConfig(
            pyproject_file="pyproject.toml", globalns=globals()
        )
        freedom: Dict[str, Any] = {
            "copyright": "2023, Tetsutaro Maruyama",
            "extensions": [
                "sphinx.ext.autodoc",
                "sphinx.ext.napoleon",
                "sphinx.ext.linkcode",
                "sphinx.ext.githubpages",
                "sphinx_rtd_theme",
            ],
            "templates_path": ["_templates"],
            "exclude_patterns": [],
            "language": "ja",
            "html_theme": "sphinx_rtd_theme",
            "html_static_path": ["_static"],
            "github_username": "tetutaro",
        }
        assert config.name == "sphinx-pyproject-poetry"
        assert len(config) == len(freedom)
        for key, value in freedom.items():
            assert config[key] == value
        for key, value in config.items():
            assert freedom[key] == value
        return

    def test_raises(self: TestSphinxConfig) -> None:
        with pytest.raises(BadConfigError):
            _ = SphinxConfig(pyproject_file="tests/tomls/empty.toml")
        with pytest.raises(BadConfigError):
            _ = SphinxConfig(pyproject_file="tests/tomls/noname.toml")
        return


class TestProjectParser:
    def test_parse_name(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "name": "test_name",
        }
        parser: ProjectParser = ProjectParser()
        name: str = parser.parse_name(config=config)
        assert name == "test-name"
        return

    def test_parse_version(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "version": 123,
        }
        parser: ProjectParser = ProjectParser()
        version: str = parser.parse_version(config=config)
        assert version == "123"
        return

    def test_parse_description(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "description": "test description",
        }
        parser: ProjectParser = ProjectParser()
        description: str = parser.parse_description(config=config)
        assert description == "test description"
        return

    def test_parse_author(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "author": [
                "1st author <1st.author@domain>",
                " 2nd author <2nd.author@domain> ",
                " 3rd author ",
            ],
        }
        parser: ProjectParser = ProjectParser()
        author: str = parser.parse_author(config=config)
        assert author == "1st author, 2nd author and 3rd author"
        return

    def test_parse_author_comma(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "author": ["1st,author"],
        }
        parser: ProjectParser = ProjectParser()
        with pytest.raises(BadConfigError):
            _ = parser.parse_author(config=config)
        return

    def test_parse_author_empty(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "author": [],
        }
        parser: ProjectParser = ProjectParser()
        with pytest.raises(BadConfigError):
            _ = parser.parse_author(config=config)
        return

    def test_parse(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "authors": ["1st author"],
            "maintainers": ["2nd author"],
        }
        parser: ProjectParser = ProjectParser()
        parsed: Dict[str, Any] = parser.parse(config=config)
        assert parsed["author"] == "1st author and 2nd author"
        return

    def test_parse2(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "authors": [],
            "maintainers": ["2nd author"],
        }
        parser: ProjectParser = ProjectParser()
        parsed: Dict[str, Any] = parser.parse(config=config)
        assert parsed["author"] == "2nd author"
        return

    def test_parse3(self: TestProjectParser) -> None:
        config: Dict[str, Any] = {
            "maintainers": ["2nd author"],
        }
        parser: ProjectParser = ProjectParser()
        with pytest.raises(BadConfigError):
            _ = parser.parse(config=config)
        return
