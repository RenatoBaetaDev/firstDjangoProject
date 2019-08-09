"""djangoblog URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from app.views import (
    PostCreate, PostUpdate, users, UserProfile, post, UserProfileEditAdmin,
    UserFollow, UserUnfollow, Index, index_all, index_followed
)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('index-all', index_all, name='index-all'),
    path('index-follow', index_followed, name='index-followed'),
    path('post/add/', PostCreate.as_view(), name='author-add'),
    path('post/<int:id>/', post, name='post'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', users, name='users'),
    path('user/<str:username>/', UserProfile.as_view(), name='user'),
    path(
        'user/<str:username>/edit', UserProfileEditAdmin.as_view(),
        name='edit_profile_admin'
    ),
    path(
        'user/<str:follower>/follows/<str:followed>/', UserFollow.as_view(),
        name='follow'
    ),
    path(
        'user/<str:follower>/unfollows/<str:followed>/',
        UserUnfollow.as_view(), name='unfollow'
    ),
    path(
        'user/<str:username>/followers/',
        UserProfile.as_view(), name='followers'
    ),
]
