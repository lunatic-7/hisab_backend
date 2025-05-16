# Updated Django URL Configuration for API

from django.urls import path
from . import views

urlpatterns = [
    # Person endpoints
    path('persons/', views.person_list_create, name='person-list-create'),
    path('persons/<int:pk>/', views.person_detail, name='person-detail'),  # New comprehensive endpoint
    path('persons/<int:pk>/delete/', views.delete_person, name='delete-person'),
    path('persons/<int:pk>/hisabs/', views.person_hisabs, name='person-hisabs'),
    
    # Hisab endpoints
    path('hisabs/', views.hisab_list_create, name='hisab-list-create'),
    path('hisabs/<int:pk>/', views.hisab_detail, name='hisab-detail'),
    path('hisabs/<int:pk>/delete/', views.delete_hisab, name='delete-hisab'),
    
    path('generate_hisab_pdf/', views.generate_hisab_pdf, name='generate_hisab_pdf'),
]