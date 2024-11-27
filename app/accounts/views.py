# accounts/views.py

import logging
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account
from .serializers import (
    AccountCreateSerializer,
    AccountDetailSerializer,
    AccountUpdateSerializer
)

logger = logging.getLogger(__name__)

class AccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling standard CRUD operations on Account model.
    Provides different serializers for different operations.
    """
    queryset = Account.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AccountUpdateSerializer
        return AccountDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Creating new account with username: {request.data.get('username')}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            
            response_serializer = AccountDetailSerializer(account)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            logger.error(f"Validation error during account creation: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during account creation: {str(e)}")
            return Response(
                {'error': 'Failed to create account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            logger.info(f"Updating account {kwargs.get('pk')}")
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            
            response_serializer = AccountDetailSerializer(account)
            return Response(response_serializer.data)
        except Exception as e:
            logger.error(f"Error updating account: {str(e)}")
            return Response(
                {'error': 'Failed to update account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        try:
            account = self.get_object()
            
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            if not all([current_password, new_password, confirm_password]):
                raise ValidationError('All password fields are required')

            if not account.check_password(current_password):
                raise ValidationError('Current password is incorrect')

            if new_password != confirm_password:
                raise ValidationError('New passwords do not match')

            account.set_password(new_password)
            account.save()

            return Response({'message': 'Password changed successfully'})
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            return Response(
                {'error': 'Failed to change password'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AccountSearchView(generics.ListAPIView):
    """
    Custom view for searching accounts with advanced filtering.
    """
    serializer_class = AccountDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Account.objects.all()
        search_term = self.request.query_params.get('search', None)

        if search_term:
            queryset = queryset.filter(
                models.Q(username__icontains=search_term) |
                models.Q(email__icontains=search_term) |
                models.Q(first_name__icontains=search_term) |
                models.Q(last_name__icontains=search_term)
            )

        return queryset.select_related()