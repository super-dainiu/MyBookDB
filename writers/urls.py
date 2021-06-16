from django.urls import path
from . import views


urlpatterns = {
    path('', views.index),
    path('createwriter/', views.create),
    path('editwriters/<int:writerid>', views.edit)
}