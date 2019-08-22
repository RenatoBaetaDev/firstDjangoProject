from django.shortcuts import render
from django.http import JsonResponse
from app.models import Post, Profile, Like
from django.contrib.auth.models import User
from datetime import datetime
from django.views import View
from django.core import serializers
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from app.forms import EditProfileForm, EditUserForm
from django.shortcuts import (
    get_object_or_404, redirect, render, HttpResponse
)


# Create your views here.

def index(request):
    return render(request, 'index.html')


class PostView(View):

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', None)

        data = {
            'message': 'Post Error trying to Save.'
        }    

        if text is not None:
            post = Post(text=text, author=request.user, timestamp = datetime.utcnow())
            post.save()
            data = {
                'message': 'Post Succesfully Saved.'
            }
        

        return JsonResponse(data)


    def get(self, request, *args, **kwargs):

        objects = Post.objects.annotate(likes=Count('postLikes')).values('author__profile__picture').order_by('-timestamp')

        json_data = json.dumps(list(objects), cls=DjangoJSONEncoder)

        # data = serializers.serialize('json', json_data)

        return JsonResponse(json_data, safe=False)

class UserProfile(View):
    template_name = 'users/user.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        profile = Profile.objects.filter(user=user).first()
        posts = Post.objects.filter(author=user)
        # following = request.user.is_following(user)
        return render(request, self.template_name, {
            'user': user,
            'profile': profile,
            'posts': posts,
            # 'following': following,
        })



class UserProfileEditAdmin(View):
    template_name = 'users/edit_user.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        profile = Profile.objects.filter(user=user).first()
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)
        args = {}
        args['user_form'] = user_form
        args['profile_form'] = profile_form
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        profile = Profile.objects.filter(user=user).first()
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('user', username=user.username)
        return render(request, self.template_name, args)


class LikeView(View):

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        user = request.POST.get('user', None)

        liked = Like.objects.filter(post_id=id, user_id=user)

        print(liked)

        if liked:
            liked.delete()
        else:
            like = Like(post=Post.objects.filter(id=id).first(), user=User.objects.filter(id=user).first())
            like.save()


        data = {
            'text' : 'text'
        }

        return JsonResponse(data)

