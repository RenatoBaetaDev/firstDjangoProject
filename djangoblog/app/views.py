from datetime import datetime

from django.contrib.auth.models import User
from django.http import cookie
from django.shortcuts import (
    get_object_or_404, redirect, render, HttpResponse
)
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from app.forms import EditProfileForm, EditUserForm, PostForm
from app.models import Post, Profile


class PostCreate(CreateView):
    model = Post
    fields = ['body']


class PostUpdate(UpdateView):
    model = Post
    fields = ['body']


class UserProfile(View):
    template_name = 'users/user.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs['username']).first()
        profile = Profile.objects.filter(user=user).first()
        posts = Post.objects.filter(author=user)
        return render(request, self.template_name, {
            'user': user,
            'profile': profile,
            'posts': posts,
        })


class UserFollow(View):
    template_name = 'users/user.html'

    def get(self, request, *args, **kwargs):
        user_follower = User.objects.filter(
            username=self.kwargs['follower']).first()
        user_followed = User.objects.filter(
            username=self.kwargs['followed']).first()
        user_follower.follow(user_followed)

        profile = Profile.objects.filter(user=user_follower).first()
        posts = Post.objects.filter(author=user_follower)
        return render(request, self.template_name, {
            'user': user_follower,
            'profile': profile,
            'posts': posts,
        })


class UserUnfollow(View):
    template_name = 'users/user.html'

    def get(self, request, *args, **kwargs):
        user_follower = User.objects.filter(
            username=self.kwargs['follower']).first()
        user_followed = User.objects.filter(
            username=self.kwargs['followed']).first()
        user_follower.unfollow(user_followed)

        profile = Profile.objects.filter(user=user_follower).first()
        posts = Post.objects.filter(author=user_follower)
        return render(request, self.template_name, {
            'user': user_follower,
            'profile': profile,
            'posts': posts,
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


class Index(View):
    def get(self, request, *args, **kwargs):
        show_followed = 'all'
        if 'index' in request.session:
            show_followed = request.session['index']
        if show_followed == 'followed':
            # posts = Post.objects.all()
            posts = request.user.followed_posts()
        else:
            posts = Post.objects.all()

        form = PostForm()
        context = {
            'posts': posts,
            'form': form,
            'show_followed': show_followed,
        }
        return render(request, "index.html", context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.timestamp = datetime.utcnow()
            post.save()
            return redirect('index')

def index_all(request):
    request.session["index"] = "all"
    # response = HttpResponseRedirect('/')
    # response.set_cookie('showAll', '0', max_age=30 * 24 * 60 * 60)
    return redirect('index')


def index_followed(request):
    request.session["index"] = "followed"
    # response = HttpResponseRedirect('/')
    # response.set_cookie('showAll', '1', max_age=30 * 24 * 60 * 60)
    return redirect('index')


def users(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})


def user(request, username):
    pass


def post(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'posts/post.html', {'posts': [post]})
  