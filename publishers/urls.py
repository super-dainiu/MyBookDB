from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('createpublishers/', views.create),
    path('editpublishers/<int:publisherid>', views.edit),
]