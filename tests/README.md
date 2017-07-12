# Melown cloud REST API test

The system tests are written using Python programming language, [pytest test suite](https://docs.pytest.org/en/latest/) and [requests library](http://docs.python-requests.org/en/master/).

To get tests up and running, you first need to 

1. obtain `access_token`
2. know server URL
3. know application id.

Once you have all those informations, you can run the tests

## Start virtualenv

It's always good to use Python [virtualenv](https://virtualenv.pypa.io/en/stable/) as starter.

## Install dependences

Once `virtualenv` is set, run `pip`

```
pip install -r requirements
```

## Run the tests

Just use Pytest and set needed informations:

```
pytest test_mario.py \
    --access_token=[YOUR_ACCESS_TOKEN]
    --url=https://[SERVER_URL]/cloud/backend/api \
    --app_id=[APPLICTION_ID]
```
