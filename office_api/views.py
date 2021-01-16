from django.db.models import Q
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from .base.classes import CreateUpdateDestroyListRetrieve

from .models import Reservation, Office
from .serializers import OfficeSerializer, OfficeUpdateSerializer, ReservationSerializer, \
    ReservationCreateUpdateSerializer, OfficeReservationSerializer


class OfficeAPI(CreateUpdateDestroyListRetrieve, viewsets.GenericViewSet):
    """
    CRUD Office
    """

    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.action == 'update':
            return OfficeUpdateSerializer
        if self.action == 'retrieve':
            return OfficeReservationSerializer
        else:
            return OfficeSerializer

    def get_object(self):
        try:
            office = Office.objects.get(id=self.kwargs['id'])
        except Office.DoesNotExist:
            return None
        return office

    def get_queryset(self):
        return Office.objects.all()

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        office = serializer
        return Response({'Office': office.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is not None:
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


class FreeOfficeView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Free workspaces
    """

    def list(self, request, *args, **kwargs) -> Response:
        try:
            datetime_from = self.request.data['datetime_from']
            datetime_to = self.request.data['datetime_to']
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        time = Office.objects.prefetch_related(
            'reservation').exclude(
            Q(reservation__datetime_from__range=(datetime_from, datetime_to)) | Q(
                reservation__datetime_to__range=(datetime_to, datetime_to))
        ).exclude(
            reservation__datetime_from__lte=datetime_from,
            reservation__datetime_to__gte=datetime_to
        ).exclude(
            reservation__datetime_from__lte=datetime_to,
            reservation__datetime_to__gte=datetime_from
        )
        serializer = OfficeReservationSerializer(time, many=True)
        return Response(serializer.data)


class ReservationAPI(CreateUpdateDestroyListRetrieve, viewsets.GenericViewSet):
    """
    CRUD Reservation
    """

    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateUpdateSerializer
        if self.action == 'list':
            return ReservationSerializer
        if self.action == 'retrieve':
            return ReservationSerializer
        if self.action == 'update':
            return ReservationCreateUpdateSerializer
        if self.action == 'destroy':
            return ReservationSerializer

    def get_object(self):
        try:
            reservation = Reservation.objects.get(id=self.kwargs['id'])
        except Reservation.DoesNotExist:
            return None
        return reservation

    def get_queryset(self) -> Reservation:
        # TODO CHECK JOIN
        return Reservation.objects.select_related().all()

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer) -> None:
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        reservation = serializer
        return Response({'reservation': reservation.data})

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if not isinstance(instance, Reservation):
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
