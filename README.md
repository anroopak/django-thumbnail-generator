# Amuze Thumbnail Generator

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

## Installing
```
$ sudo apt-get install ffmpeg
$ pip install -r requirements.txt
```

## Running
### 1. Server
```
$ python manage.py runserver
```
### 2. Queue
```
$ python manage.py qcluster
```