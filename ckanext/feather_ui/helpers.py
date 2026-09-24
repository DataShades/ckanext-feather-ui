from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any, TypeVar

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.lib.redis import connect_to_redis

log = logging.getLogger(__name__)

T = TypeVar("T")

CONFIG_CACHE_TTL = "ckanext.feather_ui.home_cache_ttl"
CACHE_PREFIX = "ckanext-feather-ui:home:"


def _cached(name: str, compute: Callable[[], T]) -> T:
    """Return `compute()`, cached in Redis for `home_cache_ttl` seconds.

    Only public data is cached, so one entry per language serves everybody.
    Redis problems never break the page: the value is just computed again.
    """
    ttl = tk.config.get(CONFIG_CACHE_TTL)
    if not ttl:
        return compute()

    key = f"{CACHE_PREFIX}{tk.h.lang()}:{name}"
    try:
        conn = connect_to_redis()
        raw = conn.get(key)
        if raw is not None:
            return json.loads(raw)
    except Exception:
        log.warning("Cannot read %s from the cache", key, exc_info=True)
        return compute()

    value = compute()
    try:
        conn.setex(key, int(ttl), json.dumps(value, default=str))
    except Exception:
        log.warning("Cannot write %s to the cache", key, exc_info=True)

    return value


def feather_ui_site_stats() -> dict[str, int]:
    """Counts shown on the home page: public datasets, organizations, groups."""

    def compute():
        datasets = tk.get_action("package_search")({"ignore_auth": True}, {"rows": 0, "fl": "id"})["count"]

        def count(is_organization: bool) -> int:
            return (
                model.Session.query(model.Group)
                .filter(model.Group.state == "active", model.Group.is_organization == is_organization)
                .count()
            )

        return {"datasets": datasets, "organizations": count(True), "groups": count(False)}

    return _cached("stats", compute)


def feather_ui_top_groups(limit: int = 9) -> list[dict[str, Any]]:
    """Groups with the most datasets."""
    return _cached(
        f"groups:{limit}",
        lambda: tk.get_action("group_list")(
            {"ignore_auth": True}, {"all_fields": True, "sort": "package_count desc", "limit": limit}
        ),
    )


def feather_ui_popular_tags(limit: int = 12) -> list[dict[str, Any]]:
    """The most used tags as `{name, display_name, count}`."""

    def compute():
        result = tk.get_action("package_search")(
            {"ignore_auth": True}, {"rows": 0, "facet.field": ["tags"], "facet.limit": limit, "facet.mincount": 1}
        )
        return result["search_facets"].get("tags", {}).get("items", [])

    return _cached(f"tags:{limit}", compute)


def feather_ui_featured_datasets(limit: int = 4) -> list[dict[str, Any]]:
    """Most recently updated public datasets."""
    return _cached(
        f"datasets:{limit}",
        lambda: tk.get_action("package_search")({"ignore_auth": True}, {"rows": limit, "sort": "metadata_modified desc"})[
            "results"
        ],
    )
