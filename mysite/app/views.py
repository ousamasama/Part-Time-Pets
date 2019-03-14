from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from app.forms import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from app.models import Dog, User, DogRental
from datetime import datetime
from django.db import connection
# Create your views here.

def index(request):
    template_name = 'index.html'
    return render(request, template_name)

def register(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'register.html'
        return render(request, template_name, {'user_form': user_form})


def login_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = {'next': request.GET.get('next', '/')}
    print("CONTEXT:", context)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            if request.POST.get('next') == '/':
              return HttpResponseRedirect('/')
            else:
              print("ELSE STATEMENT:", request.POST.get('next', '/'))
              return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, 'invalid_login.html', context)


    return render(request, 'login.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

def dogs(request):
    dogs = Dog.objects.all()
    dogrental = DogRental.objects.all()
    context = {'dogs': dogs, 'dogrental': dogrental}
    template_name = 'dogs/dogs.html'
    return render(request, template_name, context)

@login_required
def add_dog(request):
    if request.method == 'GET':
        add_dog = DogForm()
        template_name = 'dogs/add_dog.html'
        context = {'add_dog': add_dog}
        return render(request, template_name, context)

    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            print("form data", form)
            form.save()
            return HttpResponseRedirect(reverse('app:dogs'))
        else:
            print("error")

@login_required
def rent_dog(request, dog_id):
    currentuser = request.user
    dog_to_rent = Dog.objects.get(id = dog_id)
    dog_to_rent.is_available = False
    dog_to_rent.save()

    DogRental.objects.create(renter = currentuser, dog = dog_to_rent)
    return HttpResponseRedirect(reverse('app:dogs'))

@login_required
def return_dog(request, dog_id):
    currentuser = request.user
    dog_to_rent = Dog.objects.get(id = dog_id)
    rented_dog = DogRental.objects.get(renter = currentuser, dog = dog_to_rent)
    dog_to_rent.is_available = True
    dog_to_rent.save()
    
    rented_dog.delete()
    return HttpResponseRedirect(reverse('app:dogs'))

def dog_detail(request, dog_id):
    dog_detail = get_object_or_404(Dog, id = dog_id)
    context = {'dog_detail': dog_detail}
    template_name = 'dogs/dog_detail.html'
    return render(request, template_name, context)

@login_required
def your_dog_list(request, user_id):
    currentuser = request.user
    your_dogs = Dog.objects.filter(owner_id = currentuser.id)
    context = {'your_dogs': your_dogs}
    template_name = 'dogs/your_dog_list.html'
    return render(request, template_name, context)

@login_required
def edit_dog(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    currentuser = request.user
    if request.method == 'POST':
        form = DogEditForm(instance=dog, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save() 
        return HttpResponseRedirect(reverse('app:your_dog_list', args=[currentuser.id]))
  
    elif request.method == 'GET':
        edit_dog = DogEditForm(instance=dog)
        template_name = 'dogs/edit_dog.html'
        context = {'edit_dog': edit_dog, 'dog': dog}
        return render(request, template_name, context)

@login_required
def profile(request, user_id):
    currentuser = request.user
    profile = currentuser
    context = {'profile': profile}
    template_name = 'users/profile.html'
    return render(request, template_name, context)

@login_required
def edit_user(request, user_id):
    currentuser = request.user
    user = currentuser
    print("user", user)
    if request.method == 'POST':
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save() 
        return HttpResponseRedirect(reverse('app:profile', args=[user.id]))
  
    elif request.method == 'GET':
        edit_user = UserEditForm(instance=user)
        template_name = 'users/edit_user.html'
        context = {'edit_user': edit_user, 'user': user}
        return render(request, template_name, context)