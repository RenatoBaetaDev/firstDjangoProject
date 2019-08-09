import hashlib
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.gis.forms import widgets
from django.db import models


class UserFunctions:
    def gravatar(self, size=100, default='identicon', rating='g'):
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


User.__bases__ += (UserFunctions,)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=64, blank=True)
    relationships = models.ManyToManyField(
        'self',
        related_name='related_to',
        symmetrical=False,
        blank=True,
        through='Follow'
    )


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


class Post(models.Model):
    __tablename__ = 'posts'
    body = models.TextField(
        help_text="O que você está pensando?",
    )
    timestamp = models.DateTimeField(default=datetime.utcnow)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
