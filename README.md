[![Tests](https://github.com/DataShades/ckanext-feather-ui/workflows/Tests/badge.svg?branch=main)](https://github.com/DataShades/ckanext-feather-ui/actions)

# ckanext-feather-ui

A light CKAN theme for [ckanext-theming](https://github.com/DataShades/ckanext-theming),
built with [Tailwind CSS 4](https://tailwindcss.com) and
[daisyUI 5](https://daisyui.com).

## How it stays small

`feather` is a child of the `bare` theme (`parent="bare"`):

- All page templates (dataset, organization, user, admin, ...) come from `bare`.
  They contain almost no HTML of their own, only `ui.*` component calls.
- Feather re-implements the `ui.*` components with daisyUI classes
  (`theme/templates/macros/feather/`) and replaces the page skeleton
  (`base.html`, `layout.html`, `page.html`, `footer.html`) and the home page.
- Everything else (headings, links, images, autocomplete, the `ckan.sandbox().ui`
  JavaScript) falls through to `bare` through `{% ckan_extends %}`.
- No JavaScript of its own: modals use `<dialog>`, dropdowns and accordions use
  `<details>`, popovers use the native popover API.

The compiled stylesheet is about 15 KB gzipped. It contains only what the
`bare` pages use today; everything else is kept aside and can be switched back
on (see "Optional components").

## Requirements

| CKAN version | Compatible? |
|--------------|-------------|
| 2.12         | yes         |
| 2.11         | not tested  |

Requires `ckanext-theming>=0.0.6`.

## Installation

```sh
pip install -e .
```

```ini
ckan.plugins = ... feather_ui theming
ckan.ui.theme = feather
```

`theming` has to be the last plugin in the list; `feather_ui` only registers
the theme, `theming` activates it.

The compiled CSS (`theme/assets/feather.css`) is committed, so Node.js is only
needed when you change templates or design tokens.

## Customizing for a client

There are four levels, from cheapest to most involved.

### 1. Change variables (no build)

Paste overrides into the "Custom CSS" field of the CKAN admin config page:

```css
:root {
  --color-primary: oklch(52% 0.19 145);
  --fui-font-sans: "Source Sans 3", system-ui, sans-serif;
  --fui-hero-bg: url(/images/hero.jpg) center / cover;
}
```

**daisyUI tokens** (all daisyUI components follow them):

| Variable                                                      | Purpose                                           |
|---------------------------------------------------------------|---------------------------------------------------|
| `--color-primary`, `--color-primary-content`                  | Brand color and the text on top of it            |
| `--color-secondary`, `--color-accent`, `--color-neutral`      | Other palette colors (each has `-content`)       |
| `--color-info` / `success` / `warning` / `error`              | Status colors (each has `-content`)              |
| `--color-base-100` / `200` / `300`, `--color-base-content`    | Page, tinted and border surfaces, text            |
| `--radius-box`, `--radius-field`, `--radius-selector`         | Corner radius of cards, inputs, badges            |
| `--size-field`, `--size-selector`, `--border`                 | Control sizing and border width                   |

**Feather tokens:**

| Variable                                          | Purpose                                               |
|---------------------------------------------------|-------------------------------------------------------|
| `--fui-font-sans`, `--fui-font-heading`, `--fui-font-mono` | Font stacks                                  |
| `--fui-heading-weight`, `--fui-heading-color`     | Headings                                              |
| `--fui-text-muted`                                | Secondary text                                        |
| `--fui-page-width`, `--fui-page-gutter`           | Content width and side padding                        |
| `--fui-sidebar-width`, `--fui-gap`                | Sidebar width, gap between sidebar and content        |
| `--fui-field-width`                               | Maximum width of form fields                          |
| `--fui-link`, `--fui-link-hover`, `--fui-focus-ring` | Links and keyboard focus                           |
| `--fui-header-bg` / `-fg` / `-padding`, `--fui-logo-height` | Logo and search band                       |
| `--fui-nav-bg` / `-border`                        | Navigation bar below the band                         |
| `--fui-avatar-bg` / `-fg`                         | User avatar (initials) in the account menu            |
| `--fui-h1` ... `--fui-h5` (and `-lh`)             | Heading sizes and line heights                        |
| `--fui-toolbar-bg`                                | Breadcrumb strip                                      |
| `--fui-hero-bg` / `-fg` / `-padding`              | Home page hero (any `background-image` value)         |
| `--fui-footer-bg` / `-fg`                         | Footer                                                |
| `--fui-card-bg` / `-border` / `-shadow` / `-shadow-hover` | Cards, list items, sidebar sections           |

The site logo, title and description come from the standard CKAN config page. Without a configured logo the header shows the CKAN boat (`theme/public/feather/ckan-logo-boat.png`) next to the site title; a child theme can replace that file at the same path.

### 2. Change the defaults (build)

Edit the variables in `theme/assets/src/feather.css` (the `feather` daisyUI
theme and the `:root` block) and run:

```sh
npm install
npm run build      # or `npm run watch` while developing
```

### 3. Extend the theme (client extension, recommended)

Create a child theme in the client's extension instead of editing this one:

```python
from ckanext.theming.interfaces import ITheme
from ckanext.theming.lib import Theme


class AcmePlugin(ITheme, p.SingletonPlugin):
    def register_themes(self):
        return [Theme("acme", acme_root, parent="feather")]
```

```django
{# acme/templates/macros/ui.html: replace a single component #}
{% ckan_extends %}

{% macro _footer(content) %}...{% endmacro %}
{% set footer = footer | default(_footer) %}
```

For a client, inherit the theme and define a CSS file with the variable
overrides. Register it as a `styles` bundle in the child theme's
`assets/webassets.yml` and load it after Feather's by extending `base.html`:

```django
{# acme/templates/base.html #}
{% ckan_extends %}

{% block styles_theming %}
    {{ super() }}
    {% asset "theming/acme/styles" %}
{% endblock %}
```

Any template of `bare` or `feather` can be overridden the same way, and the
`layout.html` blocks (`zone_header`, `zone_toolbar`, `zone_content`, `secondary`,
`primary_content_inner`, ...) are the same as in every theming theme.

### 4. Add a dark theme

Add a second `@plugin "daisyui/theme"` block with `name: "feather-dark"` and
`prefersdark: true` to `theme/assets/src/feather.css`; daisyUI switches to it
according to `prefers-color-scheme`.

## Config settings

```ini
# Form action of the "Subscribe to newsletter" band on the home page
# (sends an `email` field). The band is hidden while this is empty.
ckanext.feather_ui.newsletter_url = https://example.com/subscribe

# Footer social icons; each one is hidden while its URL is empty.
ckanext.feather_ui.social.github = https://github.com/ckan
ckanext.feather_ui.social.youtube =
ckanext.feather_ui.social.linkedin =

# Footer links; each one is hidden while its URL is empty.
ckanext.feather_ui.footer.accessibility =
ckanext.feather_ui.footer.contact =
ckanext.feather_ui.footer.jobs =
ckanext.feather_ui.footer.press_kit =
ckanext.feather_ui.footer.terms =
ckanext.feather_ui.footer.privacy =
ckanext.feather_ui.footer.cookies =

# Seconds to cache the home page data in Redis (default: 300, 0 disables).
ckanext.feather_ui.home_cache_ttl = 300
```

## Home page

`home/index.html` follows the design: a gradient hero with the site title,
description, a joined search field and popular-tag chips; a stats card; data
categories; three resource cards; featured datasets; the newsletter band.

Data comes from four helpers in `helpers.py` (`h.feather_ui_site_stats()`,
`_top_groups()`, `_popular_tags()`, `_featured_datasets()`); "categories" are
CKAN groups and "featured" means most recently updated public datasets.
The results are cached in Redis for `home_cache_ttl` seconds (one entry per
language; only public data is cached, and a Redis failure just skips the
cache). Every section is a block (`promoted`, `search`, `popular_tags`, `stats`,
`featured_group`, `home_resources`, `featured_datasets`, `newsletter`), so a
client theme can replace or drop it. Colors are the `--color-*` and
`--fui-hero-*` variables: the primary blue is used for links and `Join`,
the teal accent for the main call-to-action buttons (`style="accent"`).

## Header and account menu

`header.html` renders the design's two tiers: logo and search on a tinted band,
navigation and the account menu on a bar below. Override these blocks in a child
theme instead of copying the file:

| Block                                   | Content                                       |
|-----------------------------------------|-----------------------------------------------|
| `header_search`                         | Search form in the band                       |
| `header_nav`                            | Main navigation items                         |
| `header_account_menu`                   | The whole account dropdown                    |
| `header_dashboard`                      | Dashboard entry                               |
| `header_account_logged`                 | Entries added by plugins, under Dashboard (Stats by default) |
| `header_account_profile`, `header_account_settings_link` | Profile entries              |
| `header_account_extra`                  | Extra entries after the settings (pages, blog, ...) |
| `header_account_log_out_link`           | Log out entry                                 |
| `header_account_notlogged`              | Log in / Register links                       |

### Adding a button from a plugin

Plugins do not put buttons into the nav bar; they add an entry to the account
menu by overriding `header_account_logged` (the same block classic CKAN plugins
already override) and calling `ui.account_nav_item`:

```django
{% ckan_extends %}

{% block header_account_logged %}
    {% if g.userobj.sysadmin %}
        {{ ui.account_nav_item(_("Demo Dashboard"), h.url_for("tables_demo.dashboard"), icon="table") }}
    {% endif %}
    {{ super() }}
{% endblock %}
```

`ui.account_nav_item(label, href, icon=...)` is a standard theming component,
so the same template works in every theming theme (the `icon` argument is
ignored where unsupported). Plugins that also have to run without `ui` can
guard with `{% if ui is defined %}` and keep their old markup as the `else`
branch, as `ckanext-tables`' demo does. Icon names come from `icon_map` in
`theme.py`.

A nav dropdown is `ui.dropdown(..., style="nav")`; menu entries are
`ui.dropdown_item(label, href, icon="cog")` separated by `ui.dropdown_divider()`.
Dropdowns are native popovers, so they close on outside click and Esc without
JavaScript (positioned with CSS anchor positioning).

## Typography

Inter (bundled: latin, latin-ext and cyrillic subsets, variable weight),
`#0F172A` text, weights 400/500/600 and Tailwind's default size scale
(12/14/16/18/20/24/30/36/48 px). Heading sizes are the `--fui-h1` ... `--fui-h5`
variables.

## Static files

`theme/public/` is served from the site root by the plugin, so the default logo
is `/feather/ckan-logo-boat.png` and the fonts are `/feather/fonts/*.woff2`. The
`@font-face` rules in `assets/src/feather.css` use these absolute URLs, because
webassets rewrites relative `url()`s against the bundle, not the site root. On a
portal served under a URL prefix (`ckan.root_path`), override the `@font-face`
`src` in the client's CSS.

## Optional components

To keep the stylesheet minimal, anything no `bare` page uses is switched off
but not deleted:

| What                                   | Where it lives                              |
|----------------------------------------|---------------------------------------------|
| `card`, `row`, `spinner`, `progress`, `radio`, `toast`, `toast_stack`, `fieldset`, `form_annotation`, `filters`, `nav`, `nav_item`, `sidebar_nav(_item)`, `tabbed_content`, `tab_pane(_wrapper)` | `templates/macros/feather/optional.html` |
| Safelists for unused variants (`btn-ghost`, `loading-*`, more `col-span-*`, ...) and styling of elements built by the `bare` JavaScript (`ckan.sandbox().ui.modal()`, notifications) | `assets/src/optional.css` |
| Extra Heroicons                     | `icon_catalog.py`                         |

Until enabled, those components fall back to `bare`'s unstyled versions. To
bring one back:

1. In `macros/ui.html` uncomment the "OPTIONAL COMPONENTS" block (or only the
   lines you need, plus the `import`).
2. In `assets/src/feather.css` delete the `@source not` line for
   `optional.html`, and copy the safelist lines the component needs from
   `optional.css` (e.g. `loading-*` for `spinner`).
3. `npm run build`.

For icons, copy a line from `icon_catalog.py` into `icon_map` in `theme.py`
and rebuild.

Component names in templates (`{% macro dropdown %}`) look like class names to
the Tailwind scanner. If a build ever emits CSS for a component you don't use,
add the word to the `@source not inline(...)` list in `feather.css`; if you
enable a component that is in that list, remove it from there.

## Icons

`ui.icon("search")` renders [Heroicons](https://heroicons.com) (outline) icons through
`@iconify/tailwind4`. The map lives in `theme/theme.py`; add an entry and run
`npm run build` to use another icon. Names missing from the map fall back to the
emoji of the `bare` theme.

## Project layout

```
ckanext/feather_ui/
├── plugin.py                  registers the theme (ITheme)
├── helpers.py                 data for the home page
├── config_declaration.yaml
└── theme/
    ├── theme.py               Theme("feather", parent="bare") + icon map
    ├── icon_catalog.py      spare icon entries (not scanned)
    ├── public/feather/        static files: default logo, fonts/ (Inter, OFL license included)
    ├── assets/
    │   ├── src/feather.css    Tailwind/daisyUI entry: tokens live here
    │   ├── src/optional.css   switched-off safelists and JS-element styling
    │   ├── feather.css        compiled output (committed)
    │   └── webassets.yml
    └── templates/
        ├── base.html layout.html header.html page.html footer.html home/index.html
        └── macros/
            ├── ui.html        component registry (falls back to bare)
            ├── feather/       component implementations (+ optional.html, switched off)
            └── ui/snippets/   package / group / resource / facet / search form markup
```

## Known limitations

- Light color scheme only (see level 4 above).
- Elements built by the `bare` JavaScript (`ckan.sandbox().ui.*`) are not
  styled; the ready-made rules are in `optional.css`.
- `ui.heading`, `ui.table_cell` and other components inherited from
  `ckanext-theming` insert their `content` argument without HTML escaping.
  Feather's own components escape it, but escape user-provided strings before
  passing them to the inherited ones.

## Developer installation

```sh
git clone https://github.com/DataShades/ckanext-feather-ui.git
cd ckanext-feather-ui
pip install -e '.[dev]'
npm install
```

## Tests

```sh
pytest --ckan-ini=test.ini
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
