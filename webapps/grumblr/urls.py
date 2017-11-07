from django.conf.urls import include, url
import grumblr.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^favicon.ico', grumblr.views.favicon),
    url(r'^$', auth_views.login),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^home/$', grumblr.views.home, name='home'),
    url(r'^registration/$', grumblr.views.register, name='registration'),
    url(r'logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^createnewuser/.*', grumblr.views.signup),
    url(r'^profile/(?P<username>\w+)$', grumblr.views.profile_other, name="profile_other"),
    url(r'^profile/$', grumblr.views.profile, name="profile_self"),
    url(r'^newpost/$', grumblr.views.newpost, name="newpost"),
    url(r'^edit/$', grumblr.views.edit_profile, name="edit_profile"),
    url(r'^followstream/$', grumblr.views.followerstream, name="followerstream"),
    url(r'^confirm/(?P<username>(\w+))/(?P<token>[\w\.-]+)/$', grumblr.views.confirm, name='confirm'),
    url(r'^reset-password/$', auth_views.password_reset, name="reset_password"),
    url(r'^reset-password/done/$', auth_views.password_reset_done, name="password_reset_done"),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),
    url(r'^reset-password/complete/$', auth_views.password_reset_complete, name = 'password_reset_complete'),
    url(r'^edit-password/$', grumblr.views.edit_password, name="edit_password"),
    url(r'^photo/(?P<username>\w+)$', grumblr.views.get_photo, name="photo"),
    url(r'photo/(?P<username>\w+)$', grumblr.views.get_photo, name="photo2"),
    url(r'^unfollow/(?P<username>\w+)$', grumblr.views.unfollow, name="unfollow"),
    url(r'^follow/(?P<username>\w+)$', grumblr.views.follow, name="follow"),
    url(r'^add_comment/(?P<postid>\d+)$', grumblr.views.add_comment, name="add_comment"),
    url(r'^add_comment_ajax/(?P<postid>\d+)$', grumblr.views.add_comment_ajax, name="add_comment_ajax"),

    # server side handler: link for ajax request to update the stream
    url(r'^updatestream/', grumblr.views.update_stream, name="update"),


    url(r'^.*', grumblr.views.error),

]