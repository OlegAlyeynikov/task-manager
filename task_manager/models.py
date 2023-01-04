from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext as _


class TaskType(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=70)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Worker(AbstractUser):
    position = models.ForeignKey(Position, null=True, on_delete=SET_NULL)
    username = models.CharField(max_length=69, null=True, unique=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.position}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("Not started", "Task not started"),
        ("In progress", "Task in progress"),
        ("On review", "Task on review"),
        ("Completed", "Task completed"),
    ]
    PRIORITY_CHOICES = [
        ("No priority", "No priority"),
        ("Low", "Low priority"),
        ("Normal", "Normal priority"),
        ("Urgent", "Urgent priority"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_at = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=70, choices=STATUS_CHOICES, default="Not started"
    )
    priority = models.CharField(
        max_length=70, choices=PRIORITY_CHOICES, default="No priority"
    )
    task_type = models.ForeignKey(TaskType, null=True, on_delete=SET_NULL)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return f"{self.name} {self.deadline} {self.status} {self.priority}"
