from rest_framework import serializers

class GuideSerializer(serializers.Serializer):
    trackingNumber = serializers.CharField(max_length=15)
    origin = serializers.CharField(max_length=100)
    destination = serializers.CharField(max_length=100)
    recipient = serializers.CharField(max_length=100)
    currentStatus = serializers.CharField(max_length=20)
    createdAt = serializers.DateField()
    updatedAt = serializers.DateField()