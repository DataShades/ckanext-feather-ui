import os

from ckanext.theming.lib import Theme

here = os.path.dirname(__file__)

# Common icon name -> Lucide icon rendered through @iconify/tailwind4. The
# full class name has to be spelled out here so the Tailwind build (which
# scans this file) generates the matching CSS. Icons missing from the map fall
# back to the emoji provided by the parent `bare` theme.
icon_map = {
    "add": "icon-[lucide--plus]",
    "arrow-left": "icon-[lucide--arrow-left]",
    "arrow-right": "icon-[lucide--arrow-right]",
    "bars": "icon-[lucide--menu]",
    "bell": "icon-[lucide--bell]",
    "book": "icon-[lucide--book-open]",
    "building": "icon-[lucide--building-2]",
    "calendar": "icon-[lucide--calendar]",
    "chart-bar": "icon-[lucide--chart-column]",
    "check": "icon-[lucide--check]",
    "check-circle": "icon-[lucide--circle-check]",
    "chevron-down": "icon-[lucide--chevron-down]",
    "chevron-left": "icon-[lucide--chevron-left]",
    "chevron-right": "icon-[lucide--chevron-right]",
    "chevron-up": "icon-[lucide--chevron-up]",
    "clock": "icon-[lucide--clock]",
    "cog": "icon-[lucide--settings]",
    "copy": "icon-[lucide--copy]",
    "database": "icon-[lucide--database]",
    "download": "icon-[lucide--download]",
    "edit": "icon-[lucide--pencil]",
    "envelope": "icon-[lucide--mail]",
    "exclamation-triangle": "icon-[lucide--triangle-alert]",
    "external-link": "icon-[lucide--external-link]",
    "eye": "icon-[lucide--eye]",
    "file": "icon-[lucide--file]",
    "filter": "icon-[lucide--list-filter]",
    "folder": "icon-[lucide--folder]",
    "globe": "icon-[lucide--globe]",
    "home": "icon-[lucide--house]",
    "info": "icon-[lucide--info]",
    "info-circle": "icon-[lucide--info]",
    "key": "icon-[lucide--key-round]",
    "link": "icon-[lucide--link]",
    "lock": "icon-[lucide--lock]",
    "minus": "icon-[lucide--minus]",
    "plus": "icon-[lucide--plus]",
    "question-circle": "icon-[lucide--circle-help]",
    "save": "icon-[lucide--save]",
    "search": "icon-[lucide--search]",
    "share": "icon-[lucide--share-2]",
    "sort": "icon-[lucide--arrow-up-down]",
    "star": "icon-[lucide--star]",
    "table": "icon-[lucide--table]",
    "tag": "icon-[lucide--tag]",
    "times": "icon-[lucide--x]",
    "times-circle": "icon-[lucide--circle-x]",
    "trash": "icon-[lucide--trash-2]",
    "upload": "icon-[lucide--upload]",
    "user": "icon-[lucide--user]",
    "users": "icon-[lucide--users]",
}


def make_theme(name: str = "feather", parent: str = "bare"):
    """Create the Feather theme.

    Client themes usually extend it::

        Theme("acme", acme_root, parent="feather")

    and override only what differs: CSS variables, a few macros, a template.
    """
    return Theme(name, here, parent=parent, icon_map=icon_map)
