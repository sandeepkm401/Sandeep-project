from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from thegoodfind.models import Finder
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models.functions import Lower, Trim



#def home(request):
  #  return HttpResponse("Welcome to the Home Page")

def thegoodfind(request):
    return render(request, 'thegoodfind.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("Email").strip()
        password = request.POST.get("Password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Email not registered!")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid password!")
            return render(request, "login.html")

    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("Username").strip()
        email = request.POST.get("Email").strip()
        password = request.POST.get("n_Password")
        confirm_password = request.POST.get("c_Password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "signup.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "signup.html")

def image(request):
    return render(request, 'image.html')

@login_required(login_url='login')
def home(request):
    recent_items = Finder.objects.order_by('-created_at')[:6]

    context = {
        "Username": request.user.username,   
        "Email": request.user.email,         
        "recent_items": recent_items,
    }

    return render(request, 'home.html', context=context)


@login_required(login_url='login')
def profile(request):
    context = {
        "Username": request.user.username,
        "Email": request.user.email
    }
    return render(request, 'profile.html', context=context)

@login_required(login_url='login')
def finder(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        found_date = request.POST.get("found_date")

        if found_date:
            found_date = datetime.fromisoformat(found_date)

        image = request.FILES.get("image")

        
        finder_item = Finder.objects.create(
            name=name,
            description=description,
            location=location,
            found_date=found_date,
            image=image,
            posted_by=request.user 
        )

        
        context = {
            "name": finder_item.name,
            "description": finder_item.description,
            "location": finder_item.location,
            "found_date": finder_item.found_date,
            "image_url": finder_item.image.url if finder_item.image else None,
            "posted_by": finder_item.posted_by.username if finder_item.posted_by else "Unknown",
            "email": finder_item.posted_by.email if finder_item.posted_by else "Not available",
        }

        return render(request, "finder_result.html", context)

    return render(request, "finder.html")


@login_required(login_url='login')
def searcher(request):
    if request.method == "POST":
        
        name = request.POST.get("name", "").strip().lower()
        description = request.POST.get("description", "").strip().lower()
        location = request.POST.get("location", "").strip().lower()

        
        matches = Finder.objects.annotate(
            clean_name=Trim(Lower('name')),
            clean_description=Trim(Lower('description')),
            clean_location=Trim(Lower('location'))
        ).filter(
            Q(clean_name__icontains=name) &
            (Q(clean_description__icontains=description) | Q(clean_location__icontains=location))
        )

        return render(request, "searcher_result.html", {
            "name": name,
            "description": description,
            "location": location,
            "matches": matches
        })

    return render(request, "searcher.html")

def finder_detail(request, pk):
    item = get_object_or_404(Finder, pk=pk)
    return render(request, 'finder_detail.html', {"item": item})

@login_required(login_url='login')
def finder_contact(request, pk):
    item = get_object_or_404(Finder, pk=pk)

    context = {
        "item": item,
        "poster_name": item.posted_by.username if item.posted_by else "Unknown",
        "poster_email": item.posted_by.email if item.posted_by else "Not available",
    }

    return render(request, "finder_contact.html", context)


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')