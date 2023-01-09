from django.urls import path

from task_manager.views import (
    TaskListView,
    TaskDetailView,
    WorkerListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    toggle_assign_to_task,
    WorkerTaskDetailView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/worker-task-detail/",
        WorkerTaskDetailView.as_view(),
        name="worker-detail",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
]

app_name = "task_manager"
