from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *
from .models import CustomUser
from django.contrib.auth.models import User
import imagehub.settings as settings
import base64
from PIL import Image
import io

def index(request):
    
    return render(request, 'feed.html')

def modelview(request):
    return render(request, 'input_form.html')

def generate_dummy_images():
    images = []
    for i in range(1, 4):
        image = Image.open(str(settings.BASE_DIR) + '/static/images/image' + str(i) + '.png')
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        base64_encoded = base64.b64encode(img_bytes).decode('utf-8')
        images.append(base64_encoded)
    return images

@login_required(login_url='login_view')
def generate_images(request):
    images = []

    prompt = ''
    num_images = 1
    if request.method == 'GET':
        images = generate_dummy_images()
 
    if request.method == 'POST':
        prompt = request.POST.get('prompt_1')
        num_images = int(request.POST.get('num_images', 1))

        if settings.DEBUG:
            images = generate_dummy_images()
        else:
            data = {
                'prompts': [prompt] * num_images,  
                'model': 'opendalle' 
            }
            response = requests.post("http://4738-34-143-195-6.ngrok-free.app/generate", json=data)
            images = response.json()

    context = {
        'response': images,
        'prompt': prompt,
        'num_images': num_images,
        'user': request.user.email
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
    return render(request, 'signup.html')

def confirm_email(email):
    return True

def signup_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')
        else:
            if not confirm_email(email):
                messages.error(request, 'Email not valid')
                return render(request, 'signup.html')
            
            user = CustomUser.objects.create_user(email=email, password=password1)
            user.save()
            print("user created")
            messages.success(request, 'Successfully signed up')
            return redirect('login_view')


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