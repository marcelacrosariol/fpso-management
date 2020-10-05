from django.http import JsonResponse

from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response 
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import (
    Equipment,
    Vessel
)

from .serializers import (
    EquipmentListSerializer,
    EquipmentVesselSerializer,
    VesselSerializer
)

from .filters import StatusSearchFilter


class VesselListApiView(ListAPIView):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer
    filter_backends =  [SearchFilter]
    search_fields =  ['code']


class VesselCreateApiView(CreateAPIView):
    queryset = Vessel.objects.all()
    serializer_class = VesselSerializer


class VesselEquipmentListApiView(ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentListSerializer
    filter_backends =  [StatusSearchFilter]
    search_fields =  ['status']

    def list(self, request, *args, **kwargs):
        try:
            vessel =Vessel.objects.get(code=kwargs.get('code'))
            self.queryset = self.queryset.filter(vessel=vessel)
        except (Vessel.DoesNotExist) as e:
            raise ValidationError(detail=e)
        return super(VesselEquipmentListApiView, self).list(request, *args, **kwargs)


class EquipmentCreateApiView(CreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentVesselSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'vessel_code': kwargs.get('code')}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class EquipmentStatusUpdateApiView(APIView):
    model = Equipment

    def get_equipment(self, code):
        try:
            return self.model.objects.get(code=code)
        except (self.model.DoesNotExist) as e:
            raise ValidationError(detail=e)

    def get_action(self, request):
        return 'deactivate' if 'deactivate' in request.get_full_path() else 'activate'

    def put(self, request, *args, **kwargs):
        eqp_code_list = request.data.get('codes')
        action = self.get_action(request)
        instances = []

        if not eqp_code_list:
            raise ValidationError(detail="Invalid Input.")

        for eqp_code in eqp_code_list:
            eqp = self.get_equipment(eqp_code)
            eqp.deactivate() if action == 'deactivate' else eqp.activate()
            instances.append(eqp)

        serializer = EquipmentListSerializer(instances, many=True)
 
        return Response(serializer.data, status=HTTP_200_OK)