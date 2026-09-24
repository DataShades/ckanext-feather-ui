import os

from ckanext.theming.lib import Theme

here = os.path.dirname(__file__)

# Common icon name -> Heroicons icon rendered through @iconify/tailwind4. The full
# class name has to be spelled out here so the Tailwind build (which scans this
# file) generates the matching CSS. Only icons used by the theme are listed;
# `icon_catalog.py` holds ready-made entries for the rest. Names missing from
# the map fall back to the emoji provided by the parent `bare` theme.
icon_map = {
    "arrow-right": "icon-[heroicons--arrow-right]",
    "book": "icon-[heroicons--book-open]",
    "building": "icon-[heroicons--building-office-2]",
    "chart-pie": "icon-[heroicons--chart-pie]",
    "chevron-down": "icon-[heroicons--chevron-down]",
    "clock": "icon-[heroicons--clock]",
    "cog": "icon-[heroicons--cog-6-tooth]",
    "dashboard": "icon-[heroicons--squares-2x2]",
    "database": "icon-[heroicons--circle-stack]",
    "edit": "icon-[heroicons--pencil]",
    "envelope": "icon-[heroicons--envelope]",
    "eye": "icon-[heroicons--eye]",
    "file": "icon-[heroicons--document]",
    "folder": "icon-[heroicons--folder]",
    "folder-open": "icon-[heroicons--folder-open]",
    "github": "icon-github",
    "globe": "icon-[heroicons--globe-alt]",
    "info-circle": "icon-[heroicons--information-circle]",
    "linkedin": "icon-linkedin",
    "lock": "icon-[heroicons--lock-closed]",
    "lock-open": "icon-[heroicons--lock-open]",
    "plus": "icon-[heroicons--plus]",
    "question-circle": "icon-[heroicons--question-mark-circle]",
    "search": "icon-[heroicons--magnifying-glass]",
    "sign-out": "icon-[heroicons--arrow-right-start-on-rectangle]",
    "sliders": "icon-[heroicons--adjustments-horizontal]",
    "table": "icon-[heroicons--table-cells]",
    "times": "icon-[heroicons--x-mark]",
    "user": "icon-[heroicons--user]",
    "users": "icon-[heroicons--users]",
    "youtube": "icon-youtube",
}


def make_theme(name: str = "feather", parent: str = "bare"):
    """Create the Feather theme.

    Client themes usually extend it::

        Theme("acme", acme_root, parent="feather")

    and override only what differs: CSS variables, a few macros, a template.
    """
    return Theme(name, here, parent=parent, icon_map=icon_map)
