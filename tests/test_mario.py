import requests
import pytest
import json
import time
import uuid


UUID = str(uuid.uuid4())
print("Testing with UUID: {}".format(UUID))

def test_resource(url, params):

    #
    # /resource/
    #
    resource="/resource/"
    url = url + resource

    resp = requests.get(url, params)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["body"]) > 0
    
    #
    # /resource/{resource_id}/
    #

    resource_id = data["body"][0]["id"]
    url = url + "/" + str(resource_id)

    resp = requests.get(url, params)

    assert resp.status_code == 200
    data = resp.json()

    assert data["body"]["caption"]

    # TODO: test PUT on ``/resource/{resource_id}``
    # TODO: test DELETE on ``/resource/{resource_id}``


def test_me(url, params):
    resource = "/me/"

    url = url + resource

    resp = requests.get(url, params)
    data = resp.json()

    requests.put(url, params=params, json={"name":"x"})

    resp = requests.get(url, params)
    data = resp.json()
    print(data)
    assert data["body"]
    assert data["body"]["name"] == "x"
    assert resp.status_code == 200

    resp = requests.put(url, params=params, json={"name": UUID})
    assert resp.status_code == 200
    assert resp.json()["body"] == "OK"

    resp = requests.get(url, params)
    data = resp.json()
    assert data["body"]
    assert data["body"]["name"] == UUID

def test_reference_frame(url, access_token, app_id):

    resource ="/reference_frame"
    url = url + resource

    params = {
        "access_token": access_token,
        "app_id": app_id
    }


    resp = requests.get(url, params)
    data = resp.json()
    assert len(data["body"]) > 0


def test_map_config(url, access_token, app_id):

    resource="/map_config"
    url = url + resource

    params = {
        "access_token": access_token,
        "app_id": app_id
    }

    resp = requests.get(url, params)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["body"]) > 0

    # TODO: test ``/map_config/`` POST
    # TODO: test ``map_config/{mapConfigId} ....

def test_analytics(url, access_token, app_id):

    resource = "/analytics/updateddatasets"
    rurl = url + resource

    params = {
        "access_token": access_token,
        "app_id": app_id
    }

    resp = requests.get(rurl, params)

    assert resp.status_code == 200
    data = resp.json()
    assert data["body"]["currentPage"] == 1
    assert len(data["body"]["updatedDatasets"]) > 0
    max_pages = data["body"]["totalCount"]

    params["page"] = max_pages
    resp = requests.get(rurl, params)
    assert resp.status_code == 200
    data = resp.json()
    assert data["body"]["currentPage"] == max_pages

    resource = "/analytics/updatedmaps"
    rurl = url + resource

    params = {
        "access_token": access_token,
        "app_id": app_id
    }

    resp = requests.get(rurl, params)

    assert resp.status_code == 200
    data = resp.json()
    assert data["body"]["currentPage"] == 1
    assert len(data["body"]["updatedMaps"]) > 0
    max_pages = data["body"]["totalCount"]

    params["page"] = max_pages
    resp = requests.get(rurl, params)
    assert resp.status_code == 200
    data = resp.json()
    assert data["body"]["currentPage"] == max_pages

def test_account_user(url, access_token, app_id):

    resource = "/account/{}/dataset".format(app_id)
    rurl = url + resource

    params = {
        "access_token": access_token,
        "app_id": app_id
    }

    resp = requests.get(rurl, params)
    print(resp)


def test_dataset(url, account_id, params):
    """
    Testing resources. This test will:

    1. create dataset
    2. upload file
    3. change dataset
    4. export resource
    5. change resource
    6. delete resource
    7. delete dataset

    Resources and methods tested:

        GET /account/{accountId}/dataset
        POST /account/{accountId}/dataset
        GET /dataset/{datasetId}
        PUT /dataset/{datasetId}
        POST /dataset/{datasetId}/export
        GET /resource
        GET /resource/{resourceId}
        PUT /resource/{resourceId}
        DELETE /resource/{resourceId}
        DELETE /dataset/{datasetId}
    """


    test_url = url + "/account/{}/dataset".format(account_id)

    ## get datasets before upload
    datasets = requests.get(test_url, params).json()
    datasets_before = datasets["body"]["datasets"]

    data = {
        "files": [{
            "byte_size": 400358,
            "crc": "",
            "path_component": "dem.tiff"
        }],
        "name": UUID,
        "type": "unknown"
    }

    ## create new upload file slot
    test_url = url + "/account/{}/dataset".format(account_id)
    resp = requests.post(url=test_url, params=params, json=data)
    test_url = url.replace("api", "upload/file")
    resp = resp.json()

    assert resp["body"]
    path = resp["body"]["files"][0]["path"]
    dataset_id = resp["body"]["id"]

    assert path

    ## upload file
    with open("data/dem.tiff", "rb") as data:
        resp = requests.post(
            test_url,
            params=params,
            data = {'path': path},
            files = { 'qqfile': data })

        assert resp.status_code == 201
        assert resp.json()["success"] == True

    ## get datasets after upload
    test_url = url + "/account/{}/dataset".format(account_id)
    datasets = requests.get(test_url, params).json()
    datasets_after = datasets["body"]["datasets"]
    assert len(datasets_before) < len(datasets_after)

    ## get uploaded file details
    test_url = url + "/dataset/{}".format(dataset_id)
    resp = requests.get(test_url, params=params)
    dataset = resp.json()["body"]
    assert dataset["id"] == dataset_id
    assert dataset["status"] in ("ready", "analysing")

    ## change dataset name
    resp = requests.put(test_url, params=params, json={"name": UUID})
    resp = requests.get(test_url, params=params)
    dataset = resp.json()["body"]
    assert dataset["name"] == UUID

    ## get resources
    test_url = url + "/resource"
    resp = requests.get(test_url, params=params)
    data = resp.json()
    resources_before = data["body"]

    ## create resource
    test_url = url + "/dataset/{}/export".format(dataset_id)
    resp = requests.post(test_url, params=params, json={
          "name": UUID,
          "caption": "testing datasets",
          "description": "my description",
          "zshift": 1
        })
    #assert resp.status_code == 201
    assert resp.ok
    data = resp.json()
    assert data["body"]["name"]  == UUID
    resource_id = data["body"]["id"]

    i = 0
    while i < 10:

        print("waiting for new resource {}/10".format(i))
        ## get resource
        test_url = url + "/resource"
        resp = requests.get(test_url, params=params)
        assert resp.status_code == 200
        data = resp.json()

        if len(resources_before) < len(data["body"]):
            print("resource generated, continuing")
            break
        else:
            i += 1
            time.sleep(10)

    if i == 10:
        raise AssertionError("Exporting resource exceeded {}s".format(10*10))

    assert data["body"][-1]["name"] == UUID

    assert len(data["body"]) > len(resources_before)

    test_url = url + "/resource/{}".format(resource_id)
    resp = requests.get(test_url, params=params)
    assert resp.status_code == 200

    ## delete resource
    test_url = url + "/resource/{}".format(resource_id)
    result = requests.delete(test_url, params=params)
    assert result.status_code == 204
    result = requests.get(test_url, params=params)

    ## delete dataset
    test_url = url + "/dataset/{}".format(resource_id)
    result = requests.delete(test_url, params=params)
    assert result.status_code == 204
    result = requests.get(test_url, params=params)



@pytest.fixture
def params(app_id, access_token):
    return {
        "access_token": access_token,
        "app_id": app_id
    }

@pytest.fixture
def account_id(url, params):
    response = requests.get(url + "/me", params)
    account_id = response.json()["body"]["accounts"][0]["id"]
    assert account_id
    return account_id
