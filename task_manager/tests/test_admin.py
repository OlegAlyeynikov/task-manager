from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@admin.iu",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(
            name="Test Position"
        )
        self.worker = get_user_model().objects.create_user(
            email="worker@worker.iu",
            password="worker123",
            position=position
        )

    def test_worker_position_listed(self):
        """Tests that worker's position is in list_display on admin page"""
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)

    def test_worker_detailed_position_listed(self):
        """Tests that worker's position is on worker detail admin page"""
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)
