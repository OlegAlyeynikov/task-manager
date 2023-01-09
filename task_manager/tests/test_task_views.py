from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task_manager.models import Task, Position, TaskType

TASK_LIST_URL = reverse("task_manager:task-list")


class PublicTaskTests(TestCase):
    def setUp(self) -> None:
        self.task = Task.objects.create(
            name="Test",
            description="Research task str",
            created_at="2022-12-20",
            deadline="2022-12-29",
            status="In progress",
            priority="Urgent",
        )

    def test_tasks_list_login_required(self):
        res = self.client.get(TASK_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_task_detail_login_required(self):
        res = self.client.get(reverse('task_manager:task-detail', kwargs={'pk': self.task.pk}))

        self.assertNotEqual(res.status_code, 200)

    def test_task_create_login_required(self):
        res = self.client.get(reverse('task_manager:task-create'))

        self.assertNotEqual(res.status_code, 200)

    def test_task_update_login_required(self):
        res = self.client.get(reverse('task_manager:task-update', kwargs={'pk': self.task.pk}))

        self.assertNotEqual(res.status_code, 200)

    def test_task_delete_login_required(self):
        res = self.client.get(reverse('task_manager:task-delete', kwargs={'pk': self.task.pk}))

        self.assertNotEqual(res.status_code, 200)

    def test_user_assign_to_task_login_required(self):
        res = self.client.get(reverse('task_manager:toggle-task-assign', kwargs={'pk': self.task.pk}))

        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTests(TestCase):
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
        self.resp_detail = self.client.get(
            reverse('task_manager:task-detail', kwargs={'pk': self.task.pk})
        )

    def test_retrieve_tasks(self):
        """Make sure the `task_manager/task_list.html` template is used"""

        resp = self.client.get(TASK_LIST_URL)
        tasks = Task.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["task_list"]),
            list(tasks)
        )

        self.assertTemplateUsed(resp, "task_manager/task_list.html")

    def test_retrieve_task_detail(self,):
        """Make sure the `task_manager/task_detail.html` template is used"""

        self.assertEqual(self.resp_detail.status_code, 200)

        self.assertTemplateUsed(self.resp_detail, "task_manager/task_detail.html")

    def test_detail_template_task_type(self):
        """Make sure the task type's name is in the rendered output"""

        self.assertContains(self.resp_detail, self.task.task_type.name)
