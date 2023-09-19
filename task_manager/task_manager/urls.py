"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('addTask/', addTask, name="addTask"),
    path('editTask/', editTask, name="editTask"),
    path('deleteTask/', deleteTask, name="deleteTask"),
    path('', viewTask, name="viewTask"),
    path('complete_task/', complete_task, name="complete_task"),
    path('delete_task/', delete_task, name="delete_task"),
    path('get_task_details/<int:task_id>/', get_task_details, name="get_task_details"),
    path('update_task/<int:task_id>/', update_task, name="update_task"),
    path('login/', loginUser, name="loginUser"),
    path('signup/', signupUser, name="signupUser"),
    path('logout/', logoutUser, name="logoutUser"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
