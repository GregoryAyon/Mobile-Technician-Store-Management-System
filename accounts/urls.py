from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('logout', views.logoutUser, name='logout'),
    path('dashboard/<str:pk>/', views.dashboard, name='dashboard'),
    path('delete/<str:pk>/', views.delete_view, name='delete'),
    path('update/<str:pk>/', views.update_view, name='update'),
    path('views/<str:wm>', views.orders_view, name='views'),
]
