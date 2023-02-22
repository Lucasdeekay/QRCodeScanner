from django.urls import path

from Scanner import views
from Scanner.views import HomeView, LoginView, RegisterView, AboutView, ContactView

app_name = "Scanner"

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('home', HomeView.as_view(), name="home"),
    path('about', AboutView.as_view(), name="about"),
    path('contact', ContactView.as_view(), name="contact"),
    path('scan', views.scan_code, name="scan_code"),
]