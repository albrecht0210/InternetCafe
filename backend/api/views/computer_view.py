from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Computer
from ..serializers import ComputerSerializer, ComputerStatusUpdateSerializer

class ComputerViewSet(mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, 
                      mixins.DestroyModelMixin, 
                      viewsets.GenericViewSet):
    
    serializer_class = ComputerSerializer
    queryset = Computer.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'update_status':
            return ComputerStatusUpdateSerializer
        return ComputerSerializer
    
    # Admin
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self._get_computer(queryset=queryset)

    #Admin
    @action(methods=['get'], detail=False)
    def available(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=1)
        return self._get_computer(queryset=queryset)

    #Admin
    @action(methods=['get'], detail=False)
    def pending(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=2)
        return self._get_computer(queryset=queryset)

    #Admin
    @action(methods=['get'], detail=False)
    def in_use(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=3)
        return self._get_computer(queryset=queryset)

    #Admin
    @action(methods=['get'], detail=False)
    def maintenance(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=4)
        return self._get_computer(queryset=queryset)

    #Admin
    @action(methods=['put'], detail=True)
    def update_status(self, request, pk):
        computer = self.get_object()
        serializer = self.get_serializer(instance=computer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_200_OK)
        return Response({'detail': 'Queue status is not waiting.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_computer(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        data = {
            'count': count,
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    