from rest_framework import serializers
from app.models.media import Media


class MediaSerializer(serializers.ModelSerializer):

    thumbnails = serializers.ListField()

    class Meta:
        model = Media
        read_only_fields = ('media_path',
                            'thumbnail_path',
                            'md5_sum',
                            'ext',
                            'content_type',
                            'duration')
