from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View

from task_manager.forms import TaskForm, TaskSearchForm
from task_manager.models import Task, Worker
from django.contrib import messages


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("account_login")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 40
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    queryset = Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class WorkerTaskDetailView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 40
    template_name = "task_manager/worker_detail.html"
    context_object_name = "task_list"
    queryset = Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerTaskDetailView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task_list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task_list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task_list")
    template_name = "task_manager/task_confirm_delete.html"


@login_required
def toggle_assign_to_task(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if Task.objects.get(id=pk) in worker.tasks.all():
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "task_manager/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 40
    queryset = Worker.objects.all()


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
