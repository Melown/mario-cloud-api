# Authorization

### Authorization process

The Melown Accounts service is based on the OAuth 2.0 framework.
The following text assumes basic knowledge of OAuth 2.0.

If, for any reason, you are not able to provide an OAuth 2.0-flow, please read
how to [authorize via password](#authorization-via-password) below.

In addition to OAuth 2.0, Melown Accounts adds support for multiple services.

The general authorization process looks like this:

![Authorization process](../img/authorization.png "Authorization process")

To use any Melown service API, you first need to obtain an Access token. The access
token binds your Melown service, client application and a specific user together.

This Access token must be attached to any Melown service API call via a
GET-method, usually named `access_token`. Each access token is valid only for
a limited amount of time. When an access token expires, the API call is rejected
and your app must obtain a new token.

To start the authenticaton process, do a GET-request to the following URL

```
https://www.melown.com/accounts/auth/init/
```

with the following parameters:

|Name           |Description                              |Value |
|---------------|-----------------------------------------|--------|
|`service_id`   |The melown-service the token will be for.|`mario` |
|`client_id`    |The application-ID for your app (see below).||
|`redirect_uri` |The URL the account service should redirect to on a successful login. This is bound to a certain `client_id` (see below). You can use exactly one `redirect_uri` per `client_id`, and it has to be exactly as you sent it to us (including a possible trailing slash!)||
|`auth_method`  |The method(s) for authentication. |`standard` |
|`response_type`|The type of authentication-response you expect.|`access_token` |
|`scopes`       |Requested scope.|`MARIO_API` |
|`state`        |Optional: Client app context data used against XSRF attacks. It's strongly recommended to use this parameter. Can be up to 30 chars.||

If these parameters identify a valid combination of app, service and scope, Melown
Accounts will navigate the user through the authorization process and redirect
him to your app (the `redirect_uri`), if successful.

While doing so, the following parameters will be passed back to your app:

|Name           |Description                              |Value |
|---------------|-----------------------------------------|------|
|`access_token` |Newly generated access token.            ||
|`expires`      |UNIX timestamp: When the token will become invalid.||
|`state`        |The client app context data passed to Melown Accounts.||
|`action`       |Action performed.                        |`accounts.signin`|

In case an error occurred, Melown Accounts will instead pass these parameters:

|Name         |Description        |
|-------------|-------------------|
|`error`      |Error description. |
|`error_code` |Error code.        |

### `client_id` and `redirect_uri`

You obtain a `client_id` by contacting us. Please send an email to `info at melown dot com`
and tell us, what you are planning to do. In any case, please provide a
`redirect_uri` (and include that in your email), to where we should redirect
after a successful login.

### Authorization via password

In case the default authorization via OAuth 2.0 is not an option for you please
contact us. We can enable your application for password authentication.

To perform a login with email and password, do a `POST`-request to the following URL:

```
https://www.melown.com/accounts/auth/login/
```

with the GET-parameters `service_id`, `client_id`, `scopes` (see above) and a JSON-body
containing an object with two properties `email` and `password`.

When successful, you will receive a JSON object

```json
{
  "result": "aaaaaabbbbbbcccccc"
}
```

where `result` will be your access token.

In case of an error, you will receive

```json
{
  "error": {
    "name": "Error",
    "code":401,
    "message":"Authorization failed"
  }
}
```
or similar.
