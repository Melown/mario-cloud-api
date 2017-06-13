# projects/mario-cloud-api

Documentation for mario cloud (console application).

This documentation is a collection
of yaml-files for [swagger](http://swagger.io/). You can use [swagger-ui](http://swagger.io/swagger-ui/) to view and try it.

The dataset-upload is documented in [upload-analysis.md](upload-analysis.md)

### Installation
- clone swagger-ui from https://github.com/swagger-api/swagger-ui.git
- Make the `dist`-folder from swagger-ui accessible to your webserver.
- Make the `api`-folder from this repository accessible to your webserver.
- Edit `dist/index.html` in swagger-ui:  
  Look for the lines where the `SwaggerUIBundle` gets initialized (`window.onload`)
  and change the `url` there.  
  If your `api/index.yaml` is for example accessible under `http://localhost/mario-cloud-api/index.yaml`,
  your `onload` should look like this:
```
window.onload = function() {
  // Build a system
  const ui = SwaggerUIBundle({
    url: "http://localhost/mario-cloud-api/index.yaml",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  })

  window.ui = ui
}

```
Now open swagger-ui in your webbrowser.

The reason for using a webserver is, that CORS-policies usually will prevent you from accessing swagger-ui from the filesystem directly (or rather prevents swagger-ui from loading the documentation).

If you absolutely insist on running swagger-ui from the filesystem, you can probably tamper with your browser settings and allow local file XHR-requests.
