from django.urls import path
from useradmin import views

app_name='useradmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]


