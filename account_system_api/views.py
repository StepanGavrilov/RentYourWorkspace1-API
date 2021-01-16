from rest_framework import viewsets, status
from rest_framework.response import Response

from .base.classes import CreateUpdateDestroyListRetrieve

from .serializers import AccountCreateSerializer, AccountSerializer, AccountUpdateSerializer
from .serializers import Account

from .base.permissions import IsAccountOwner


class AccountAPI(CreateUpdateDestroyListRetrieve, viewsets.GenericViewSet):
    """
    CRUD Account
    """

    lookup_url_kwarg = 'id'
    permission_classes = (IsAccountOwner, )

    def get_object(self):
        try:
            account = Account.objects.get(id=self.kwargs['id'])
        except Account.DoesNotExist:
            return None
        return account

    def get_queryset(self):
        return Account.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        if self.action == 'list':
            return AccountSerializer
        if self.action == 'retrieve':
            return AccountSerializer
        if self.action == 'update':
            return AccountUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        post = serializer
        return Response({'Account': post.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
            print('Not none')
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.check_object_permissions(self.request, instance)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance is not None:
            self.check_object_permissions(self.request, instance)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)