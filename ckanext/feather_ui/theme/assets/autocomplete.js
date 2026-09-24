/*
 * CKAN's own forms mark fields with `data-module="autocomplete"`, a select2
 * module that ships in the `base/ckan` bundle. Themes built on ckanext-theming
 * do not load that bundle, so those fields stayed plain inputs.
 *
 * This module answers to the same name and hands text inputs over to the
 * `theming-autocomplete` widget, translating the legacy `data-module-*`
 * options (tags, createtags, key, label, tokensep, interval). Selects are left
 * alone: they stay native (daisyUI styles their dropdown).
 */
/* The stock module wins when a page loads the `base/ckan` bundle. */
if (!ckan.module.registry.autocomplete) ckan.module("autocomplete", function () {
  const flag = (value, fallback) => (value === undefined ? fallback : value === true || value === "true");

  return {
    options: {
      tags: false,
      createtags: true,
      source: null,
      key: false,
      label: false,
      tokensep: ",",
      interval: 300,
      minimumInputLength: 0,
    },

    initialize: function () {
      const el = this.el[0];
      if (el.tagName !== "INPUT") return;

      const opts = this.options;
      const tags = flag(opts.tags, false);
      const separator = (opts.tokensep || ",").charAt(0);
      const idKey = opts.key || (opts.source && /tag\/autocomplete/.test(opts.source) ? "Name" : "name");
      const labelKey = opts.label || idKey;

      const attrs = {
        "allow-multiple": tags,
        "allow-new": tags || flag(opts.createtags, true),
        joined: tags,
        separator: separator,
        "id-key": idKey,
        "label-key": labelKey,
        debounce: opts.interval,
      };
      if (opts.source) attrs.source = opts.source;
      if (opts.minimumInputLength) attrs["min-chars"] = opts.minimumInputLength;
      if (tags && el.value.trim()) {
        attrs.selected = JSON.stringify(el.value.split(separator).map((v) => v.trim()).filter(Boolean));
      }

      Object.entries(attrs).forEach(([name, value]) => el.setAttribute("data-module-" + name, value));
      el.value = "";
      el.setAttribute("data-module", "theming-autocomplete");
      ckan.module.initializeElement(el);
    },
  };
});
