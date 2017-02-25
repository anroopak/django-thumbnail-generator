# Amuze Thumbnail Generator - Design

## Architecture

```
       Client          |          Server             |            Async Job
       ------          |          ------             |            ---------
                       |                             |
                 (1) Upload                          |
              --------------->                       |
                       |                             |
                       |   (2) Save in Location      |
                       |                             |
                       |                      (3) Trigger Async Job
                       |                       to Generate Thumbnail
                       |                    ----------------------->
                       |                             |
                (4) Response                         |
             <----------------                       |
                       |                             |
                       |                             |        (*.1) Generate thumbnail
                       |                             |
                       |                             |        (*.2) Update the thumbnail URL

```


## Model
 - media_id = Auto incremented ID field
 - name = String - name of the media
 - content_type = String - content type (mime type) of the media
 - md5_sum = String - md5 checksum of the media
 - duration = Float - duration of the media. Default is -1, when duration calculation has not been performed.
 - media_path = String - path to the media
 - thumbnail_path = String - path to the thumbnail

## Some Design decisions
#### 1. Async Job to generate thumbnail, determine duration
Generation of thumbnail and determination of duration uses more computing power. 
These operations are time consuming also. 

Making the user wait for these jobs to complete, would not be a good UX.
Hence, response is sent as soon as media upload is completed, and these operations are performed in background.

#### 2. Why not use `FileField` for storing media?
Using `FileField` restricts us to the Django framework to interpret the model.
 
Also, it restricts us from storing the media in other storage services like AWS S3, Google Cloud storage. 
