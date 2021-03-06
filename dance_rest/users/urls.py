from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('details/',
        views.ManageDetailsUserView.as_view({'get': 'retrieve'}),
        name='details'),
    path('create_details/',
        views.CreateDetailsUserView.as_view({'post': 'create'}),
        name='create_details'),
]
