from django.urls import path

from . import views
from .views import DashboardView, AttendanceRegisterView, AttendanceSheetView, LoginView, LogoutView, \
    RegisterCoursesView, RegisteredCoursesView, RegisterView, ForgotPasswordView, UpdatePasswordView, CreateCourseView

app_name = 'Scanner'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('forgot_password', ForgotPasswordView.as_view(), name="forgot_password"),
    path('forgot-password/<int:user_id>/update-password', UpdatePasswordView.as_view(), name='update_password'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('create_course', CreateCourseView.as_view(), name="create_course"),
    path('course_registration', RegisterCoursesView.as_view(), name="register_courses"),
    path('course_registration/add_course', views.add_course, name="add_course"),
    path('course_registration/remove_course', views.remove_course, name="remove_course"),
    path('course_registration/registered_courses', RegisteredCoursesView.as_view(), name="registered_courses"),
    path('attendance', AttendanceRegisterView.as_view(), name="attendance_register"),
    path('attendance/take_attendance', views.take_attendance, name="take_attendance"),
    path('attendance/view', AttendanceSheetView.as_view(), name="attendance_sheet"),
]