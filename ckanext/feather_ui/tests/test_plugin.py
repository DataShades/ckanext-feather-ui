import ckan.plugins.toolkit as tk
import pytest
from ckan.tests import factories

from ckanext.feather_ui import helpers
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


class FakeRedis:
    def __init__(self):
        self.data: dict[str, str] = {}

    def get(self, key: str):
        return self.data.get(key)

    def setex(self, key: str, ttl: int, value: str):
        self.data[key] = value


@pytest.fixture
def redis(monkeypatch: pytest.MonkeyPatch):
    fake = FakeRedis()
    monkeypatch.setattr(helpers, "connect_to_redis", lambda: fake)
    return fake


@pytest.mark.usefixtures("with_request_context")
class TestCache:
    def test_value_is_computed_once(self, redis: FakeRedis):
        calls: list[int] = []

        def compute():
            calls.append(1)
            return {"count": 1}

        assert helpers._cached("stats", compute) == {"count": 1}
        assert helpers._cached("stats", compute) == {"count": 1}
        assert len(calls) == 1

    @pytest.mark.ckan_config(helpers.CONFIG_CACHE_TTL, 0)
    def test_zero_ttl_disables_cache(self, redis: FakeRedis):
        calls: list[int] = []
        helpers._cached("stats", lambda: calls.append(1))
        helpers._cached("stats", lambda: calls.append(1))

        assert len(calls) == 2
        assert not redis.data

    def test_redis_failure_does_not_break_the_page(self, monkeypatch: pytest.MonkeyPatch):
        def broken():
            raise ConnectionError

        monkeypatch.setattr(helpers, "connect_to_redis", broken)

        assert helpers._cached("stats", lambda: 42) == 42
