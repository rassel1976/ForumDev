from django.conf.urls import url
from django.contrib import admin

from Forum import views

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.detailView, name='detail'),
    url(r'^(?P<post_id>[0-9]+)/addcomment/$',views.addComment),
    url(r'^createpost/', views.CreatePostForm.as_view()),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^avatar/$', views.AvatarView),
    url(r'^avatar/add/$',views.AvatarUploadView),
    url(r'^contact/$', views.contact),
    url(r'^user/(?P<user_id>[0-9]+)/$',views.UserPage,name='user'),
    url(r'^message/(?P<message_id>[0-9]+)/$',views.MessagePage,name='message'),
    url(r'^message/(?P<user_id>[0-9]+)/add/$',views.CreateMessage, name='startmes'),
]
