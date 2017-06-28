# Upload

You can upload custom data to our platform and use these resources in your maps.

The following data formats are supported:

- tls tileset data
- [GDAL raster data](http://www.gdal.org/formats_list.html)
- [VEF tileset data](https://)

## Analysing your data

Before uploading possibly gigabytes of data, you can run an analysis on that data,
to see if we can process it. This step is optional, but it is suggested you
do this. Otherwise you might end up with invalid data that just uses up your precious
space but is not usable.

The analyse process is described in the [Dataset analysis](upload-analysis.md) document.

## Creating a dataset

To upload custom data, you first need to create a new dataset, and then upload your
files to that dataset.

Start by making a `POST`-request to `/cloud/backend/api/account/<account-ID>/dataset`
with the following body:
```
{
  files: <filelist>,
  name: <dataset-name>,
  type: "unknown"
}
```

- `<dataset-name>` is the name the dataset will have
- `<filelist>` is an array of `files`

A `file` is an object:
```
{
  byte_size: <file-size>,
  crc: "",
  path_component: <file-name>
}
```

- `<file-size>` is the size of the file in bytes
- `<file-name>` is the basename (without path) of the file (yes, although it is named "path_component")

Example:
```
{
  files: [
    {
      byte_size: 1200032,
      crc: "",
      path_component: "myhome.tiff"
    }
  ],
  name: "At home",
  type: "unknown"
}
```

You will receive a response with the created dataset:
```
{
  "body": {
    "id": 102,
    "name": "At home",
    "owner_account_id": 205,
    "type": "unknown",
    "status": "uploading",
    "progress": 0,
    "byte_size": 1200032,
    "area": 0,
    "make": {
      "analyse_target_id": null,
      "export_target_id": null,
      "export_last_status": null,
      "export_last_message": null
    },
    "time_created": "2017-06-28T08:11:48.000Z",
    "time_edited": "2017-06-28T08:11:48.000Z",
    "time_analyse_started": "2017-06-28T08:11:48.000Z",
    "time_export_started": null,
    "upload_progress": 0,
    "analyse_progress": 0,
    "export_progress": 0,
    "analyse_status": null,
    "export_status": null,
    "category": null,
    "format": null,
    "format_detail": null,
    "files": [
      {
        "path": "102/upload/data/myhome.tiff",
        "progress": 0,
        "crc": "",
        "upload_byte_offset": 0,
        "byte_size": 1200032
      }
    ],
    "resources": []
  }
}
```

Now you can upload the actual file(s) to that dataset:

## Uploading files

For each of your files (the `files`-array in the response):

- Create a form (`multipart/form-data`) with the following fields:

  |Name   |Type |Use |
  |-------|-----|----|
  |qqfile |file |The actual file |
  |path   |text |The internal path to that file, as it appears in the `files`-array |

- `POST` this to `/cloud/backend/upload/file`

This will kick off an import process that starts with analysing the file (again).

You would then start to query for progress of the whole process via `/cloud/backend/api/dataset/<dataset-id>`. The response will be the same like the one above from uploading the dataset.

When the `status`-property of the response is "ready", the file was successfully uploaded, analysed and imported.
