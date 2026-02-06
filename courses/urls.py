from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:id>/', views.course_detail, name='course'),
    path('buy/<int:course_id>/', views.buy_course, name='buy_course'),
    path('course/<int:course_id>/modules/', views.course_modules, name='course_modules'),
    path('module/<int:module_id>/watch/', views.watch_module, name='watch_module'),
    path('course/<int:course_id>/review/', views.add_review, name='add_review'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
]

