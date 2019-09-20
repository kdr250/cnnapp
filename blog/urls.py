"""cnnapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, LabelListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('<int:pk>', PostDetailView.as_view(), name='blog-detail'),
    path('create', PostCreateView.as_view(), name='blog-create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='blog-update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='blog-delete'),
    path('about/', views.about, name='blog-about'),
    path('cnn/', views.cnn, name='about-cnn'),
    path('cifar/', views.cifar, name='about-cifar'),
    path('label/<str:label>', LabelListView.as_view(), name='label-list'),
]
