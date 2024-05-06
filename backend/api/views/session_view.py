from django.utils import timezone
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Session, Queue
from ..permissions import IsOwner
from ..serializers import SessionSerializer

class SessionViewSet(mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.DestroyModelMixin, 
                     viewsets.GenericViewSet):
    
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get_permissions(self):
        if self.action == ['my_all_session', 'my_session', 'create_session', 'end_session']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False)
    def create_session(self, request):
        user = self.request.user.id
        
        try:
            queue_entry = Queue.objects.get(account=user)
        except Queue.DoesNotExist:
            return Response({"error": "Queue entry not found"}, status=status.HTTP_404_NOT_FOUND)
        
        computer_id = request.data.get('computer')
        if not computer_id:
            return Response({"error": "Computer ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if queue_entry.computer.id != computer_id:
            return Response({"error": "Computer ID does not match queue entry"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['account'] = user

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queue_entry.computer.status = 3
            queue_entry.computer.save(update_fields=['status'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=True)
    def end_session(self, request):
        session = self.get_object()
        session.end_time = timezone.now()
        session.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def my_all_session(self, request, *args, **kwargs):
        user = self.request.user.id
        queryset = self.queryset.filter(account=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(methods=['get'], detail=False)
    def my_session(self, request, *args, **kwargs):
        user = self.request.user.id
        try:
            queryset = self.queryset.get(account=user)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({'details': 'No session.'}, status=status.HTTP_404_NOT_FOUND)
        
