# Mario documentation
Documentation for the mario cloud (console) API.

### Authorization process
see [docs/authorization.md](docs/authorization.md)


### Dataset upload
see [docs/dataset-upload.md](docs/dataset-upload.md)

### API
The API-documentation uses the OpenAPI Specification(OAS) and is packed together
with the [swagger-ui](http://swagger.io/swagger-ui/). An adapted version of swagger-ui
can be found in this repository.

#### Installation
Due to some specialities of the cloud-API, you need to follow the instructions here
in case you want to test the API from within swagger-ui. If you are fine with just
viewing it, you can of course just open [docs/api/index.yaml](docs/api/index.yaml)
in your local copy of swagger-ui.

The Mario Accounts-API expects an application-ID that is bound with a redirect-URL.
We setup the app_id `com.melown.mario-api-docs` to redirect to
`http://localhost/mario-api/oauth2-redirect.html`. This means, you have to run a
webserver, you have to run on port 80, and you have to make swagger-ui available
under the path `/mario-api`.

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

After loggin in via swagger-ui, you should be able to use all API-methods from within swagger-ui.
