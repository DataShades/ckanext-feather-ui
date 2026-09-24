from __future__ import annotations

import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckanext.theming.interfaces import ITheme
from ckanext.theming.lib import Theme

from .theme.theme import make_theme


@tk.blanket.config_declarations
class FeatherUiPlugin(ITheme, p.SingletonPlugin):
    """Registers the `feather` theme.

    Activate it with `ckan.ui.theme = feather`; the `theming` plugin has to be
    enabled as well, after this one.
    """

    # ITheme

    def register_themes(self) -> list[Theme]:
        return [make_theme()]
