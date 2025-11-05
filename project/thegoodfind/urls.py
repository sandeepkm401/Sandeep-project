from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.finder_detail, name='finder_detail'),
    path('searcher/', views.searcher, name='searcher'),
    path('finder/<int:pk>/', views.finder_detail, name='finder_detail'),
    path('finder/<int:pk>/contact/', views.finder_contact, name='finder_contact'),
]
