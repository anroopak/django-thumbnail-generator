# API Doc for Amuze Thumbnail Generator

## Upload
#### Request
**POST** /v1/media/
Type: multipart/form-data
```
name = // Name of the file - str
media = // File obj
```
#### Response
```
Code: 201
{
  "media_id": 1,
  "name": "Name",
  "content_type": "video/x-msvideo",
  "md5_sum": "0d25f310ce0308e584756f03158b7201",
  "duration": -1,
  "media_url": "http://localhost:8000/media/1_md5.avi",
  "thumbnail_url": ""
}
```

## List
#### Request
**GET** /v1/media/
#### Response
```
Code : 200,
{
  "count": 12,
  "next": "http://localhost:8000/v1/media/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "media_id": 1,
      "name": "Some Name",
      "content_type": "video/mp4",
      "md5_sum": "4431a412c0d34dec2a6cc0715d42e6df",
      "duration": 0,
      "media_url": "http://localhost:8000/media/1_4431a412c0d34dec2a6cc0715d42e6df.mp4",
      "thumbnail_url": ""
    },
    {
      "media_id": 2,
      "name": "Some Name",
      "content_type": "video/mp4",
      "md5_sum": "4431a412c0d34dec2a6cc0715d42e6df",
      "duration": 109,
      "media_url": "http://localhost:8000/media/2_4431a412c0d34dec2a6cc0715d42e6df.mp4",
      "thumbnail_url": "http://localhost:8000/thumbnail/2_thumbnail_4431a412c0d34dec2a6cc0715d42e6df"
    },
    ...
  ]
}
```


## Update
#### Request
**PUT** /v1/media/:media_id/
```
{
	"media_id": 1,
	"name": "New name"
}
```
#### Response
```
{
  "media_id": 10,
  "name": "New name",
  "content_type": "video/mp4",
  "md5_sum": "30a799b6b37985aa3341754d46db8db8",
  "duration": 83,
  "media_url": "http://localhost:8000/media/10_30a799b6b37985aa3341754d46db8db8.mp4",
  "thumbnail_url": "http://localhost:8000/thumbnail/10_thumbnail_30a799b6b37985aa3341754d46db8db8.jpg"
}
```

## Delete
#### Request
**DELETE** /v1/media/:media_id/
#### Response
```
Code: 204
```

## Delete Bulk
#### Request
**DELETE** /v1/media/remove/
```
{
	"ids": [1, 2, 3]
}
```
#### Response
```
Code: 204
```
