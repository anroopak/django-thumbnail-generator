import os

import subprocess

import shutil
from django.db import models

from utils import amuze_time
from utils.amuze_config import AmuzeConfig
import hashlib


class Media(models.Model):
    class Meta:
        db_table = "amuze_media"

    media_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=AmuzeConfig.MAX_STR_LENGTH)

    content_type = models.CharField(max_length=AmuzeConfig.MAX_STR_LENGTH)
    md5_sum = models.CharField(max_length=AmuzeConfig.MAX_STR_LENGTH)

    duration = models.FloatField(default=0.0)
    media_path = models.CharField(max_length=AmuzeConfig.MAX_STR_LENGTH)
    thumbnail_path = models.CharField(max_length=AmuzeConfig.MAX_STR_LENGTH)

    @property
    def thumbnails(self):
        return os.listdir(self.thumbnail_path) if self.thumbnail_path else []

    @staticmethod
    def generate_md5(file_obj, block_size=65536):
        tmp_hash = hashlib.md5()
        tmp_buffer = file_obj.read(block_size)
        while len(tmp_buffer) > 0:
            tmp_hash.update(tmp_buffer)
            tmp_buffer = file_obj.read(block_size)
        return tmp_hash.hexdigest()

    def upload(self, media_file):
        self.md5_sum = Media.generate_md5(media_file.file)
        self.content_type = media_file.content_type
        self.save()
        self._move_to_media_folder(media_file)
        self.save()

    def _move_to_media_folder(self, media_file):
        tmp, ext = os.path.splitext(media_file.name)
        file_path = "%d_%s%s" % (self.pk, self.md5_sum, ext)
        self.media_path = os.path.join(AmuzeConfig.MEDIA_FOLDER, file_path)
        with open(self.media_path, "w+") as w_file:
            if isinstance(media_file, file):
                w_file.write(media_file.read())
            else:
                for chunk in media_file.chunks():
                    w_file.write(chunk)

    def _find_thumbnail_point(self):
        return int(self.duration / 2)

    def generate_thumbnail(self, width=AmuzeConfig.THUMBNAIL_WIDTH, height=AmuzeConfig.THUMBNAIL_HEIGHT):
        thumbnail_folder_name = "%d_thumbnail_%s" % (self.pk, self.md5_sum)
        thumbnail_point = self._find_thumbnail_point()
        self.thumbnail_path = os.path.join(AmuzeConfig.THUMBNAIL_FOLDER, thumbnail_folder_name)
        if not os.path.exists(self.thumbnail_path):
            os.mkdir(self.thumbnail_path)
        file_name = os.path.join(self.thumbnail_path, thumbnail_folder_name + "_%02d.jpg")
        cmd = "ffmpeg -i %s -ss %d \
            -vf \"select=gt(scene\,0.4)\" \
            -vf scale=%d:%d -frames:v 5 \
            -vsync vfr %s \
            -loglevel panic"
        cmd %= (self.media_path, thumbnail_point, width, height, file_name)
        subprocess.check_output(cmd, shell=True)
        self.save()

    def find_duration(self):
        cmd = "ffmpeg -i %s 2>&1 | grep Duration | awk '{print $2}' | tr -d ,"
        cmd %= self.media_path
        duration_str = subprocess.check_output(cmd, shell=True)
        duration_str = duration_str.split(".")[0]
        self.duration = amuze_time.convert_time_str_to_seconds(duration_str)
        self.save()

    def remove(self):
        os.remove(self.media_path)
        shutil.rmtree(self.thumbnail_path)
        self.delete()


def find_duration_job(media_id):
    media = Media.objects.get(pk=media_id)
    media.find_duration()


def generate_thumbnail_job(media_id):
    media = Media.objects.get(pk=media_id)
    media.generate_thumbnail()
