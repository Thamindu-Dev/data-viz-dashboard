(function () {
    "use strict";
    const SDK = window.__HERMES_PLUGIN_SDK__;
    const PLUGINS = window.__HERMES_PLUGINS__;
    
    if (!SDK || !PLUGINS) return;

    const React = SDK.React;

    function DataVizDashboard() {
        return React.createElement('iframe', {
            src: `http://${window.location.hostname}:5000/`,
            style: { width: '100%', height: '100vh', border: 'none', display: 'block' },
            title: 'System Intelligence Dashboard'
        });
    }

    PLUGINS.register("data-viz-dashboard", DataVizDashboard);
})();