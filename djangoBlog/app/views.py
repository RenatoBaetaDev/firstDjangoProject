from django.shortcuts import render
from django.http import JsonResponse
from app.models import Post, Profile, Like, Comment
from django.contrib.auth.models import User
from datetime import datetime
from django.views import View
from django.core import serializers
from django.db.models import Count, Case, When, Value, IntegerField, Q
from django.core.serializers.json import DjangoJSONEncoder
import json
from app.forms import EditProfileForm, EditUserForm
from django.shortcuts import (
    get_object_or_404, redirect, render, HttpResponse
)
from django.contrib.auth import logout


# Create your views here.

def index(request):
    return render(request, 'index.html')


def userLogout(request):
    logout(request)
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

        # qs2 = Offer.objects.select_related('subscription').extra(
        #     select={'monthly_fee': 'mobile_subscription.monthly_fee'})

        user = User.objects.filter(id=request.user.id).first()

        print(user)
        objects = Post.objects.annotate(likes=Count('postLikes')) \
            .annotate(comment_count=Count('comments')) \
            .annotate(hasComments=Case(When(comment_count=0, then=Value(False)), default=Value(True), output_field=IntegerField())) \
            .annotate(like_count=Count('postLikes', filter=Q(postLikes__user=user))) \
            .annotate(iveLiked=Case(When(like_count=0, then=Value(False)), default=Value(True), output_field=IntegerField())) \
            .values('id','text','timestamp','likes','author__profile__picture', 'hasComments', 'iveLiked').order_by('-timestamp')

        json_data = json.dumps(list(objects), cls=DjangoJSONEncoder)

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
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form = user_form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('user', username=user.username)

        context = {}
        for var in args:
            context[var] = var
        return render(request, self.template_name, context)


class LikeView(View):

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id', None)
        user = request.POST.get('user', None)

        liked = Like.objects.filter(post=id, user=user)

        if liked:
            liked.delete()
        else:
            like = Like(post=Post.objects.filter(id=id).first(), user=User.objects.filter(id=user).first())
            like.save()


        data = {
            'text' : 'text'
        }

        return JsonResponse(data)

class CommentView(View):

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', None)
        user = request.POST.get('user', None)
        post = request.POST.get('post', None)

        data = {
            'message': 'Error trying to Save Comment.'
        }

        if text is not None and user is not None and post is not None:
            comment = Comment(text=text, author=user, post=Post.objects.filter(id=post).first())
            comment.save()
            data = {
                'message': 'Comment Succesfully Saved.'
            }

        return JsonResponse(data)


    def get(self, request, *args, **kwargs):
        post = request.GET.get('post', None)

        objects = Comment.objects.filter(post=post).values().order_by('-created_date')

        json_data = json.dumps(list(objects), cls=DjangoJSONEncoder)

        return JsonResponse(json_data, safe=False)