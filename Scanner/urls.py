from django.urls import path

from Scanner import views
from Scanner.views import HomeView, LoginView, RegisterView

app_name = "Scanner"

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('home', HomeView.as_view(), name="home"),
    path('logout', views.logout, name="logout"),
]