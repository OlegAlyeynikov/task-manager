from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Task, Position, TaskType

WORKER_LIST_URL = reverse("task_manager:worker-list")
WORKER_DETAIL_URL = reverse("task_manager:worker-detail")


class PublicTaskTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            email="test@gmail.com",
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            position=self.position
        )
        self.task = Task.objects.create(
            name="Test",
            description="Research task str",
            created_at="2022-12-20",
            deadline="2022-12-29",
            status="In progress",
            priority="Urgent",
        )

    def test_worker_list_login_required(self):
        res = self.client.get(WORKER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_worker_tasks_login_required(self):
        res = self.client.get(WORKER_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test@gmail.com",
            "password123"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Test")
        self.position = Position.objects.create(name="Developer")
        self.task = Task.objects.create(
            name="Test",
            description="Research task str",
            created_at="2022-12-20",
            deadline="2022-12-29",
            status="In progress",
            priority="Urgent",
            task_type=self.task_type,
        )
        self.worker = get_user_model().objects.create_user(
            email="test_new@gmail.com",
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            position=self.position
        )

    def test_retrieve_workers(self):
        """Make sure the `task_manager/worker_list.html` template is used"""

        resp = self.client.get(WORKER_LIST_URL)
        workers = get_user_model().objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["worker_list"]),
            list(workers)
        )

        self.assertTemplateUsed(resp, "task_manager/worker_list.html")

    def test_retrieve_worker_tasks(self):
        """Make sure the `task_manager/worker_detail.html` template is used"""

        resp = self.client.get(WORKER_DETAIL_URL)
        tasks = Task.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["task_list"]),
            list(tasks)
        )

        self.assertTemplateUsed(resp, "task_manager/worker_detail.html")
