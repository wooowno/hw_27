from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('Z/', views.UserZListView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('<int:pk>/update/', views.UserUpdateView.as_view()),
    path('<int:pk>/delete/', views.UserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
