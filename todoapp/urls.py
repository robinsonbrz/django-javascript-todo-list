from django import views
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (CustomLoginView, DeleteView, RegisterPage, TaskCreate,
                    TaskDetail, TaskList, TaskReorder, TaskUpdate)

app_name = 'todoapp'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='todoapp:login'), name='logout'), # noqa E501
    path('register/', RegisterPage.as_view(), name='register'),
    path('tasks', TaskList.as_view(), name='tasks'),
    # path('', views.Vazia, name='log'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]
