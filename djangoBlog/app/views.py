from django.shortcuts import render
from django.http import JsonResponse
from app.models import Post, Profile
from django.contrib.auth.models import User
from datetime import datetime
from django.views import View
from django.core import serializers



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

        data = serializers.serialize('json', Post.objects.all())


        return JsonResponse(data, safe=False)