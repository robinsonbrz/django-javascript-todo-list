from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
# Create your views here.
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# Imports for Reordering Feature
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView

from .forms import PositionForm
from .models import Task

# def Vazia(request):
#     return render(request,'todoapp/login.html')


class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todoapp:tasks')


class RegisterPage(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todoapp:tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoapp:tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    redirect_to = 'todoapp:login'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    redirect_to = 'todoapp:login'
    model = Task
    context_object_name = 'task'
    template_name = 'todoapp/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    redirect_to = 'todoapp:login'
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('todoapp:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    redirect_to = 'todoapp:login'
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('todoapp:tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    redirect_to = 'todoapp:login'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('todoapp:tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('todoapp:tasks'))
