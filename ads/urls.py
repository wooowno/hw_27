from django.urls import path
from rest_framework import routers

from ads import views
from ads.views import CategoryViewSet

router = routers.SimpleRouter()
router.register('category', CategoryViewSet)

urlpatterns = [
    path('', views.AdListView.as_view()),
    path('create/', views.AdCreateView.as_view()),
    path('<int:pk>/', views.AdDetailView.as_view()),
    path('<int:pk>/update/', views.AdUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', views.AdImageView.as_view()),
]

urlpatterns += router.urls
