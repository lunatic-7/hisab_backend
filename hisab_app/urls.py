# Updated Django URL Configuration for API

from django.urls import path
from . import views

urlpatterns = [
    # Person endpoints
    path('persons/', views.person_list_create, name='person-list-create'), # person create krne ke aur dkhne ke liye
    path('persons/<int:pk>/', views.person_detail, name='person-detail'),
    # path('persons/<int:pk>/delete/', views.delete_person, name='delete-person'),
    path('persons/<int:pk>/hisabs/', views.person_hisabs, name='person-hisabs'), # person ka hisab dekhne ke liye
    
    # Hisab endpoints
    path('hisabs/', views.hisab_list_create, name='hisab-list-create'), #  hisab create krne ke liye
    path('hisabs/<int:pk>/', views.hisab_detail, name='hisab-detail'),
    path('hisabs/<int:pk>/delete/', views.delete_hisab, name='delete-hisab'), # hisab delete krne ke liye
    
    path('generate_hisab_pdf/', views.generate_hisab_pdf, name='generate_hisab_pdf'), # pdf ke liye
]

