/* Switches the daisyUI theme of the page and remembers the choice. */
ckan.module("feather-theme-picker", function () {
  const STORAGE_KEY = "feather-ui-theme";

  return {
    initialize: function () {
      this.root = document.documentElement;
      this.buttons = this.el[0].querySelectorAll("[data-set-theme]");

      this.el[0].addEventListener("click", (event) => {
        const button = event.target.closest("[data-set-theme]");
        if (button) this._apply(button.dataset.setTheme, true);
      });

      this._mark(this.root.getAttribute("data-theme") || "feather");
    },

    _apply: function (theme, persist) {
      this.root.setAttribute("data-theme", theme);
      this._mark(theme);
      if (!persist) return;
      try {
        localStorage.setItem(STORAGE_KEY, theme);
      } catch (e) {
        /* private mode: the choice just lasts until the next page load */
      }
    },

    _mark: function (theme) {
      this.buttons.forEach((button) => {
        button.setAttribute("aria-checked", String(button.dataset.setTheme === theme));
      });
    },
  };
});
