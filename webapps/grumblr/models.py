# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image

# Create your models here.
# A database to store user's information when sign up
# It should contain 4 entries: username, firstname, lastname, and email
# , and username will be used as the primary key to mapping to other
# data table

class UserBasicInfo(models.Model):
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField()
    user = models.ForeignKey(User)

    # how to print characters
    def __unicode__(self):
        return self.username

class Posts(models.Model):
    username = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post = models.CharField(max_length=100)
    #puser = models.ForeignKey(User)
    def __unicode__(self):
        return self.username

    #@property
    #def comments(self):





class Profile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=20, blank=True, null=True, )
    lastname = models.CharField(max_length=20, blank=True, null=True, )
    age = models.CharField(max_length=5, blank=True, null=True, )
    bio = models.CharField(max_length=420, blank=True, null=True,)
    picture = models.ImageField(upload_to="user-img", blank=True, default="user.png")

    def __unicode__(self):
        return "%s %s (%s)" % (self.firstname, self.lastname,
                               self.age)

class UserFollower(models.Model):
    user = models.OneToOneField(User)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, related_name='followers')


    def get_followers(self):
        names = []
        f = self.followers.all()
        for u in f:
            names.append(u.username)
        return names
    def __str__(self):
        return '%s, %s' % self.user, self.count

class Comments(models.Model):
    username = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    text = models.TextField()
    post = models.ForeignKey(Posts, unique=False, related_name="comments")
    picture = models.ImageField(upload_to="user-img", blank=True, default="user.png")

    def __unicode__(self):
        return self.text


