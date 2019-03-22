from django.shortcuts import render, redirect, get_object_or_404
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MenteeRegisterForm,UserUpdateForm, ProfileUpdateForm
from django.views.generic import TemplateView
from ..models import Profile, Msg
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from django.urls import reverse_lazy
from .. import models
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.



"""Home landing page"""
def home(request):

    return render(request, 'home.html')


"""Home account landing page after you login"""
@login_required
def account(request):

    users = User.objects.all().filter(is_mentor=True)

    context = {

        'users': users


    }

    return render(request, 'menti/account.html', context)


"""Controls the register module"""
def register(request):

    if request.method == 'POST':

        form = MenteeRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')

    else:

        form = MenteeRegisterForm()


    return render(request, 'menti/register.html', {'form': form})


"""Login function"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('account'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'menti/login.html', {})






"""View, Update Your Profile"""
@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {

        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'menti/profile.html', context)


"""Creates new message"""

class MessageCreateView(CreateView):

    fields = ('receipient', 'msg_content')
    model = Msg
    template_name = 'menti/messagecreate.html'




    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)






"""Views lists of messages you have sent to other users"""

class MessageListView(ListView):

    model = Msg
    template_name = 'menti/listmessages.html'
    context_object_name = 'sentmesso'

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)


"""details the message sent"""

class SentDetailView(DetailView):
    model = Msg
    context_object_name = 'messo'
    template_name = 'menti/sent.html'



    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)


"""Views lists of inbox messages received"""

class InboxView(ListView):

    model = Msg
    context_object_name = 'inbox'
    template_name = 'menti/inbox.html'


    def get_queryset(self):
        return self.model.objects.filter(receipient=self.request.user)

""" Views in detail the message received in the inbox"""


"""Inbox Detailed view"""
class InboxDetailView(DetailView):

    model = Msg
    context_object_name = 'messo'
    template_name = 'menti/inboxview.html'


    def get_queryset(self):
        return self.model.objects.filter(receipient=self.request.user)




"""controls messege view"""
class MessageView(TemplateView):
    template_name = 'menti/messages-module.html'
    model = models.Msg
    context_object_name = 'sentmesso'



def messege_view(request):

    count = Msg.objects.values('msg_content').count()

    context = {

        'count': count
    }


    return render(request, 'menti/messages-module.html', context)



class SentMessageDelete(DeleteView):
    model = models.Msg
    success_url = reverse_lazy("list")
    template_name = 'menti/sentmessage_delete.html'