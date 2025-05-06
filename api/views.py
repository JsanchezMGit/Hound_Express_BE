from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import GuideSerializer
from .models import Guia

class GuideAPIViewSet(ViewSet):
    serializer_class = GuideSerializer

    def list(self, request):
        guides = Guia.objects.values('trackingNumber', 'origin', 'destination', 'recipient', 'currentStatus', 'createdAt', 'updatedAt')
        return Response(guides)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guide = Guia()
            guide.trackingNumber = serializer.validated_data.get('trackingNumber')
            guide.origin = serializer.validated_data.get('origin')
            guide.destination = serializer.validated_data.get('destination')
            guide.recipient = serializer.validated_data.get('recipient')
            guide.recipient = serializer.validated_data.get('recipient')
            guide.currentStatus = serializer.validated_data.get('currentStatus')
            guide.save()
            return Response({guide.trackingNumber, guide.origin, guide.destination, guide.recipient, guide.currentStatus, guide.createdAt, guide.updatedAt})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        guide = Guia.objects.filter(pk=pk).first()
        return Response({guide.trackingNumber, guide.origin, guide.destination, guide.recipient, guide.currentStatus, guide.createdAt, guide.updatedAt})
    
    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guide = Guia.objects.filter(pk=pk).first()
            guide.currentStatus = serializer.validated_data.get('status')
            guide.save()
            return Response({guide.trackingNumber, guide.origin, guide.destination, guide.recipient, guide.currentStatus})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        guide = Guia.objects.filter(pk=pk).first()
        guide.delete()
        return Response({"message":"La guia se elimino"})