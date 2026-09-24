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

## Config settings

```ini
# Slim account bar (login, dashboard, settings) above the header.
# (optional, default: true)
ckanext.feather_ui.show_account_bar = true
```

## Customising for a client

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
| `--color-primary`, `--color-primary-content`                  | Brand colour and the text on top of it            |
| `--color-secondary`, `--color-accent`, `--color-neutral`      | Other palette colours (each has `-content`)       |
| `--color-info` / `success` / `warning` / `error`              | Status colours (each has `-content`)              |
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
| `--fui-account-bg` / `-fg`                        | Account bar                                           |
| `--fui-header-bg` / `-fg` / `-border` / `-height`, `--fui-logo-height` | Header                           |
| `--fui-toolbar-bg`                                | Breadcrumb strip                                      |
| `--fui-hero-bg` / `-fg` / `-padding`              | Home page hero (any `background-image` value)         |
| `--fui-footer-bg` / `-fg`                         | Footer                                                |
| `--fui-card-bg` / `-border` / `-shadow` / `-shadow-hover` | Cards, list items, sidebar sections           |

The site logo, title and description come from the standard CKAN config page.

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

## Optional components

To keep the stylesheet minimal, anything no `bare` page uses is switched off
but not deleted:

| What                                   | Where it lives                              |
|----------------------------------------|---------------------------------------------|
| `card`, `row`, `spinner`, `progress`, `radio`, `toast`, `toast_stack`, `fieldset`, `form_annotation`, `filters`, `nav`, `nav_item`, `sidebar_nav(_item)`, `footer_*_nav(_item)`, `tabbed_content`, `tab_pane(_wrapper)` | `templates/macros/feather/optional.html` |
| Safelists for unused variants (`btn-ghost`, `loading-*`, more `col-span-*`, ...) and styling of elements built by the `bare` JavaScript (`ckan.sandbox().ui.modal()`, notifications) | `assets/src/optional.css` |
| Extra Lucide icons                     | `icon_catalogue.py`                         |

Until enabled, those components fall back to `bare`'s unstyled versions. To
bring one back:

1. In `macros/ui.html` uncomment the "OPTIONAL COMPONENTS" block (or only the
   lines you need, plus the `import`).
2. In `assets/src/feather.css` delete the `@source not` line for
   `optional.html`, and copy the safelist lines the component needs from
   `optional.css` (e.g. `loading-*` for `spinner`).
3. `npm run build`.

For icons, copy a line from `icon_catalogue.py` into `icon_map` in `theme.py`
and rebuild.

Component names in templates (`{% macro dropdown %}`) look like class names to
the Tailwind scanner. If a build ever emits CSS for a component you don't use,
add the word to the `@source not inline(...)` list in `feather.css`; if you
enable a component that is in that list, remove it from there.

## Icons

`ui.icon("search")` renders [Lucide](https://lucide.dev) icons through
`@iconify/tailwind4`. The map lives in `theme/theme.py`; add an entry and run
`npm run build` to use another icon. Names missing from the map fall back to the
emoji of the `bare` theme.

## Project layout

```
ckanext/feather_ui/
├── plugin.py                  registers the theme (ITheme)
├── config_declaration.yaml
└── theme/
    ├── theme.py               Theme("feather", parent="bare") + icon map
    ├── icon_catalogue.py      spare icon entries (not scanned)
    ├── assets/
    │   ├── src/feather.css    Tailwind/daisyUI entry: tokens live here
    │   ├── src/optional.css   switched-off safelists and JS-element styling
    │   ├── feather.css        compiled output (committed)
    │   └── webassets.yml
    └── templates/
        ├── base.html layout.html page.html footer.html home/index.html
        └── macros/
            ├── ui.html        component registry (falls back to bare)
            ├── feather/       component implementations (+ optional.html, switched off)
            └── ui/snippets/   package / group / resource / facet / search form markup
```

## Known limitations

- Light colour scheme only (see level 4 above).
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
