from django.urls import path
from . import views

urlpatterns = [
    # API endpoints (keep your existing ones)
    path('api/', views.api_root, name='api_root'),
    path('api/register/', views.register_user, name='register_user'),
    path('api/authenticate/', views.authenticate_user, name='authenticate_user'),
    path('api/capture-face/', views.capture_face_encoding, name='capture_face'),
    path('api/profile/', views.get_user_profile, name='get_profile'),
    path('api/access-logs/', views.get_access_logs, name='access_logs'),
    path('api/visitor-logs/', views.get_visitor_logs, name='visitor_logs'),
    path('api/security-areas/', views.get_security_areas, name='security_areas'),
    path('api/create-admin/', views.create_admin_user, name='create_admin'),

    # Template views (ADD THESE)
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_page, name='profile_page'),
    path('logout/', views.logout_view, name='logout'),
]
