from datetime import datetime, timezone

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from Forum.forms import UserCreationForm, UploadAvatarForm, DocumentForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views import generic
from django.views.generic import FormView
from django.views.generic import View
from django.http import HttpResponse

from Forum.forms import CommentForm, PostForm, FMessageForm, OMessageForm
from Forum.models import Post, Comment, CustomUser, Avatar, Document, FMessage, OMessage


class IndexView(generic.ListView):
    template_name = "forum/index.html"
    context_object_name = "latest_post_list"

    def get_queryset(self):
        return Post.objects.order_by()[:]


def detailView(request, post_id):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['CUser'] = CustomUser.objects.get(username = Post.objects.get(id = post_id).post_user)
    args['CUserAvatar'] = Document.objects.get(description=Post.objects.get(id = post_id).post_user)
    args['Post'] = Post.objects.get(id=post_id)
    args['comments'] = Comment.objects.filter(comment_post_id=post_id)
    args['users'] = CustomUser.objects.all()
    for user in CustomUser.objects.all():
        if not Document.objects.filter(description=user.username):
            av1 = Document(description=user.username, document= user.avatar)
            av1.save()
    args['avatars'] = Document.objects.all()
    args['form'] = comment_form
    args['request'] = request
    return render_to_response('forum/detail.html', args)


def addComment(request, post_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_post = Post.objects.get(id=post_id)
            comment.comment_name = request.user.username
            comment.save()
    return redirect('/forum/%s/' % post_id)


class CreatePostForm(FormView):
    form_class = PostForm
    success_url = '/forum/'
    template_name = "forum/createpost.html"

    def form_valid(self, form):
        instanse = form.save(commit=False)
        instanse.post_user = self.request.user.username
        #print(self.request.user.username)

        instanse.save()

        return redirect(self.get_success_url())

class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = '/forum/login/'
    template_name = "forum/register.html"

    def form_valid(self, form):
        form.save()

        return super(RegisterFormView,self).form_valid(form)

class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = "forum/login.html"

    success_url = '/forum/'

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request,self.user)
        return super(LoginFormView,self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/forum/")


def AvatarView(request):
    if not Document.objects.filter(description=request.user.username):
        av1 = Document(document=request.user.avatar, description=request.user.username)
        av1.save()
    args = {}
    args.update(csrf(request))
    args['avatar'] = Document.objects.get(description=request.user.username)
    args['request'] = request
    args['form'] = DocumentForm
    args['fuserms'] = FMessage.objects.filter(fuser=request.user.username)
    args['suserms'] = FMessage.objects.filter(suser=request.user.username)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            if Document.objects.get(description = request.user.username):
                p1 =Document.objects.get(description=request.user.username)
                p1.delete()
            form1.description = request.user.username
            form1.save()
            redirect('/forum/')
    return render_to_response("forum/avatar.html", args)

def AvatarUploadView(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            if Document.objects.filter(description=request.user.username):
                p1 = Document.objects.get(description=request.user.username)
                p1.delete()
            form1.description = request.user.username
            form1.save()
            return redirect('/forum/avatar/')
    else:
        form = DocumentForm()
    return render(request, 'forum/AvatarUpload.html', {
        'form': form
    })

def search(request):
    errors = []
    form = {}
    search_users = {}
    if request.POST:

        form['name'] = request.POST.get('name')

        if not form['name']:
            errors.append('Заполните имя')
        if not errors:
            search_users = CustomUser.objects.filter(username__contains=form['name'])

    return render(request, 'forum/contact.html', {'errors': errors, 'form': form, 'search_users': search_users})

def UserPage(request, user_id):
    args = {}
    args.update(csrf(request))
    PUser = CustomUser.objects.get(id = user_id)
    if not Document.objects.filter(description=PUser.username):
        av1 = Document(document=PUser.avatar, description=PUser.username)
        av1.save()
    see = False
    for message in FMessage.objects.all():
        if (message.fuser == PUser.username and message.suser == request.user.username) or (message.fuser == request.user.username and message.suser == PUser.username):
            see = True
            args['msid'] = message.id
    args['see'] = see
    args['avatar'] = Document.objects.get(description=PUser.username)
    args['request'] = request
    args['PUser'] = PUser
    return render_to_response('forum/UserPage.html',args)

def MessagePage(request, message_id):
    args = {}
    args.update(csrf(request))
    args['request'] = request
    args['fmessage'] = FMessage.objects.get(id = message_id)
    args['omessages'] = OMessage.objects.filter(sm_fm_id=message_id)
    args['form'] = OMessageForm
    if FMessage.objects.get(id = message_id).fuser == request.user.username:
        args['ouser'] = CustomUser.objects.get(username = FMessage.objects.get(id = message_id).suser)
        args['ouserav'] = Document.objects.get(description=FMessage.objects.get(id = message_id).suser)
        args['fuserav'] = Document.objects.get(description=request.user.username)
    else:
        args['ouser'] = CustomUser.objects.get(username=FMessage.objects.get(id=message_id).fuser)
        args['ouserav'] = Document.objects.get(description=FMessage.objects.get(id=message_id).fuser)
        args['fuserav'] = Document.objects.get(description=request.user.username)
    if request.POST:
        form = OMessageForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.sm_fm_id = message_id
            commit.user = request.user
            commit.save()
            redirect("/forum/message/%s"%message_id)
    return render_to_response('forum/messages.html',args)




def CreateMessage(request, user_id):
    args = {}
    args.update(csrf(request))
    args['request'] = request
    args['form'] = FMessageForm
    args['tuser'] = CustomUser.objects.get(id = user_id)
    if request.POST:
        form = FMessageForm(request.POST)
        if form.is_valid():
            fmessage = form.save(commit=False)
            fmessage.fuser = request.user.username
            fmessage.suser = CustomUser.objects.get(id=user_id).username
            fmessage.save()
            return redirect('/forum/')
    return render_to_response('forum/createm.html',args)
