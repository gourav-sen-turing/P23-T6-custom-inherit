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
# - Group 1: parameter name (sequence of word characters at start of line)
# - Group 2: everything after the parameter name until the next parameter or end of string
_RE_PATTERN_ITEMS = re.compile(
    r'^(\w+)'  # Parameter name at start of line
    r'('       # Start capturing the rest
    r'[^\n]*'  # Rest of the first line (type annotation if any)
    r'(?:\n(?!\w)[^\n]*)*'  # Subsequent indented lines (description)
    r')',      # End capturing
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
        The document sections dictionary where items sections will be parsed
        into OrderedDict format in place.
    """
    for section_name in SECTION_NAMES:
        if section_name in doc_sections and doc_sections[section_name]:
            content = doc_sections[section_name]

            # For Google style, parameters are indented, so we need to dedent
            # Check if all lines start with the same indentation
            lines = content.splitlines()
            if lines:
                # Get the indentation of the first non-empty line
                indent_len = 0
                for line in lines:
                    if line.strip():
                        indent_len = len(line) - len(line.lstrip())
                        break

                # Remove common indentation
                if indent_len > 0:
                    dedented_lines = []
                    for line in lines:
                        if line.strip():  # non-empty line
                            dedented_lines.append(line[indent_len:])
                        else:  # empty line
                            dedented_lines.append(line)
                    content = '\n'.join(dedented_lines)

            # Parse the section content into individual items
            items = OrderedDict()
            matches = _RE_PATTERN_ITEMS.findall(content)
            for name, content in matches:
                items[name] = content
            # Replace the string content with the parsed OrderedDict
            doc_sections[section_name] = items


def merge(prnt_sec, child_sec, merge_within_sections, style):
    """Merge the doc-sections of the parent's and child's attribute with items.

    Parameters
    ----------
    prnt_sec: OrderedDict[str, str]
        Parent's section items.
    child_sec: OrderedDict[str, str]
        Child's section items.
    merge_within_sections: bool
        Whether to merge the items from parent and child.
    style: str
        The doc style ('numpy' or 'google').

    Returns
    -------
    str
        The rendered merged section content.
    """
    if not isinstance(prnt_sec, OrderedDict):
        prnt_sec = OrderedDict()
    if not isinstance(child_sec, OrderedDict):
        child_sec = OrderedDict()

    if merge_within_sections:
        # Merge parent and child items, with child items taking precedence
        merged_items = OrderedDict()
        # First add all parent items
        for key, value in prnt_sec.items():
            merged_items[key] = value
        # Then add/override with child items
        for key, value in child_sec.items():
            merged_items[key] = value
        return _render(merged_items, style)
    else:
        # Use child section if it exists, otherwise use parent
        if child_sec:
            return _render(child_sec, style)
        elif prnt_sec:
            return _render(prnt_sec, style)
        else:
            return ""
