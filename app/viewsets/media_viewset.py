from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status

from app.models.media import Media, find_duration_job, generate_thumbnail_job
from app.serializers.media_serializer import MediaSerializer

from utils.amuze_config import AmuzeConfig
from django_q.tasks import Chain


class MediaViewset(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('media_id', 'name', )
    search_fields = ('name', )

    def create(self, request, *args, **kwargs):
        request_ser = MediaSerializer(data=request.data)
        if not request_ser.is_valid():
            return Response(request_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        name = request_ser.data['name']
        media_file = request.FILES['media']

        if media_file.content_type not in AmuzeConfig.SUPPORTED_FORMATS:
            response_text = {
                "error": "File Format not supported"
            }
            return Response(response_text, status=status.HTTP_400_BAD_REQUEST)

        if media_file.size > AmuzeConfig.SUPPORTED_FILE_SIZE:
            response_text = {
                "error": "File size exceeds supported file size"
            }
            return Response(response_text, status=status.HTTP_400_BAD_REQUEST)

        media = Media(name=name)
        media.upload(media_file)

        chain = Chain()
        chain.append(find_duration_job, media.pk)
        chain.append(generate_thumbnail_job, media.pk)
        chain.run()

        media_ser = MediaSerializer(media, context={'request': request})
        return Response(media_ser.data, status=status.HTTP_201_CREATED)

    @list_route(methods=['DELETE'])
    def remove(self, request, *args, **kwargs):

        class RequestSerializer(serializers.Serializer):
            ids = serializers.ListField(child=serializers.IntegerField())

        request_ser = RequestSerializer(data=request.data)
        if not request_ser.is_valid():
            return Response(request_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        media_ids = request_ser.data['ids']
        media_objs = self.queryset.objects.filter(pk__in=media_ids)

        missing_ids = list(set(media_ids) - set([t.pk for t in media_objs]))
        if len(missing_ids) != 0:
            return Response({
                "error": "Some IDs are missings - `%s`" % "`,`".join([str(t) for t in missing_ids])
            }, status=status.HTTP_400_BAD_REQUEST)

        for media in media_objs:
            media.remove()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            media = self.queryset.get(pk=pk)
            media.remove()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({"error": e.message}, status=status.HTTP_404_NOT_FOUND)
