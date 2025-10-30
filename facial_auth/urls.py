from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('register/', views.register_user, name='register'),
    path('authenticate/', views.authenticate_user, name='authenticate'),
    path('capture-face/', views.capture_face_encoding, name='capture_face'),
    path('profile/', views.get_user_profile, name='profile'),
    path('access-logs/', views.get_access_logs, name='access_logs'),
    path('visitor-logs/', views.get_visitor_logs, name='visitor_logs'),
    path('security-areas/', views.get_security_areas, name='security_areas'),
    path('create-admin/', views.create_admin_user, name='create_admin'),
]
