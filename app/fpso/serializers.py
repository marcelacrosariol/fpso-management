from rest_framework.exceptions import ValidationError

from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    Serializer,
    CharField,
    SerializerMethodField,
)

from rest_framework.validators import UniqueValidator

from .models import Equipment, Vessel


class VesselSerializer(ModelSerializer):
    class Meta:
        model =  Vessel
        fields = ('code',)

    def validate_code(self, value):
        if not value.isalnum():
            raise ValidationError(detail='Code must be alphanumeric.')
        return value


class EquipmentListSerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model =  Equipment
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
        model = Equipment
        fields = ('name', 'code', 'location')

    def validate_code(self, value):
        if not value.isalnum():
            raise ValidationError(detail='Code must be alphanumeric.')
        return value
    
    def create(self, validated_data):
        vessel_code = self.context.get('vessel_code')
        try:
            vessel = Vessel.objects.get(code=vessel_code)
            equipment = self.Meta.model.objects.create(vessel=vessel, **validated_data)
            return equipment
        except (Vessel.DoesNotExist) as e:
            raise ValidationError(detail=e)
