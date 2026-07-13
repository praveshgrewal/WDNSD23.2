from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # User management
    path('add-user/', views.add_user, name='add_user'),
    path('users/', views.user_list, name='user_list'),
    path('user/<int:employee_id>/', views.user_detail, name='user_detail'),

    # Face capture
    path('capture/<int:employee_id>/', views.capture_faces, name='capture_faces'),
    path('api/capture/<int:employee_id>/', views.capture_frame, name='capture_frame'),

    # Model training
    path('train/', views.train_view, name='train'),
    path('api/train/', views.train_model_api, name='train_model_api'),

    # Attendance
    path('mark-attendance/', views.mark_attendance_view, name='mark_attendance'),
    path('api/recognize/', views.recognize_face_api, name='recognize_face_api'),
    path('api/manual-attendance/', views.manual_attendance_api, name='manual_attendance_api'),
    path('attendance/', views.attendance_list, name='attendance_list'),
]
