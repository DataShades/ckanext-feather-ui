(function (ckan, $) {
    // Ensure global `fui` object exists
    window.fui = window.fui || {};

    function toggleTheme() {
        document.documentElement.classList.toggle('dark');
        localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    }

    // Check for saved theme preference or default to light mode
    if (
        localStorage.theme === 'dark' ||
        (!localStorage.theme && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
        document.documentElement.classList.add('dark');
    }

    // Expose to global `fui`
    window.fui.toggleTheme = toggleTheme;

})(this.ckan, this.jQuery);
