from django.urls import path
from .import views

urlpatterns = [
    path('', views.ProgramList.as_view(), name='program_list'),
    path('<str:program_id>/', views.ProgramDetail.as_view(), name='program_detail'),
    path('access_token/<str:program_id>/', views.access_token, name='access_token')
]
