import urlparse
from rest_framework import serializers
from app.models.media import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = (
            'media_path',
            'thumbnail_path',
        )
        read_only_fields = (
            'media_path',
            'thumbnail_path',
            'md5_sum',
            'content_type',
            'duration'
        )

    def to_representation(self, instance):
        data = super(MediaSerializer, self).to_representation(instance)
        if 'request' in self.context:
            base = "%s://%s" % (self.context['request'].scheme, self.context['request'].get_host())
            data['media_url'] = urlparse.urljoin(base, instance.media_path) if instance.media_path else ""
            data['thumbnail_url'] = urlparse.urljoin(base, instance.thumbnail_path) if instance.thumbnail_path else ""
        return data
