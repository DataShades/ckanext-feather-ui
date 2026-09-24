import os

from ckanext.theming.lib import Theme

here = os.path.dirname(__file__)

# Common icon name -> Lucide icon rendered through @iconify/tailwind4. The full
# class name has to be spelled out here so the Tailwind build (which scans this
# file) generates the matching CSS. Only icons used by the theme are listed;
# `icon_catalogue.py` holds ready-made entries for the rest. Names missing from
# the map fall back to the emoji provided by the parent `bare` theme.
icon_map = {
    "building": "icon-[lucide--building-2]",
    "chevron-down": "icon-[lucide--chevron-down]",
    "clock": "icon-[lucide--clock]",
    "edit": "icon-[lucide--pencil]",
    "eye": "icon-[lucide--eye]",
    "file": "icon-[lucide--file]",
    "globe": "icon-[lucide--globe]",
    "plus": "icon-[lucide--plus]",
    "search": "icon-[lucide--search]",
    "times": "icon-[lucide--x]",
}


def make_theme(name: str = "feather", parent: str = "bare"):
    """Create the Feather theme.

    Client themes usually extend it::

        Theme("acme", acme_root, parent="feather")

    and override only what differs: CSS variables, a few macros, a template.
    """
    return Theme(name, here, parent=parent, icon_map=icon_map)
