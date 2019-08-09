from random import randint
from faker import Faker

from django.contrib.auth.models import User

from .models import Profile, Post


def users(count=50):
    fake = Faker()
    i = 0
    while i < count:
        u = User(
            email=fake.email(),
            username=fake.user_name(),
            password='password',
            first_name=fake.name(),
        )
        u.save()
        p = Profile(
            user=u,
            about_me=fake.text()
        )
        p.save()
        i += 1


def posts(count=500):
    fake = Faker()
    user_count = User.objects.count()
    for i in range(count):
        u = User.objects.get(id=randint(0, user_count - 1))
        p = Post(
            body=fake.text(),
            timestamp=fake.past_date(),
            author=u
        )
        p.save()
