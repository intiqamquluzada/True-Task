from django.urls import path
from .views import my_profile


app_name = 'app'

urlpatterns = [

    path('profile/<slug>/', my_profile, name='profile')

]