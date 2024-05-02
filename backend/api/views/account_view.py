from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..permissions import IsProfileOwner, IsOwner
from ..serializers import AccountSerializer, AccountUpdateSerializer, AccountUpdatePasswordSerializer

Account = get_user_model()

class AccountRegister(generics.CreateAPIView):
    serializer_class = AccountSerializer

class AccountViewSet(mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin, 
                     mixins.ListModelMixin, 
                     viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # def get_serializer_class(self):
    #     if self.action == 'update':
    #         return AccountUpdateSerializer
    #     elif self.action == 'update_password':
    #         return AccountUpdatePasswordSerializer
    #     return AccountSerializer

    def get_permissions(self):
        if self.action == 'profile':
            permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
        else:
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    # Admin
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': count,
            'results': serializer.data
        }
        return Response(data)

    # User
    @action(methods=['get'], detail=False)
    def profile(self, request):
        return Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)
    
    # Admin
    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['put'], detail=True)
    # def update_password(self, request):
    #     account = self.get_object()
    #     serializer = self.get_serializer(instance=account, data=request.data, user=account)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    