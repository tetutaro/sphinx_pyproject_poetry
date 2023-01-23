#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Move some of your Sphinx configuration into pyproject.toml created by poetry.
"""
# stdlib
from __future__ import annotations
from typing import Any, Dict, Iterator, List, Mapping, MutableMapping, Optional
import re

# 3rd party
import dom_toml
from dom_toml.decoder import TomlPureDecoder
from dom_toml.parser import TOML_TYPES, AbstractConfigParser, BadConfigError
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from domdf_python_tools.words import word_join

__version__ = "0.1.0"  # Automatically updated by poetry-dynamic-versioning
__all__ = ["SphinxConfig"]


class SphinxConfig(Mapping[str, Any]):
    """Read the Sphinx configuration from pyproject.toml created by poetry.

    :param pyproject_file: The path to the ``pyproject.toml`` file.
    :param globalns: The global namespace of the ``conf.py`` file.
            The variables parsed from the ``[tool.sphinx-pyproject]``
            table will be added to this namespace.
            By default, or if explicitly :py:obj:`None`, this does not happen.
    :no-default globalns:

    """

    name: str
    """The value of the `tool.poetry.name <name>` key.

    Underscores are replaced by dashes but :pep:`508` normalization
    is *not* applied.

    The recommendation is to assign this to the
    project valiable in ``conf.py``:

    .. code-block:: python

        from sphinx_pyproject_poetry import SphinxConfig

        config = SphinxConfig()
        project = config.name
    """

    version: str
    """The value of the `tool.poetry.version <version>` key.

    Converted to a string if the value was a number
    in the ``pyproject.toml`` file.
    """

    description: str
    """The value of the `tool.poetry.description <description>` key.
    """

    author: str
    """A string giving the names of the authors.

    This is parsed from the `tool.poetry.authors <authors>` key,
    or the `tool.poetry.maintainers <maintainers>` key as a fallback.

    The names are joined together, e.g.:

    .. code-block:: TOML

        # pyproject.toml

        [tool.poetry]
        authors = ["1st Author <1st_author@domain>", "2nd Author"]

    .. code-block:: python

        >>> SphinxConfig("pyproject.toml").author
        '1st Author, 2nd Author'
    """

    def __init__(
        self: SphinxConfig,
        pyproject_file: PathLike = "pyproject.toml",
        *,
        globalns: Optional[MutableMapping] = None,
    ):
        pyproject_file = PathPlus(pyproject_file).abspath()
        config = dom_toml.load(pyproject_file, decoder=TomlPureDecoder)
        tool_poetry = config.get("tool", {}).get("poetry", {})
        if len(tool_poetry) == 0:
            raise BadConfigError(
                f"No 'tool.poetry' table found in {pyproject_file.as_posix()}"
            )
        pep621_config = ProjectParser().parse(tool_poetry)
        for key in ("name", "version", "description"):
            if key not in pep621_config:
                raise BadConfigError(
                    f"Either {key!r} was not declared "
                    "in the 'tool.poetry' table "
                    "or it was marked as 'dynamic', "
                    "which is unsupported by 'sphinx-pyproject-poetry'."
                )
        self.name = pep621_config["name"]
        self.version = pep621_config["version"]
        self.description = pep621_config["description"]
        self.author = pep621_config["author"]
        self._freeform = config.get("tool", {}).get("sphinx-pyproject", {})
        if globalns is not None:
            globalns.update(pep621_config)
            globalns.update(self._freeform)
        return

    def __getitem__(self, item) -> Any:
        """Returns the value of the given key
        in the  ``tool.sphinx-pyproject`` table.

        :param item:
        """
        return self._freeform[item]

    def __len__(self) -> int:
        """Returns the number of keys
        in the ``tool.sphinx-pyproject`` table.
        """
        return len(self._freeform)

    def __iter__(self) -> Iterator[str]:
        """Returns an iterator over the keys
        in the ``tool.sphinx-pyproject`` table.

        :rtype:

        .. latex:clearpage::
        """
        yield from self._freeform


class ProjectParser(AbstractConfigParser):
    """Parser for :pep:`621` metadata from ``pyproject.toml``."""

    def parse_name(self, config: Dict[str, TOML_TYPES]) -> str:
        """Parse the :pep621:`name` key.

        :param config: The unparsed TOML config for the ``[tool.poetry]`` table
        """
        name = config["name"]
        self.assert_type(name, str, ["tool", "poetry", "name"])
        return str(name).replace("_", "-")

    def parse_version(
        self: ProjectParser, config: Dict[str, TOML_TYPES]
    ) -> str:
        """Parse the :pep621:`version` key.

        :param config: The unparsed TOML config for the ``[tool.poetry]`` table
        """
        version = config["version"]
        self.assert_type(version, (str, int), ["tool", "poetry", "version"])
        return str(version)

    def parse_description(self, config: Dict[str, TOML_TYPES]) -> str:
        """Parse the :pep621:`description` key.

        :param config: The unparsed TOML config for the ``[tool.poetry]`` table
        """
        description = config["description"]
        self.assert_type(description, str, ["tool", "poetry", "description"])
        return description

    @staticmethod
    def parse_author(config: Dict[str, TOML_TYPES]) -> str:
        """Parse the :pep621:`authors/maintainers` key.

        :param config: The unparsed TOML config for the ``[tool.poetry]`` table
        """
        all_authors: List[str] = list()
        for idx, author in enumerate(config["author"]):
            match = re.match(r"(.*?)<(.*)>", author)
            if match is not None:
                name = match.groups()[0].strip()
            else:
                name = author.strip()
            if "," in name:
                raise BadConfigError(
                    f"The 'tool.poetry.authors[{idx}].name' key "
                    "cannot contain commas."
                )
            if len(name) > 0 and name not in all_authors:
                all_authors.append(name)
        if len(all_authors) == 0:
            raise BadConfigError(
                "The 'tool.poetry.authors' key cannot be empty."
            )
        return word_join(all_authors)  # type: ignore

    @property
    def keys(self: ProjectParser) -> List[str]:
        """The keys to parse from the TOML file."""
        return [
            "name",
            "version",
            "description",
            "author",
        ]

    def parse(
        self: ProjectParser,
        config: Dict[str, TOML_TYPES],
        set_defaults: bool = False,
    ) -> Dict[str, TOML_TYPES]:
        """Parse the TOML configuration.

        :param config:
        :param set_defaults: Has no effect in this class.
        """
        try:
            config["author"] = config.pop("authors")
        except KeyError:
            raise BadConfigError(
                "'authors' was not declared "
                "in the 'tool.poetry' table, "
                "which is unsupported by 'sphinx-pyproject-poetry'."
            )
        if "maintainers" in config:
            config["author"].extend(config.pop("maintainers"))
        return super().parse(config)
