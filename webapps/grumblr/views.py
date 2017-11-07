# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, render, get_object_or_404, resolve_url, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import Context,loader,RequestContext
from types import StringType
from .forms import UserRegistrationForm, ProfileModelForm, ResetPasswordForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import  send_mail
from .models import UserBasicInfo, Posts, Profile, UserFollower, Comments
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from mimetypes import guess_type
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import os
import json


# Create your views here.
def main(request):
    return render(request, "main.html", {})

def favicon(requet):
    dirspot = os.getcwd()
    print dirspot
    image_data = open("grumblr/static/images/favicon.ico", "rb").read()
    return HttpResponse(image_data, content_type="image/png")

def login2(request):
    respose = ""
    if(request.POST):
        if 'uname' in request.POST:
            respose = request.POST['uname']
    return HttpResponse("You just logged in as "+respose)

def error(request):
    logout(request)
    return main(request)

@login_required
def home(request):
    # get the user's data from the database
    user = UserBasicInfo.objects.get(username = request.user.username)
    context = {}
    context['firstname'] = user.firstname
    context['lastname'] = user.lastname
    context['user'] = request.user
    allposts = Posts.objects.all().order_by('-time')
    context['allposts'] = allposts
    context['time'] = date.day
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, "home.html", context)

    #print request.user.username
    #context['newpost'] = userlatestpost
    #return HttpResponse(request.user.email)
    return render(request, "home.html", context)

@login_required
def followerstream(request):
    context = {}
    context['user'] = request.user
    context['time'] = date.day
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        render(request, "home.html", context)
    follower, created = UserFollower.objects.get_or_create(user = request.user)
    if not created:
        names = follower.get_followers()
        allposts = Posts.objects.filter(username__in=names).order_by('-time')
        context['allposts'] = allposts
        #context['commentform'] = CommentForm()


    return render(request, "followerstream.html", context)

@login_required
def profile(request):
    context = {}

    try:
        user = UserBasicInfo.objects.get(username = request.user.username)
    except ObjectDoesNotExist:
        return render(request, "home.html", context)
    context['user'] = user
    posts = Posts.objects.filter(username=request.user.username).order_by('-time')
    context['posts'] = posts
    context['firstname'] = user.firstname
    context['lastname'] = user.lastname
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        render(request, "home.html", context)
    context['self'] = request.user
    #context['commentform'] = CommentForm()
    return render(request, "profile.html", context)

@login_required
def profile_other(request, username):
    context = {}
    try:
        userinfo = UserBasicInfo.objects.get(username = username)
    except ObjectDoesNotExist:
        return HttpResponse("Unrecognized username")
    context['self'] = request.user
    posts = Posts.objects.filter(username = username).order_by('-time')
    context['posts'] = posts
    context['firstname'] = userinfo.firstname
    context['lastname'] = userinfo.lastname
    user = get_object_or_404(User, username=username)
    context['user'] = user
    if following(username, request.user) == True:
        context['following'] = 'yes'
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        render(request, "home.html", context)
    context['commentform'] = CommentForm()
    return render(request, "profile.html", context)

@login_required
def newpost(request):
    errors = []
    if not 'newpost' in request.POST or not request.POST['newpost']:
        errors.append('You must enter an item to add.')
    else:
        new_post = Posts(username = request.user.username, post = request.POST['newpost'])
        new_post.save()
    posts = Posts.objects.filter(username=request.user.username).order_by('-time')
    context = {'posts': posts, 'errors': errors}
    #profile = Profile.objects.filter(user=request.user)
    #if len(profile) == 1:
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except:
        context['errors'].append('No posts match to this user')
    context['commentform'] = CommentForm()
    return render(request, 'profile.html', context)



def register(request):
    return render(request, "registration.html", {})

@login_required
def editprofile(request):
    context = {}
    user = UserBasicInfo.objects.get(username=request.user.username)
    context['user'] = UserBasicInfo.objects.get(username=request.user.username)
    posts = Posts.objects.filter(username=request.user.username).order_by('-time')
    context['posts'] = posts
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        pass

    if request.method == 'GET':
        context['displayform'] = "display"
        context['profileform'] = ProfileModelForm()
        return render(request, "profile.html", context)

    elif request.method == 'POST':
        newprofile, created = Profile.objects.get_or_create(user = request.user)
        profileform = ProfileModelForm(request.POST, instance=newprofile)
        if profileform.is_valid():
            newprofile = profileform.save(commit=False)
            newprofile.user = request.user
            newprofile.save()
        else :
            return HttpResponse("invalid form")
        #context['profile']= newintro
        return HttpResponseRedirect('/profile/')
    return render(request, "profile.html", context)


@login_required
def edit_profile(request):
    context = {}
    context['passwordform'] = ResetPasswordForm()
    context['profileform'] = ProfileModelForm()
    if request.method == 'GET':
        return render(request, "editprofile.html", context)

    if request.method == 'POST':
        messages = []
        newprofile, created = Profile.objects.get_or_create(user=request.user)
        profileform = ProfileModelForm(request.POST, request.FILES, instance=newprofile)
        # allow user only update a certain set of fields, fields left blank
        # won't affected previously stored data
        if profileform.is_valid():
            newprofile = profileform.save(commit=False)
            newprofile.user = request.user
            if not profileform.cleaned_data['bio']is None:
                newprofile.bio = profileform.cleaned_data['bio']
                newprofile.save(update_fields=['bio'])
                messages.append('Added %s' % profileform.cleaned_data['bio'])
            if not profileform.cleaned_data['firstname'] is None:
                newprofile.firstname = profileform.cleaned_data['firstname']
                newprofile.save(update_fields=['firstname'])
                messages.append('Added %s' % profileform.cleaned_data['firstname'])
            if not profileform.cleaned_data['lastname'] is None:
                newprofile.lastname = profileform.cleaned_data['lastname']
                newprofile.save(update_fields=['lastname'])
                messages.append('Added %s' % profileform.cleaned_data['lastname'])
            if not profileform.cleaned_data['age'] is None:
                newprofile.age = profileform.cleaned_data['age']
                newprofile.save(update_fields=['age'])
                messages.append('Added %s' % profileform.cleaned_data['age'])
            if not profileform.cleaned_data['picture'] is None:
                newprofile.picture = profileform.cleaned_data['picture']
                newprofile.save(update_fields=['picture'])

            context['messages'] = messages
            context['profileform'] = profileform


        return render(request, "editprofile.html", context)

@login_required()
def edit_password(request):
    context = {}
    context['profileform'] = ProfileModelForm()
    context['passwordform'] = ResetPasswordForm()
    if request.method == 'GET':

        #profile = Profile.objects.filter(user=request.user)

        return render(request, "editprofile.html", context)


    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user.username)
        #password1= request.POST['new_password']
        #password2=request.POST['new_password_r']
        #if password1 == password2:
        resetform = ResetPasswordForm(request.POST)
        if resetform.is_valid():
            user.set_password(resetform.cleaned_data['password'])
            user.save()
            messages = ["You has successfully changed your password"]
            context['messages']=messages
        else:
            context['passworderrors'] = ["invalid password"]
    context['profileform'] = ProfileModelForm()
    context['passwordform'] = ResetPasswordForm()
    return render(request, "editprofile.html", context)

def reset_password(request, email, username):
    return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

def signup(request):
    if request.method ==  'GET':
        return render(request, "registration.html", {})
    errors = []
    context = {}
    context['errors']=errors
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            newusername = userObj['username']
            newfirstname = userObj['firstname']
            newlastname = userObj['lastname']
            newemail = userObj['email']
            newpassword = userObj['password']
            newuser, created = UserBasicInfo.objects.get_or_create(username=newusername)
            # check if the username has already been registered
            if(not created):
                errors.append("ERR: username exists.")
            else:
                newuser.firstname = newfirstname
                newuser.lastname = newlastname
                newuser.email = newemail
                newuser.save() #mush add save to update database
            if not (User.objects.filter(username=newusername).exists() or User.objects.filter(email=newemail).exists()):
                user = User.objects.create_user(newusername, newemail, newpassword)
                user.is_active = False
                user.save()
                #send_mail(newemail, 'Use %s to confirm your email' % user.confirmation_key)
                send_email_confirmation(request, user)
                # login the new user
                user = authenticate(username=newusername, password=newpassword)
                #login(request, user)
                return HttpResponseRedirect(reverse('home'))

            else:
                errors.append("ERR: email exists.")
        else:
            errors.append(form.errors)
            return render(request, 'registration.html', context)
    else:
        return HttpResponseRedirect("no post query")
    return render(request, 'registration.html', context)

@login_required()
def get_photo(request, username):
    #return HttpResponse("Request from" + username)
    user = get_object_or_404(User, username=username)
    #print "get photo for: " + username
    if not (Profile.objects.filter(user = user).exists()):
        return get_default_photo()

    entry = get_object_or_404(Profile, user = user )
    #print "entry!"
    if entry and entry.picture:
        content_type = guess_type(entry.picture.name)
        #print "url"+ entry.picture.name
        return HttpResponse(entry.picture, content_type = content_type)
    else:

        raise Http404

def get_default_photo():
    dirspot = os.getcwd()
    #print dirspot
    picture = dirspot+"/grumblr/static/images/user/user.png"
    try:
        with open(picture, "rb") as f:
            #print "default photo:" + f.name
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        raise Http404

@login_required
def follow(request, username):
    self = get_object_or_404(User, id = request.user.id)
    target = get_object_or_404(User, username=username)
    follower, created = UserFollower.objects.get_or_create(user = self)
    follower.followers.add(target)

    return HttpResponseRedirect(reverse('profile_other', kwargs={'username': username}))

@login_required
def unfollow(request, username):
    self = get_object_or_404(User, id=request.user.id)
    target = get_object_or_404(User, username=username)
    follower, created = UserFollower.objects.get_or_create(user=self)
    follower.followers.remove(target)

    return HttpResponseRedirect(reverse('profile_other', kwargs={'username': username}))

def following(username, self):
    follower, created = UserFollower.objects.get_or_create(user=self)
    followed = follower.get_followers()
    followed = follower.get_followers()
    for f in followed:
        if f == username:
            return True
    return False

def send_email_confirmation(request, newuser):
    token = default_token_generator.make_token(newuser)
    email_body = """Welcome to grumblr, please click the link below to confirm your recent registration:
    localhost:8000%s
    """ % (reverse('confirm', args=(newuser.username, token)))
    send_mail(subject="Verify your email address", message=email_body, from_email="no-reply@grumblr.com",
              recipient_list=[newuser.email])

def confirm(request, username, token):
    user = User.objects.get(username = username)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def update_stream(request):
    # the time range for the new posts should be withinn
    # [current, current-timeinterval]
    # slow network? use timestamp at the server side instead of
    # datetime.now()
    time = datetime.now() - timedelta(seconds=5)
    new_posts = Posts.objects.filter(time__gte = time).order_by('time')
    response_text = serializers.serialize("json", new_posts)


    return HttpResponse(response_text, content_type="application/json")

def add_comment(request, postid):
    # print "parent url:" + request.META.get('HTTP_REFERER')
    if request.POST:
        form = CommentForm(request.POST)
        print "post a comment for " + postid
        if(form.is_valid()):
            text = form.cleaned_data['text']
            print text
            parent_post = Posts.objects.get(pk = postid)
            #usr = get_object_or_404(Profile, user = request.user)
            comment = Comments(username = request.user.username, text = text, post = parent_post)
            comment.save()
            response_text = serializers.serialize("json", [comment])
            return HttpResponse(response_text, content_type="application/json")
            #JsonResponse({'time': comment.time})
            #return
            #HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print form
            return HttpResponse('')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_comment_ajax(request, postid):
    print postid
    if request.POST:
        print "post a comment for "+postid
        form = CommentForm(request.POST)
        if (form.is_valid()):
            text = form.cleaned_data['text']
            print text
            parent_post = Posts.objects.get(pk=postid)

            comment = Comments(username=request.user.username, text=text, post=parent_post)
            comment.save()
            return HttpResponse('')