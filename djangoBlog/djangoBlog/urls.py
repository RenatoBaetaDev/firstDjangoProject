"""djangoBlog URL Configuration

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
from django.urls import path
from app.views import index, PostView, UserProfile, UserProfileEditAdmin, LikeView, CommentView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('post_save/', PostView.as_view(), name="post_save"),
    path('get_posts/', PostView.as_view(), name="get_posts"),
    path('comment_post/', CommentView.as_view(), name="comment_post"),
    path('get_comments/', CommentView.as_view(), name="get_comments"),
    path('user/<str:username>/', UserProfile.as_view(), name='user'),
    path(
        'user/<str:username>/edit', UserProfileEditAdmin.as_view(),
        name='edit_profile_admin'
    ),
    path('like_post/', LikeView.as_view(), name="like_post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


