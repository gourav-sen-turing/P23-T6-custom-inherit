"""This module handles sections with items."""

from collections import OrderedDict
import inspect
import re

try:
    from textwrap import indent
except ImportError:
    # for Python < 3.3
    def indent(text, padding):
        return ''.join(padding+line for line in text.splitlines(True))


_RE_PATTERN_ITEMS = None

_STYLE_TO_PADDING = {
    "numpy": "",
    "google": " " * 4,
}

SECTION_NAMES = ("Attributes", "Parameters")


def _render(body, style):
    """Render the items of a section.

    Parameters
    ----------
    body: OrderedDict[str, Optional[str]]
        The items of a section.
    style: str
        The doc style.

    Returns
    -------
    str
    """
    padding = _STYLE_TO_PADDING[style]
    section = []
    for key, value in body.items():
        section += [indent("{}{}".format(key, value), padding)]
    return "\n".join(section)


def set_defaults(doc_sections):
    """Set the defaults for the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    for section_name in SECTION_NAMES:
        doc_sections[section_name] = OrderedDict()


def parse(doc_sections):
    """Parse the sections with items in place.

    Parameters
    ----------
    doc_sections: OrderedDict[str, Optional[str]]
    """
    pass


def merge(prnt_sec, child_sec, merge_within_sections, style):
    """Merge the doc-sections of the parent's and child's attribute with items.

    Parameters
    ----------
    prnt_sec: OrderedDict[str, str]
    child_sec: OrderedDict[str, str]
    merge_within_sections: bool
        Wheter to merge the items.
    style: str
        The doc style.

    Returns
    -------
    OrderedDict[str, str]
        The merged items.
    """
    return ""
