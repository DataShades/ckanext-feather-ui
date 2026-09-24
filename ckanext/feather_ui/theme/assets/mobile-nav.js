/* Two-level navigation drawer: switches between its panels and starts over each time it opens. */
ckan.module("feather-mobile-nav", function () {
  return {
    initialize: function () {
      const drawer = this.el[0];
      this.panels = drawer.querySelectorAll("[data-nav-panel]");

      drawer.addEventListener("click", (event) => {
        const trigger = event.target.closest("[data-nav-open]");
        if (trigger) this._show(trigger.dataset.navOpen);
      });
      drawer.addEventListener("toggle", (event) => {
        if (event.newState === "closed") this._show("main");
      });
    },

    _show: function (name) {
      this.panels.forEach((panel) => {
        panel.hidden = panel.dataset.navPanel !== name;
      });
    },
  };
});
