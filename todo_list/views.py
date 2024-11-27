from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic

from todo_list.forms import TaskForm
from todo_list.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    queryset = (
        Task.objects.order_by("is_done", "-datetime").prefetch_related("tags")
    )
    paginate_by = 5


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo_list:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse("todo_list:task-detail", kwargs={"pk": self.object.id})


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todo_list:task-list")


class TaskChangeStatusView(generic.View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs["pk"])
        task.is_done = not task.is_done
        task.save()
        return redirect("todo_list:task-list")


class TagListView(generic.ListView):
    model = Tag
    paginate_by = 5


class TagCreateView(generic.CreateView):
    model = Tag
    fields = [
        "name",
    ]
    success_url = reverse_lazy("todo_list:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = [
        "name",
    ]
    success_url = reverse_lazy("todo_list:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("todo_list:tag-list")
