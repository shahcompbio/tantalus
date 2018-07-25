from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import django_filters
import tantalus.models
import tantalus.api.serializers
import tantalus.tasks
from tantalus.api.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class OwnerEditModelViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class_readonly
        return self.serializer_class_readwrite


class SampleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tantalus.models.Sample.objects.all()
    serializer_class = tantalus.api.serializers.SampleSerializer
    filter_fields = ('sample_id',)


class FileResourceViewSet(OwnerEditModelViewSet):
    queryset = tantalus.models.FileResource.objects.all()
    serializer_class_readonly = tantalus.api.serializers.FileResourceSerializerRead
    serializer_class_readwrite = tantalus.api.serializers.FileResourceSerializer
    filter_fields = ('id',)


class DNALibraryViewSet(OwnerEditModelViewSet):
    queryset = tantalus.models.DNALibrary.objects.all()
    serializer_class_readonly = tantalus.api.serializers.DNALibrarySerializer
    serializer_class_readwrite = tantalus.api.serializers.DNALibrarySerializer
    filter_fields = ('library_id',)


class SequencingLaneViewSet(OwnerEditModelViewSet):
    queryset = tantalus.models.SequencingLane.objects.all()
    serializer_class_readonly = tantalus.api.serializers.SequencingLaneSerializer
    serializer_class_readwrite = tantalus.api.serializers.SequencingLaneSerializer
    filter_fields = ('flowcell_id', 'lane_number', 'library_id')


class SequenceDatasetViewSet(OwnerEditModelViewSet):
    queryset = tantalus.models.SequenceDataset.objects.all()
    serializer_class_readonly = tantalus.api.serializers.SequenceDatasetSerializerRead
    serializer_class_readwrite = tantalus.api.serializers.SequenceDatasetSerializer
    filter_fields = ('library__library_id', 'sample__sample_id',)


class StorageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tantalus.models.Storage.objects.all()
    serializer_class = tantalus.api.serializers.StorageSerializer
    filter_fields = ('name',)


class ServerStorageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tantalus.models.ServerStorage.objects.all()
    serializer_class = tantalus.api.serializers.ServerStorageSerializer
    filter_fields = ('name',)


class AzureBlobStorageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = tantalus.models.AzureBlobStorage.objects.all()
    serializer_class = tantalus.api.serializers.AzureBlobStorageSerializer


class FileInstanceViewSet(OwnerEditModelViewSet):
    queryset = tantalus.models.FileInstance.objects.all()
    serializer_class_readonly = tantalus.api.serializers.FileInstanceSerializerRead
    serializer_class_readwrite = tantalus.api.serializers.FileInstanceSerializer
    filter_fields = ('storage__name',)


class FileTransferViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.FileTransfer.objects.all()
    serializer_class = tantalus.api.serializers.FileTransferSerializer
    filter_fields = ('name', 'id',)


class MD5CheckViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.MD5Check.objects.all()
    serializer_class = tantalus.api.serializers.MD5CheckSerializer


class BRCImportFastqsViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.BRCFastqImport.objects.all()
    serializer_class = tantalus.api.serializers.ImportBRCFastqsSerializer
    filter_fields = ('id',)


class QueryGscWgsBamsViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.GscWgsBamQuery.objects.all()
    serializer_class = tantalus.api.serializers.QueryGscWgsBamsSerializer


class QueryGscDlpPairedFastqsViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.GscDlpPairedFastqQuery.objects.all()
    serializer_class = tantalus.api.serializers.QueryGscDlpPairedFastqsSerializer
    filter_fields = ('dlp_library_id', 'id',)


class ImportDlpBamViewSet(viewsets.ModelViewSet):
    queryset = tantalus.models.ImportDlpBam.objects.all()
    serializer_class = tantalus.api.serializers.ImportDlpBamSerializer
    filter_fields = ('id',)


class FileTransferRestart(APIView):
    def get(self, request, pk, format=None):
        transfer = tantalus.models.FileTransfer.objects.get(pk=pk)
        serializer = tantalus.api.serializers.FileTransferSerializer(transfer)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        transfer = tantalus.models.FileTransfer.objects.get(pk=pk)
        if not transfer.running:
            transfer.state = 'transfer files queued'
            transfer.finished = False
            transfer.save()
            tantalus.tasks.transfer_files_task.apply_async(
                args=(transfer.id,),
                queue=transfer.get_queue_name())
        serializer = tantalus.api.serializers.FileTransferSerializer(transfer)
        return Response(serializer.data)


class DatasetsTag(viewsets.ModelViewSet):
    """
    To tag datasets in this endpoint, use the following JSON format to POST:
        { "name": "test_api_tag", "datasets": [1, 2, 3, 4] }
    """
    queryset = tantalus.models.Tag.objects.all()
    serializer_class = tantalus.api.serializers.DatasetTagSerializer


# TODO: move this
from tantalus.backend.serializers import *

class AddDataView(viewsets.ViewSet):
    def create(self, request, format=None):
        with django.db.transaction.atomic():
            for dictionary in request.data:
                if dictionary['model'] == 'FileInstance':
                    dictionary.pop('model')
                    get_or_create_serialize_file_instance(dictionary)

                elif dictionary['model'] == 'BamFile':
                    dictionary.pop('model')
                    get_or_create_serialize_bam_file(dictionary)

                elif dictionary['model'] == 'PairedEndFastqFiles':
                    dictionary.pop('model')
                    get_or_create_serialize_fastq_files(dictionary)

                elif dictionary['model'] == 'ReadGroup':
                    dictionary.pop('model')
                    get_or_create_serialize_read_group(dictionary)

                else:
                    raise ValueError('model type {} not supported'.format(dictionary['model']))

            return Response('success', status=201)
