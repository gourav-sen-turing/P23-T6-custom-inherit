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


# Regex pattern to match parameter/attribute items
# Matches: parameter_name followed by optional content (type annotation, description)
# The pattern captures:
# - Group 1: parameter name (at start of line, word characters)
# - Group 2: everything after the parameter name until the next parameter or end
_RE_PATTERN_ITEMS = re.compile(
    r'^(\w+)((?:.*(?:\n(?:[ \t]+.*))*)?)',
    re.MULTILINE
)

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
    for section_name in SECTION_NAMES:
        if section_name in doc_sections and doc_sections[section_name]:
            # Extract the section content
            section_content = doc_sections[section_name]

            # Remove common leading whitespace (for Google style)
            lines = section_content.splitlines()
            if lines:
                # Find minimum indentation
                min_indent = float('inf')
                for line in lines:
                    if line.strip():  # Skip empty lines
                        indent_len = len(line) - len(line.lstrip())
                        min_indent = min(min_indent, indent_len)

                # Remove the common indentation
                if min_indent < float('inf') and min_indent > 0:
                    dedented_lines = []
                    for line in lines:
                        if line.strip():
                            dedented_lines.append(line[min_indent:])
                        else:
                            dedented_lines.append(line)
                    section_content = '\n'.join(dedented_lines)

            # Parse items using the regex
            items = OrderedDict()
            matches = _RE_PATTERN_ITEMS.findall(section_content)

            for name, content in matches:
                items[name] = content

            # Replace the string content with the parsed OrderedDict
            doc_sections[section_name] = items


def merge(prnt_sec, child_sec, merge_within_sections, style):
    """Merge the doc-sections of the parent's and child's attribute with items.

    Parameters
    ----------
    prnt_sec: OrderedDict[str, str]
    child_sec: OrderedDict[str, str]
    merge_within_sections: bool
        Whether to merge the items.
    style: str
        The doc style.

    Returns
    -------
    str
        The merged items rendered as a string.
    """
    if not merge_within_sections:
        # If not merging, use child if it exists, otherwise parent
        if child_sec:
            return _render(child_sec, style)
        elif prnt_sec:
            return _render(prnt_sec, style)
        else:
            return ""

    # Merge the items: start with parent items, then add/override with child items
    merged_items = OrderedDict()

    # Add parent items first
    if prnt_sec:
        for key, value in prnt_sec.items():
            merged_items[key] = value

    # Add/override with child items
    if child_sec:
        for key, value in child_sec.items():
            merged_items[key] = value

    # Render the merged items
    return _render(merged_items, style)
