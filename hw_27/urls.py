from django.contrib import admin
from django.urls import path

from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('cat/', views.CategoryViews.as_view()),
    path('ad/', views.AdViews.as_view()),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),
    path('ad/<int:pk>/', views.AdDetailView.as_view()),
]
