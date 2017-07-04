# Mario REST API usage

The Mario API is designed according to [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) principles (with some slight changes).

The server and the client are communicating using set of *resources*,
represented as URL, with one or more *methods*, which can be applied on the
resources - we are using HTTP methods `GET`, `POST`, `PUT` and `DELETE`. Not all
resources are using all methods.

As data exchange format, `application/json` is used. You should make sure, that
the client application is sending `Content-type: application/json` in the
request header.

While REST is designed to be state-less, we need to make sure, that client
application is authorised to perform some operations on some applications.
Therefore, all the URLs need to have two extra parameters: `app_id` (APPLICATION_ID, 
identifies a certain application) and `access_token`. The application should be
known to you, how to obtain `access_token` is [documented elsewhere](authorization.md).

Therefore, generic URL template looks like:

```
https://[SERVER]/cloud/backend/api/[RESOURCE]?access_token=[ACCESS_TOKEN]&app_id=[APPLICATION_ID]
```

Where 

* `[SERVER]` is the Mario server name, like https://www.melown.com/
* `[RESOURCE]` is the REST API URL resource endpoint
* `[ACCESS_TOKEN]` is the authorisation character string, [see documentation](authorization.md)
* `[APPLICATION_ID]` is application identification

[Full Mario REST API documentation](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#) should be always seen at Swagger editor.

## Some API resources

We are not going to document the [full REST API resources](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#), but just some of them for example.

You can also check [tests](../tests/) for getting some hints about how to use
it.

## User profile

To get details about your own user profile, you shall check the [/me](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#operations%2Cget-%2Fme%2CUser%20profile) resource.

With HTTP GET method, you will obtain user details JSON file. You can test it in
the command line, using
[Wget](https://www.gnu.org/software/wget/manual/wget.html) tool.

```
wget -O - "https://www.melown.com/cloud/backend/api/me?access_token=NOTVaLiDAccessTookEnString34&app_id=com.melown.mario-api-docs"
```
As response, you shall obtain following JSON-encoded data:

```
{
    "body":{
        "id":111111,
        "email":"name@server.com",
        "name":"Name Surname",
        "flag_admin":false,
        "accounts":[{
            "id":5432,
            "alias":"name-server-com",
            "name":"name@server.com",
            "dataset_quota_mb":20480,
            "user_role":"admin"
        }]
    }
}
```
Which tells you something about your user ID and accounts you have access to.

Same you can do with Python:

```
import requests

url = "https://www.melown.com/cloud/backend/api/me
params = {
    "access_token": "NOTVaLiDAccessTookEnString34",
    "app_id": "com.melown.mario-api-docs"
}

resp = requests.get(url, params)
print(resp.status_code) # shall print 200
print(resp.json()) # will return JSON-encoded data

```

### Changing user name

This operation is performed using `PUT` method:

According to
[documentation](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#operations%2Cput-%2Fme%2CUser%20profile)
you can change only the `name` of an existing user by sending JSON data to the
`PUT` method:

```
wget -O - \
    --body-data='{"name":"xXx"}' \
    --method=PUT \
    --header="Content-type: application/json" \
    "https://www.melown.com/cloud/backend/api/me?access_token=NotValidAccessToken24&app_id=com.melown.mario-api-docs"
```

As result, a `{ "body": "Operation successful" }` message should be obtained.

Same example using Python (continuing from the previous example):

```
requests.put(url, params=params, json={"name":"xXx"})
```

## Uploading a dataset

Dataset upload is performed in two steps:

1. first you have to initialize empty dataset, using `POST` on `/account/[ACCOUNT_ID]/dataset`
2. then you have to upload data into the dataset, again using `POST` on `/dataset/[DATASET_ID]` resource

The process is documented in [separate file](dataset-upload.md), you can come
back to this section, once you are finished. 

## Exporting dataset as Resource

After [data upload](datset-upload.md), you need to export it as Resource in
order to be able to use it in the client-side rendering application.

Once the dataset is uploaded, you can call `POST` method on the
[/dataset/{DATASET_ID}/export](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#operations,post-/dataset/{datasetId}/export,Dataset) resource.

It may take a while, you may check the progress status of dataset-being exported using
`GET` on [/dataset/{DATASET_ID}](http://editor.swagger.io/?url=https%3A%2F%2Fraw.githubusercontent.com%2FMelown%2Fmario-cloud-api%2Fmaster%2Fdocs%2Fapi%2Findex.yaml#operations,get-/dataset/{datasetId},Dataset).

Once exported, it can be used in VTS-Client application.


