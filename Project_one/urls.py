"""
URL configuration for Project_one project.

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
from Reminder.views import Registerview,Loginview,Logout,Taskview,Profiledelete,Taskedit,Taskdelete,Updateprofile,Profileview
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/',Registerview.as_view(),name="register"),
    path("",Loginview.as_view(),name="login"),
    path("welcome/",Loginview.as_view(),name="welcome"),

    path("profile/",Profileview.as_view(),name="profile"),
    path("up/<int:pk>",Updateprofile.as_view(),name="update"),
    path("del/<int:pk>",Profiledelete.as_view(),name="prodelete"),
    path("index/",Taskview.as_view(),name="task"),
    path("index/edit/<int:pk>",Taskedit.as_view(),name="edit"),
    path("index/delete/<int:pdk>",Taskdelete.as_view(),name="delete"),
      path("logout/",Logout.as_view(),name="logout"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)