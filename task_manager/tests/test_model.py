from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import TaskType, Position, Task


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")

        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position.objects.create(name="Developer")

        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        position = Position.objects.create(name="Developer")
        worker = get_user_model().objects.create_user(
            email="test@gmail.com",
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last",
            position=position
        )
        self.assertEqual(str(worker), f"{worker.first_name} {worker.last_name} {position}")

    def test_task_str(self):
        task = Task.objects.create(
            name="Test",
            description="Research task str",
            created_at="2022-12-20",
            deadline="2022-12-29",
            status="In progress",
            priority="Urgent",
        )

        self.assertEqual(str(task), f"{task.name} {task.deadline} {task.status} {task.priority}")

    def test_create_task_with_position(self):
        position = Position.objects.create(name="Developer")
        email = "test@gmail.com"
        username = "test"
        password = "test12345"
        position = position
        worker = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            position=position
        )

        self.assertEqual(worker.email, email)
        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)
