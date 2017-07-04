# Mario REST API documentation
Documentation for the mario cloud (console) API.

### Authorization process
see [docs/authorization.md](docs/authorization.md)


### Dataset upload
see [docs/dataset-upload.md](docs/dataset-upload.md)

### API
The API-documentation uses the OpenAPI Specification(OAS) and is packed together
with the [swagger-ui](http://swagger.io/swagger-ui/). A customized version of
swagger-ui can be found in this repository. To see HTML generated documentation
directly, you can visit [Mario REST API](http://editor.swagger.io/?url=https://raw.githubusercontent.com/Melown/mario-cloud-api/master/docs/api/index.yaml) on swagger.

#### Installation
Due to some specialities of the API, you need to follow the instructions here
in case you want to test the API from within swagger-ui. If you are fine with just
viewing it, you can of course just open [docs/api/index.yaml](docs/api/index.yaml)
in your local copy of swagger-ui, or you can visit the
[Swagger editor](http://editor.swagger.io/?url=https://raw.githubusercontent.com/Melown/mario-cloud-api/master/docs/api/index.yaml).

The Mario Accounts-API expects an application-ID that is connected with a certain
redirect-URL. We setup an application that redirects to `http://localhost/mario-api/oauth2-redirect.html` so you can use the documentation to test the API.

This means, you have to run a webserver, you have to run it on port 80, and you
have to make swagger-ui available under the path `/mario-api`.

To do so, just copy (or link) the whole `mario-api`-folder into your webserver's
document-root. In case you are on windows, make sure you also copy the `docs`-folder
(which is symlinked) into your `mario-api`-folder. All in all you should end up
with the following structure:

```
─ documentroot
  └─ mario-api
     ├─ index.html
     ├─ swagger-ui-bundle.js
     ...
     └─ docs
        └─ api
           ├─ account
           ├─ definitions.yaml
           ...
           └─ index.yaml
```

Now navigate your webbrowser to http://localhost/mario-api.

After logged in in via swagger-ui, you should be able to use all API-methods from
within swagger-ui.

**Content:**

* [Authorisation](docs/authorization.md)
* [REST API usage](docs/rest-api-usage.md)
* [Dataset upload](docs/dataset-upload.md)
