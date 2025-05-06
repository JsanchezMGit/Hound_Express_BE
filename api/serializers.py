from api.models import Guia, Estatus
from rest_framework import serializers

class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus
        fields = ['status', 'timestamp', 'updatedBy']
        read_only_fields = ['timestamp']

class GuideSerializer(serializers.ModelSerializer):
    history = StatusHistorySerializer(many=True, read_only=True, source='estatus_set')
    class Meta:
        model = Guia
        fields = ['id', 'trackingNumber', 'origin', 'destination', 'recipient', 'currentStatus', 'createdAt', 'updatedAt', 'history']
        read_only_fields = ['createdAt', 'updatedAt']