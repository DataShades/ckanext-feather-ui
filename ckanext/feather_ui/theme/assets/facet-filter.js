/* Filters the items of a facet section by the text typed into its search box. */
ckan.module("feather-facet-filter", function () {
  return {
    initialize: function () {
      const section = this.el[0];
      this.input = section.querySelector("[data-facet-filter]");
      this.noMatch = section.querySelector("[data-facet-nomatch]");
      this.items = section.querySelectorAll("[data-facet-item]");

      if (this.input) {
        this.input.addEventListener("input", this._onInput.bind(this));
      }
    },

    _onInput: function () {
      const needle = this.input.value.trim().toLowerCase();
      let visible = 0;

      this.items.forEach(function (item) {
        const match = item.textContent.toLowerCase().includes(needle);
        item.hidden = !match;
        if (match) visible++;
      });

      this.noMatch.classList.toggle("hidden", visible > 0);
    },
  };
});
