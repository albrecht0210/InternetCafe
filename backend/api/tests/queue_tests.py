from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Queue, Account, Computer
from ..serializers import QueueSerializer, QueueStatusUpdateSerializer

class QueueAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.queue_url = reverse('queue-list')
        self.waiting_url = reverse('queue-waiting')
        self.now_serving_url = reverse('queue-now-serving')
        self.account = Account.objects.create(username='testuser')
        self.computer = Computer.objects.create(name='Test Computer')

    def test_get_queue_list(self):
        response = self.client.get(self.queue_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_waiting_queue(self):
        response = self.client.get(self.waiting_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_now_serving_queue(self):
        response = self.client.get(self.now_serving_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_queue_computer(self):
        self.client.force_login(self.account)
        response = self.client.post(reverse('queue-queue-computer'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dequeue_computer(self):
        self.client.force_login(self.account)
        response = self.client.post(reverse('queue-dequeue-computer'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_queue_number(self):
        self.client.force_login(self.account)
        response = self.client.get(reverse('queue-get-queue-number'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Assuming user doesn't have a queue number

    def test_waiting_action(self):
        response = self.client.get(reverse('queue-waiting'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_now_serving_action(self):
        response = self.client.get(reverse('queue-now-serving'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more tests as needed
