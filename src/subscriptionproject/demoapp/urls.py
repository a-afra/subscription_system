from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('my_account/', views.my_account, name="my_account"),
    path('login/', views.login, name="login"),
    path('plan_item/<int:pk>', views.display_plan_item, name="plan_item"),
]