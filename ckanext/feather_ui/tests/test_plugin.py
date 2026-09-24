import pytest

import ckan.plugins.toolkit as tk
from ckan.tests import factories

from ckanext.theming import lib


@pytest.mark.usefixtures("with_plugins")
class TestTheme:
    def test_theme_is_registered_on_top_of_bare(self):
        theme = lib.get_active_theme()

        assert theme.name == "feather"
        assert theme.parent == "bare"

    def test_home_page_uses_theme_styles(self, app):
        resp = app.get("/")

        assert resp.status_code == 200
        assert "-feather.css" in resp.body

    @pytest.mark.usefixtures("clean_db")
    def test_dataset_pages(self, app):
        dataset = factories.Dataset(notes="Some **notes**")

        for url in [
            tk.url_for("dataset.search"),
            tk.url_for("dataset.read", id=dataset["name"]),
            tk.url_for("organization.index"),
            tk.url_for("user.login"),
        ]:
            assert app.get(url).status_code == 200

    @pytest.mark.ckan_config("ckanext.feather_ui.show_account_bar", False)
    def test_account_bar_can_be_disabled(self, app):
        assert 'id="account"' not in app.get("/").body

    def test_account_bar_is_shown_by_default(self, app):
        assert 'id="account"' in app.get("/").body

