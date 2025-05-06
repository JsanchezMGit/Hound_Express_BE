from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import GuideSerializer
from .models import Guia, Estatus
import datetime

class GuideAPIViewSet(ViewSet):
    serializer_class = GuideSerializer

    def list(self, request):
        guides = Guia.objects.prefetch_related('estatus_set').all()
        serializer = self.serializer_class(guides, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guide = serializer.save()
            status = Estatus()
            status.status = guide.currentStatus
            status.guide = guide
            status.timestamp = datetime.datetime.now()
            status.updatedBy = request.user
            status.save()
            
            new_guide = Guia.objects.prefetch_related('estatus_set').get(pk=guide.id)
            serializer = self.serializer_class(new_guide)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        guide = Guia.objects.prefetch_related('estatus_set').filter(pk=pk).first()
        if guide:
            serializer = self.serializer_class(guide)
            return Response(serializer.data)
        return Response({'message': 'Guía no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guide = Guia.objects.filter(pk=pk).first()
            if not guide:
                return Response({'message': 'Guía no encontrada'}, status=status.HTTP_404_NOT_FOUND)
            if guide.currentStatus != serializer.validated_data.get('currentStatus'):
                guide.currentStatus = serializer.validated_data.get('currentStatus')
                guide.updatedAt = datetime.datetime.now()
                guide.save()
                status = Estatus()
                status.status = guide.currentStatus
                status.guide = guide
                status.timestamp = guide.updatedAt
                status.updatedBy = request.user
                status.save()
            refreshed_guide = Guia.objects.prefetch_related('estatus_set').get(pk=guide.id)
            serializer = self.serializer_class(refreshed_guide)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        guide = Guia.objects.filter(pk=pk).first()
        if guide:
            guide.delete()
            return Response({'message': 'La guía se eliminó correctamente'})
        return Response({'message': 'Guía no encontrada'}, status=status.HTTP_404_NOT_FOUND)