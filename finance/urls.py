from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('update-income/', views.update_income, name='update_income'),
    path('update-expense/', views.update_expense, name='update_expense'),
    path('delete-income/', views.delete_income, name='delete_income'),
    path('delete-expense/', views.delete_expense, name='delete_expense'),
    path('charts/', views.generate_charts, name='charts'),
] 