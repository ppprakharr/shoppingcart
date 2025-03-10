from django.urls import path
from userauths import views

app_name='userauths'
urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/',views.login_view, name='sign-in'),
    path('sign-out/',views.logout_view, name='sign-out'),
    path('edit-profile',views.edit_profile_view,name='edit-profile'),
    path('contact/',views.contact_views,name='contact-us'),
]
