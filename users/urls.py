from django.urls import path
from . import views


urlpatterns = {
    path('', views.index),
    path('createuser/', views.create),
    path('edituser/<int:userid>', views.edit),
}