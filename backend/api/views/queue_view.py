from django.db import transaction
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Queue, Computer
from ..serializers import QueueSerializer, QueueStatusUpdateSerializer
from ..permissions import IsOwner

class QueueViewSet(mixins.ListModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.DestroyModelMixin, 
                   viewsets.GenericViewSet):
    
    serializer_class = QueueSerializer
    queryset = Queue.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'destroy', 'retrieve', 'waiting']:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        elif self.action == 'get_queue_number':
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action == 'now_serving':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['update_to_now_serving']:
            return QueueStatusUpdateSerializer
        return QueueSerializer
    
    # Admin
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self._get_queue(queryset=queryset)
    
    # Admin
    @action(methods=['post'], detail=False)
    def next_queue(self, request):
        with transaction.atomic():
            computer_pending_entry = Computer.objects.filter(status=2).first()
            
            if computer_pending_entry:

                queue_now_entry = Queue.objects.filter(computer=computer_pending_entry.id).first()
                queue_waiting_entry = Queue.objects.filter(status=1).first()
                computer = queue_now_entry.computer
                
                # serve queue_waiting_entry queue
                if queue_waiting_entry:
                    queue_waiting_entry.status = 2 
                    queue_waiting_entry.computer = computer
                    queue_waiting_entry.save(update_fields=['status', 'computer'])
                    computer.status = 2
                    computer.save(update_fields=['status'])

                # delete queue_now_entry queue
                if queue_now_entry:
                    queue_now_entry.delete()
                return Response({}, status=status.HTTP_200_OK)
        return Response({'detail': 'No computer pending now.'}, status=status.HTTP_200_OK)
    
    # User
    @action(methods=['post'], detail=False)
    def queue_computer(self, request, *args, **kwargs):
        # Make Data
        user = self.request.user.id
        data = { 'account': user }
        serializer = self.get_serializer(data=data)

        # Check if data is bvalid
        if serializer.is_valid():
            with transaction.atomic():
                # Save data
                queue_entry = serializer.save()
                # Get an available computer
                computer_entry = Computer.objects.filter(status=1).first()
                # computer is available
                if computer_entry:
                    # update queue status to now serving
                    # update queue computer to computer entry
                    queue_entry.status = 2
                    queue_entry.computer = computer_entry
                    queue_entry.save(update_fields=['status', 'computer'])

                    # update computer status to pending
                    computer_entry.status = 2
                    computer_entry.save(update_fields=['status'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # User
    @action(methods=['post'], detail=False)
    def dequeue_computer(self, request, *args, **kwargs):
        user = self.request.user.id
        try:
            with transaction.atomic():
                # get queue entry of the user
                queue_entry = Queue.objects.get(account=user)
                computer = queue_entry.computer
                
                # get the queue entry of next queue waiting
                next_queue_entry = Queue.objects.filter(status=1).first()
                
                # if next queue entry has value
                if next_queue_entry:
                    # update status and computer values
                    next_queue_entry.status = 2 
                    next_queue_entry.computer = computer
                    next_queue_entry.save(update_fields=['status', 'computer'])
                    computer.status = 2
                    computer.save(update_fields=['status'])
                else:
                    # if not update the computer status to available
                    computer.status = 1
                    computer.save(update_fields=['status'])
                # delete the queue entry
                queue_entry.delete()
            return Response({}, status=status.HTTP_200_OK)
        except Queue.DoesNotExist:
            return Response({'error': 'User is not in the queue'}, status=status.HTTP_404_NOT_FOUND)

    # User
    @action(methods=['get'], detail=False)
    def get_queue_number(self, request, *args, **kwargs):
        user = self.request.user.id
        try:
            queryset = self.queryset.get(account=user)
            serializer = self.get_serializer(instance=queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Queue.DoesNotExist:
            return Response({'details': 'No queue.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Admin
    @action(methods=['get'], detail=False)
    def waiting(self, request):
        queryset = self.queryset.filter(status=1)
        return self._get_queue(queryset=queryset)

    # Auth, No Auth
    @action(methods=['get'], detail=False)
    def now_serving(self, request):
        queryset = self.queryset.filter(status=2)
        return self._get_queue(queryset=queryset)
    
    def _get_queue(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        data = {
            'count': count,
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
