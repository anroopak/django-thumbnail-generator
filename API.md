# API Doc for Amuze Thumbnail Generator

## Upload
#### Request
**PUT** /v1/media/upload/
```
name = // Name of the file - str
media = // File obj
```
#### Response
```
{
  "media_id": 1,
  "thumbnails": [],
  "name": "Some Name",
  "content_type": "video/mp4",
  "md5_sum": "4431a412c0d34dec2a6cc0715d42e6df",
  "duration": 0,
  "media_path": "./media/15_4431a412c0d34dec2a6cc0715d42e6df.mp4",
  "thumbnail_path": ""
}
```

## List
**GET** /v1/media/