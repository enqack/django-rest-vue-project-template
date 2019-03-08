from django.urls import include, path

from . import views


app_name = 'custom_auth'

urlpatterns = [
    path('account/new/', views.UserCreateView.as_view(), name='account_create'),
    path('account/<int:pk>', views.UserDetailView.as_view(), name='account_detail'),
    path('account/<int:pk>/edit', views.UserUpdateView.as_view(), name='account_edit'),
    path('account/list/', views.UserListView.as_view(), name='account_list'),
    path('profile/', views.UserProfileView.as_view(), name='account_profile'),
]
