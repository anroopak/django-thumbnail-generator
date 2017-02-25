# Amuze Thumbnail Generator

[1. Design](./Design.md)
[2. API Doc](./API.md)

## Installing
```
$ sudo apt-get install ffmpeg
$ pip install -r requirements.txt
$ python manage.py migrate
```

## Running
Both the server and the qcluster needs to run in parallel. 
### 1. Server
```
$ python manage.py runserver
```
### 2. Queue
```
$ python manage.py qcluster
```