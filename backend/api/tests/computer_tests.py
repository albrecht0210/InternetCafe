from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Computer
from ..serializers import ComputerSerializer, ComputerStatusUpdateSerializer

class ComputerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.computer_url = reverse('computer-list')
        self.available_url = reverse('computer-available')
        self.in_use_url = reverse('computer-in-use')
        self.maintenance_url = reverse('computer-maintenance')
        self.computer = Computer.objects.create(name='Test Computer')

    def test_get_computer_list(self):
        response = self.client.get(self.computer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_available_computers(self):
        response = self.client.get(self.available_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_computers_in_use(self):
        response = self.client.get(self.in_use_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_computers_under_maintenance(self):
        response = self.client.get(self.maintenance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_computer_status(self):
        update_status_url = reverse('computer-update-status', kwargs={'pk': self.computer.id})
        data = {'status': 2}  # Change status to 'In Use'
        response = self.client.put(update_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.computer.refresh_from_db()
        self.assertEqual(self.computer.status, 2)  # Status should be updated to 'In Use'

    def test_invalid_update_computer_status(self):
        update_status_url = reverse('computer-update-status', kwargs={'pk': self.computer.id})
        data = {'status': 5}  # Invalid status
        response = self.client.put(update_status_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
