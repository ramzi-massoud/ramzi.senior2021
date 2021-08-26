from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
from django.conf.urls import url
# from Project.models import *
from Project import forms
# from Project.forms import *
from Project.settings import EMAIL_HOST_USER
from School_MS.models import *
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages
from Project import settings
import logging

# email_imports:
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.


logging.basicConfig(filename='test.log',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)


def index(request):

    # context = {''}
    # return HttpResponse("<h1>SUCCESS</h1>")
    form = forms.ContactForm()
    context = {'form':form}
    return render(request, 'pages/home.html',context)


def user_login(request):
    """
    user login through username & password
    """
    # form = forms.StudentProfileInfoForm
    form = forms.UserForm()
    context = {'form': form}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # django built in authentication function
        user = authenticate(username=username, password=password)
        # get user obj by username
        # if valid -> check if active -> if true ->login
        try:
            if user:
                if user.is_active:
                    # session
                    login(request, user)
                    logging.debug("Logged in")
                    return HttpResponseRedirect(reverse('home'))

            else:
                logging.warn("\t:invalid login details")
                return HttpResponse("<h3>Invalid Login Details...</h3>")
        except:
            logging.warn(":**user_login: *invalid login details")
            return HttpResponse("<h3>Invalid Login Details.</h3>")
    else:
        return render(request, 'pages/login.html', context)

    return render(request, 'pages/login.html', context)


@login_required()
def announcements(request):
    """
    get list of announcements
    """
    context = {}

    Announcements = Announcement.objects.all()

    context['Announcements'] = Announcements
    logging.info("Navigated to Announcenemet Page")
    return render(request, 'pages/Announcements.html', context)


@login_required
def list_courses(request):
    """
    get list of announcements
    """
    context = {}

    Courses = AllCourses.objects.all() #SELECT * FROM Courses'

    context['Courses'] = Courses

    return render(request, 'pages/all_courses.html', context)


@login_required
def home(request):
    """
    Preview user profile
    """

    context = {
        'Courses': Courses.objects.filter(user=request.user).all()
        #query to select courses from database where user = user
    }

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['emp'] = StudentProfile.objects.filter(
        user_id=request.user.id).first()
    return render(request, 'pages/userpage.html', context)


@login_required
def edit_profile(request):
    """
    user updates his *existing profile
    """
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST, instance=request.user)

        profile_form = forms.StudentProfileInfoForm(
            data=request.POST, instance=request.user.studentprofile)
        try:
            if user_form.is_valid() and profile_form.is_valid():
                # save user to DB:
                user = user_form.save()
                # encrypt password:
                user.set_password(user.password)
                # update user:
                user.save()
                # can't commit => still need to edit profile
                profile = profile_form.save(commit=False)

                # check if profile pic provided
                if 'profile_pic' in request.FILES:
                    print("picture found")
                    profile.profile_pic = request.FILES['profile_pic']

                profile.user = user
                profile.save()
                logging.info("\t **edit_profile:Profile succesfully updated")
                
        except:
            logging.warn("\t **edit_profile:FAILED to UPDATE PROFILE") 
            return HttpResponseRedirect(reverse('home'))
            return render(request, 'pages/edit_profile.html',context)
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.StudentProfileInfoForm(instance=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    context['MEDIA_URL'] = settings.MEDIA_URL
    context['emp'] = StudentProfile.objects.filter(
        user_id=request.user.id).first()
    return render(request, 'pages/edit_profile.html', context)

@login_required()
def contactView(request):
    if request.method == 'GET':
        form = forms.ContactForm()
    else:
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['ramzi.senior2021@gmail.com'])
                logging.info("\t **contactView:Email Sent Succesfully")
            except BadHeaderError:
                logging.warn("\t **contactView: FAILED to SEND Email")
                return HttpResponse('Invalid header found.')
            #return HttpResponse('<h3>We Recieved your Email... <br/>We Will reply Shortly...</h3> ')
            return render(request,'pages/thanks.html')           
    return render(request, 'pages/contactus.html', {'form': form})
    # return HttpResponse("OK")


def logout_request(request):
    """
    log out for user from all pages
    """
    form = forms.UserForm()
    context = {'form': form}
    logout(request)
    logging.info("\t **logout_request: USER Logged out")
    return HttpResponseRedirect(reverse('user_login'))
    # return render(request, 'pages/login.html',context)


urlpatterns = [
    url(r'index/', index, name='index'),
    url(r'user_login/', user_login, name='user_login'),
    url(r'logout/', logout_request, name='logout_request'),
    url(r'home/', home, name='home'),
    url(r'announcements/', announcements, name='announcements'),
    url(r'list_courses/', list_courses, name='list_courses'),
    url(r'edit_profile/', edit_profile, name='edit_profile'),
    url(r'contactView/', contactView, name='contactView'),

]
