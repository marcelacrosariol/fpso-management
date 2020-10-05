from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)

from rest_framework.validators import UniqueValidator

from . import models


class VesselSerializer(ModelSerializer):
    class Meta:
        model =  models.Vessel
        fields = ('code',)


class EquipmentListSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model =  models.Equipment
        fields = (
            'name',
            'code',
            'location',
            'status',
        )
    
    def get_status(self, obj):
        return obj.get_status()


class EquipmentVesselSerializer(ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = ('name', 'code', 'location')
    
    def create(self, validated_data):
        vessel_code = self.context.get('vessel_code')
        vessel = models.Vessel.objects.get(code=vessel_code)
        equipment = self.Meta.model.objects.create(vessel=vessel, **validated_data)
        return equipment


class EquipmentStatusListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        equipment_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        print(equipment_mapping, data_mapping)

        # Perform creations and updates.
        ret = []
  

        return ret

class EquipmentStatusSerializer(Serializer):
    code = CharField()

    class Meta:
        list_serializer_class = EquipmentStatusListSerializer