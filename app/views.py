from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *
import imagehub.settings as settings

def index(request):
    return render(request, 'feed.html')

def modelview(request):
    return render(request, 'input_form.html')

@login_required(login_url='login_view')
def generate_images(request):
    if request.method == 'POST':
        if settings.DEBUG:
            datas = {
                "prompt": request.POST.get('prompt_1'),
                "num_images": int(request.POST.get('num_images'))
            }
            images = OpenAIapi().get_images(datas)
        else:
            pass
    context = {
        'response': images
    }

    return render(request, 'output.html', context)


def login_view(request):
    if request.user.is_authenticated:
        context = {
            'messages': 'You are already logged in'
        }
        return redirect('index')
    else:
        context = {
            'messages': 'Please login'
        }
    return render(request, 'login.html', context)

def signup_view(request):
    return redirect(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
            messages.success(request, 'Successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_view')

@login_required(login_url='login_view')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out')
    else:
        messages.warning(request, 'You are not logged in')

    return redirect('login_view')