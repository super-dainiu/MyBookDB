from django.urls import path
from . import views

urlpatterns = {
    path('', views.index),
    path('createbooks/', views.create),
    path('editbooks/<int:bookid>', views.edit),
}
