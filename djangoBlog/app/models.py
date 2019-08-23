import hashlib
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=64, blank=True)
    picture = models.ImageField(upload_to='blog/%Y/%m/%d')


class Post(models.Model):
    __tablename__ = 'posts'
    text = models.TextField( )
    timestamp = models.DateTimeField(default=datetime.utcnow)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.utcnow)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postLikes')
    created = models.DateTimeField(auto_now_add=True)

class UserFunctions:
    @property
    def gravatar(self, size=40, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}:s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def follow(self, user):
        follower_profile = Profile.objects.filter(user=self).first()
        followed_profile = Profile.objects.filter(user=user).first()
        relationship, created = Follow.objects.get_or_create(
            follower=follower_profile,
            followed=followed_profile
        )
        return relationship

    def unfollow(self, user):
        follower_profile = Profile.objects.filter(user=self).first()
        followed_profile = Profile.objects.filter(user=user).first()
        Follow.objects.filter(
            follower=follower_profile,
            followed=followed_profile).delete()
        return

    def is_following(self, user):
        if user.id is None:
            return False
        follower_profile = Profile.objects.filter(user=self).first()
        followed_profile = Profile.objects.filter(user=user).first()
        return Follow.objects.filter(
            follower=follower_profile,
            followed=followed_profile
        ).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter(
            follower_id=user.id).first() is not None

    def follows(self):
        profile = Profile.objects.filter(user=self).first()
        followeds = profile.follower.all()
        users = [i.followed.user for i in followeds]
        return users

    def followed_posts(self):
        return Post.objects.filter(author__in=self.follows())


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    followed = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='followed'
    )
