from django.test import TestCase

from rest_framework.test import APITestCase
from django.urls import reverse

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST
)

from .models import Equipment, Vessel


class VesselTestCase(APITestCase):
    def setUp(self):
        self.list_url = 'vessel_list'
        self.create_url = 'vessel_create'

        self.valid_payload = {'code': 'MV001'}
        self.long_code_payload = {'code': 'MV2200000011'}
        self.invalid_payload = {'code': '@@@44444'}
        self.empty_payload = {}
        self.empty_code_payload = {}

    def test_vessel_list(self): 
        response = self.client.get(
            reverse(self.list_url)
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_valid_create_vessel(self):
        response = self.client.post(
            reverse(self.create_url),
            self.valid_payload
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_empty_create_vessel(self):
        response = self.client.post(
            reverse(self.create_url),
            self.empty_payload
        )
        self.assertEqual(response.status_code,HTTP_400_BAD_REQUEST)
    
    def test_empty_code_create_vessel(self):
        response = self.client.post(
            reverse(self.create_url),
            self.empty_code_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_long_code_create_vessel(self):
        response = self.client.post(
            reverse(self.create_url),
            self.long_code_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_invalid_code_create_vessel(self):
        response = self.client.post(
            reverse(self.create_url),
            self.invalid_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
    

class VesselEquipmentTestCase(APITestCase):
    def setUp(self):
        self.list_url = 'vessel_equipment_list'
        self.register_url = 'vessel_equipment_register'

        self.vessel = Vessel.objects.create(code='MV100')

        self.valid_payload = {
            'name': 'compressor',
            'code': '5310B9D7',
            'location': 'Brazil'
        }
        self.empty_payload = {}
        self.missing_payload = {
            'name': 'compressor',
            'code': '5310B9D7'
        }

    def test_valid_vessel_eqp_list(self):
        response = self.client.get(
            reverse(self.list_url, args=[self.vessel.code])
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_invalid_vessel_eqp_list(self):
        response = self.client.get(
            reverse(self.list_url, args=['MV002'])
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_valid_vessel_eqp_register(self):
        response = self.client.post(
            reverse(self.register_url, args=[self.vessel.code]),
            self.valid_payload
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_invalid_vessel_eqp_register(self):
        response = self.client.post(
            reverse(self.register_url, args=['MV002']),
            self.valid_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_empty_vessel_eqp_register(self):
        response = self.client.post(
            reverse(self.register_url, args=[self.vessel.code]),
            self.empty_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_missing_vessel_eqp_register(self):
        response = self.client.post(
            reverse(self.register_url, args=[self.vessel.code]),
            self.missing_payload
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
