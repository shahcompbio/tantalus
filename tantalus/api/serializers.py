from django.db import transaction
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer)
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from celery import chain

import tantalus.models
from tantalus.utils import start_deployment
from tantalus.exceptions.api_exceptions import *
from tantalus.exceptions.file_transfer_exceptions import *


class SampleSerializer(serializers.ModelSerializer):
    sample_id = serializers.CharField(
        validators=[
            UniqueValidator(queryset=tantalus.models.Sample.objects.all())
        ]
    )

    class Meta:
        model = tantalus.models.Sample
        fields = '__all__'


class FileInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.FileInstance
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=tantalus.models.FileInstance.objects.all(),
                fields=('file_resource', 'storage')
            )
        ]


class FileResourceSerializer(serializers.ModelSerializer):
    file_instances = FileInstanceSerializer(source='fileinstance_set', many=True, read_only=True)
    md5 = serializers.CharField(
        validators=[
            UniqueValidator(queryset=tantalus.models.FileResource.objects.all())
        ]
    )

    class Meta:
        model = tantalus.models.FileResource
        fields = '__all__'


class DNALibrarySerializer(serializers.ModelSerializer):
    library_id = serializers.CharField(
        validators=[
            UniqueValidator(queryset=tantalus.models.DNALibrary.objects.all())
        ]
    )

    class Meta:
        model = tantalus.models.DNALibrary
        fields = '__all__'


class DNASequencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.DNASequences
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=tantalus.models.DNASequences.objects.all(),
                fields=('dna_library', 'index_sequence')
            )
        ]


class SequenceLaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.SequenceLane
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=tantalus.models.SequenceLane.objects.all(),
                fields=('flowcell_id', 'lane_number')
            )
        ]


class AbstractDataSetSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = tantalus.models.AbstractDataSet
        fields = '__all__'

    def to_representation(self, obj):
        if isinstance(obj, tantalus.models.SingleEndFastqFile):
            return SingleEndFastqFileSerializer(obj, context=self.context).to_representation(obj)

        elif isinstance(obj, tantalus.models.PairedEndFastqFiles):
            return PairedEndFastqFilesSerializer(obj, context=self.context).to_representation(obj)

        elif isinstance(obj, tantalus.models.BamFile):
            return BamFileSerializer(obj, context=self.context).to_representation(obj)

        return super(AbstractDataSetSerializer, self).to_representation(obj)


class SingleEndFastqFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    lanes = SequenceLaneSerializer(many=True)
    dna_sequences = DNASequencesSerializer()
    class Meta:
        model = tantalus.models.SingleEndFastqFile
        exclude = ['polymorphic_ctype']
        #TODO: add validator


class PairedEndFastqFilesReadSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    lanes = SequenceLaneSerializer(many=True)
    dna_sequences = DNASequencesSerializer()

    class Meta:
        model = tantalus.models.PairedEndFastqFiles
        exclude = ['polymorphic_ctype']


class PairedEndFastqFilesSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = tantalus.models.PairedEndFastqFiles
        exclude = ['polymorphic_ctype']
        validators = [
            UniqueTogetherValidator(
                queryset=tantalus.models.PairedEndFastqFiles.objects.all(),
                fields=('reads_1_file', 'reads_2_file')
            )
        ]


class BamFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    lanes = SequenceLaneSerializer(many=True)
    dna_sequences = DNASequencesSerializer()

    class Meta:
        model = tantalus.models.BamFile
        exclude = ['polymorphic_ctype']
        validators = [
            UniqueTogetherValidator(
                queryset=tantalus.models.BamFile.objects.all(),
                fields=('bam_file', 'bam_index_file')
            )
        ]


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.Storage
        exclude = ['polymorphic_ctype']

    def to_representation(self, obj):
        if isinstance(obj, tantalus.models.ServerStorage):
            return ServerStorageSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, tantalus.models.AzureBlobStorage):
            return AzureBlobStorageSerializer(obj, context=self.context).to_representation(obj)
        return super(StorageSerializer, self).to_representation(obj)


class ServerStorageSerializer(serializers.ModelSerializer):
    # generic_url = serializers.SerializerMethodField(method_name='_get_generic_url')

    class Meta:
        model = tantalus.models.ServerStorage
        exclude = ['polymorphic_ctype']

    def to_representation(self, obj):
        res = super(ServerStorageSerializer, self).to_representation(obj)
        return res


class AzureBlobStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.AzureBlobStorage
        exclude = ['polymorphic_ctype']


class FileTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.FileTransfer
        fields = '__all__'


class DeploymentSerializer(serializers.ModelSerializer):
    running = serializers.BooleanField(read_only=True)
    finished = serializers.BooleanField(read_only=True)
    errors = serializers.BooleanField(read_only=True)
    file_transfers = FileTransferSerializer(many=True, read_only=True)

    class Meta:
        model = tantalus.models.Deployment
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                datasets = validated_data.pop('datasets')
                instance = tantalus.models.Deployment(**validated_data)
                instance.save()
                instance.datasets = datasets
                instance.save()
                start_deployment(instance)
            return instance
        except DeploymentUnnecessary as e:
            raise ValidationError({'unnecessary': True})
        except DeploymentNotCreated as e:
            raise ValidationError(str(e))


class GSCQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.GSCQuery
        fields = '__all__'


class MD5CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = tantalus.models.MD5Check
        fields = '__all__'


