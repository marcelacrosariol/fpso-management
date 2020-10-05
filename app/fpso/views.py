from django.http import JsonResponse

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response 
from rest_framework.views import APIView

from . import models, serializers


class VesselListApiView(ListAPIView):
    queryset = models.Vessel.objects.all()
    serializer_class = serializers.VesselSerializer
    filter_backends =  [SearchFilter]
    search_fields =  ['code']


class VesselCreateApiView(CreateAPIView):
    queryset = models.Vessel.objects.all()
    serializer_class = serializers.VesselSerializer


class VesselEquipmentListApiView(ListAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = serializers.EquipmentListSerializer

    def list(self, request, *args, **kwargs):
        kw_status = kwargs.get('status')
        self.queryset = self.queryset.filter(vessel__code=kwargs.get('code'))

        if kw_status:
            status_selected = models.Equipment.get_status_options(kw_status)
            if status_selected is None:
                raise NotFound(detail="Page not found.", code=404)
            self.queryset = self.queryset.filter(status=status_selected)

        return super(VesselEquipmentListApiView, self).list(request, *args, **kwargs)


class EquipmentCreateApiView(CreateAPIView):
    queryset = models.Equipment.objects.all()
    serializer_class = serializers.EquipmentVesselSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'vessel_code': kwargs.get('code')}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EquipmentStatusUpdateApiView(APIView):
    model = models.Equipment

    def get_equipment(self, code):
        try:
            return self.model.objects.get(code=code)
        except (self.model.DoesNotExist) as e:
            raise ValidationError(detail=e)

    def get_action(self, request):
        return 'activate' if request.get_full_path() else 'deactivate'

    def put(self, request, *args, **kwargs):
        eqp_code_list = request.data.get('codes')
        action = self.get_action(request)
        instances = []

        if not eqp_code_list:
            raise ValidationError(detail="Invalid Input.")

        for eqp_code in eqp_code_list:
            eqp = self.get_equipment(eqp_code)
            eqp.activate() if action == 'deactivate' else eqp.deactivate()
            instances.append(eqp)

        serializer = serializers.EquipmentListSerializer(instances, many=True)
 
        return Response(serializer.data, status=status.HTTP_200_OK)