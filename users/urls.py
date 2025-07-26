from django.urls import path

from users.views import UserCreationView, EditProfileView, ProfileLogoutView, ProfileLoginView

urlpatterns = [
	path('register/', UserCreationView.as_view(), name='register'),
	path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
	path('login/', ProfileLoginView.as_view(), name='login'),
	path('logout/', ProfileLogoutView.as_view(), name='logout'),
]