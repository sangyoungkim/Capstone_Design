from django.urls import path
from CapstoneApp import views


urlpatterns = [
  path('',views.index, name="index"),
  path('<id>', views.html),
]
