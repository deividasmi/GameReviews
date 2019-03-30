from django.urls import path
from .views import ReviewListView, ReviewDetailView, ReviewCreateView
from . import views


urlpatterns = [
    path('', ReviewListView.as_view(), name='reviews-home'),
    path('about/', views.about, name='reviews-about'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='reviews-detail'),
    path('review/new/', ReviewCreateView.as_view(), name='reviews-create'),
]