from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from app.forms import *
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from app.models import Dog, User, DogRental, Review
from datetime import datetime
from django.db import connection
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
# Create your views here.

def index(request):
    '''
    Renders the home page
    '''
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
                messages.success(request, "Login successful!")
                return HttpResponseRedirect('/')
            else:
              print("ELSE STATEMENT:", request.POST.get('next', '/'))
              return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            # Bad login details were provided. So we can't log the user in.
            messages.error(request, "Invalid login details provided. Please try again.")
            return render(request, 'login.html', context)


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
    '''
    Brings back all dogs listed in database
    '''
    dogs = Dog.objects.all()
    dogrental = DogRental.objects.all()
    context = {'dogs': dogs, 'dogrental': dogrental}
    template_name = 'dogs/dogs.html'
    return render(request, template_name, context)

@login_required
def add_dog(request):
    '''
    Allows user to add new dog
    '''
    currentuser = request.user
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
            messages.success(request, f"{form.name} added successfully!")
            return HttpResponseRedirect(request.POST.get('next', f'/your_dog_list/{currentuser.id}'))
        else:
            print("error")

@login_required
def rent_dog(request, dog_id):
    '''
    Allows user to rent dog
    '''
    currentuser = request.user
    dog_to_rent = Dog.objects.get(id = dog_id)
    dog_to_rent.is_available = False
    dog_to_rent.save()

    DogRental.objects.create(renter = currentuser, dog = dog_to_rent)
    return HttpResponseRedirect(reverse('app:dogs'))

@login_required
def return_dog(request, dog_id):
    '''
    Allows user to return dog they have rented
    '''
    currentuser = request.user
    dog_to_rent = Dog.objects.get(id = dog_id)
    rented_dog = DogRental.objects.get(renter = currentuser, dog = dog_to_rent)
    dog_to_rent.is_available = True
    dog_to_rent.save()
    
    rented_dog.delete()
    return HttpResponseRedirect(reverse('app:dogs'))

def dog_detail(request, dog_id):
    '''
    Shows user the specific dog's information
    '''
    currentuser = request.user
    dog_detail = get_object_or_404(Dog, id = dog_id)
    reviews = Review.objects.all()
    context = {'dog_detail': dog_detail, 'reviews': reviews}
    template_name = 'dogs/dog_detail.html'
    return render(request, template_name, context)

@login_required
def your_dog_list(request, user_id):
    '''
    Shows user the dogs they have uploaded
    '''
    currentuser = request.user
    your_dogs = Dog.objects.filter(owner_id = currentuser.id)
    context = {'your_dogs': your_dogs}
    template_name = 'dogs/your_dog_list.html'
    return render(request, template_name, context)

@login_required
def edit_dog(request, dog_id):
    '''
    Allows user to edit dog's information
    '''
    dog = get_object_or_404(Dog, id=dog_id)
    currentuser = request.user
    if request.method == 'POST':
        form = DogEditForm(instance=dog, data=request.POST, files=request.FILES)
        print("form", form)
        if form.is_valid():
            form.save()
        messages.success(request, f"{dog.name}'s details changed successfully!")
        return HttpResponseRedirect(reverse('app:your_dog_list', args=[currentuser.id]))
  
    elif request.method == 'GET':
        edit_dog = DogEditForm(instance=dog)
        template_name = 'dogs/edit_dog.html'
        context = {'edit_dog': edit_dog, 'dog': dog}
        return render(request, template_name, context)

@login_required
def profile(request, user_id):
    '''
    Renders the profile page
    '''
    currentuser = request.user
    profile = currentuser
    context = {'profile': profile}
    template_name = 'users/profile.html'
    return render(request, template_name, context)

@login_required
def edit_user(request, user_id):
    '''
    Allows user to edit their information
    '''
    currentuser = request.user
    user = currentuser
    print("user", user)
    if request.method == 'POST':
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()

        messages.success(request, "Profile details changed successfully!")
        return HttpResponseRedirect(reverse('app:profile', args=[user.id]))
  
    elif request.method == 'GET':
        edit_user = UserEditForm(instance=user)
        template_name = 'users/edit_user.html'
        context = {'edit_user': edit_user, 'user': user}
        return render(request, template_name, context)

#thanks brendan
@login_required
def change_password(request):
    '''
    Allows user to edit their password
    '''
    if request.method == 'GET':
        user = request.user
        new_password_form = ChangePassword()
        context = {'new_password_form': new_password_form}
        return render(request, 'users/change_password.html', context)

    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        old_password = request.POST['old_password']
        new_password_form = ChangePassword(data=request.POST, instance=user)
        print("old password", request.POST['old_password'])
        print("password", request.POST['password'])
        print("confirm pw", request.POST['confirm_password'])
        print("request post", request.POST)

        # validate password using installed validators in settings.py
        try:
            validate_password(request.POST['password']) == None
        except ValidationError:
            # return to form with form instance and message
            context = {'new_password_form': new_password_form}
            messages.error(request, "Password change failed. Please try again.")
            return render(request, 'users/change_password.html', context)

        # verify requesting user's username and old_password match
        authenticated_user = authenticate(username=user.username, password=old_password)
        print("authenticated user", authenticated_user)

        # check data types in submission.
        if new_password_form.is_valid():
            # Note that user instance is used here for updating (not posting)
            # Hash the password and update the user object
            user.set_password(request.POST['password'])
            user.save()

            # re-authenticate with new password
            authenticated_user = authenticate(username=user.username, password=request.POST['password'])
            login(request=request, user=authenticated_user)
            
            # return to user profile with success message after logging user in with new credentials
            messages.success(request, "Password changed successfully!")
            return HttpResponseRedirect(request.POST.get('next', f'/profile/{user.id}'))

        else:
            # return to form with form instance and message
            context = {'new_password_form': new_password_form}
            messages.error(request, "Password change failed. Please try again.")
            return render(request, 'users/change_password.html', context)

@login_required
def add_review(request, dog_id):
    '''
    Allows user to add a review to a dog
    '''
    currentuser = request.user
    if request.method == 'GET':
        dog = get_object_or_404(Dog, id=dog_id)
        add_review = DogReviewForm()
        template_name = 'dogs/add_review.html'
        context = {'add_review': add_review, 'dog': dog}
        return render(request, template_name, context)

    if request.method == 'POST':
        form = DogReviewForm(request.POST)
        dog = get_object_or_404(Dog, id=dog_id)
        if form.is_valid():
            form = form.save(commit=False)
            form.dog = dog
            form.reviewer = request.user
            description = request.POST['description']
            form.save()

            messages.success(request, "Review added successfully!")
            return HttpResponseRedirect(request.POST.get('next', f'/dog_detail/{dog_id}'))
        else:
            print("error")

@login_required
def are_you_sure(request, user_id):
    '''
    Allows user to confirm they want to delete their profile
    '''
    currentuser = request.user
    user = User.objects.get(id = user_id)
    context = {'user': user}
    template_name = 'users/are_you_sure.html'
    return render(request, template_name, context)
    
@login_required
def delete_profile(request, user_id):
    '''
    Allows user to delete their profile and all relations
    '''
    currentuser = request.user
    user = User.objects.get(id = user_id)
    reviews = Review.objects.all()
    dogs_rented = DogRental.objects.all()
    dogs = Dog.objects.all()

    for dog_rented in dogs_rented:
        for dog in dogs:
            if dog_rented.renter_id == user_id and dog_rented.dog_id == dog.id:
                print("dog", dog)
                dog.is_available = True
                dog.save()
                dog_rented.delete()

    for review in reviews:
        review.delete()

    user.delete()
    template_name = 'index.html'
    messages.success(request, "Profile deleted successfully!")
    return render(request, template_name)

@login_required
def delete_dog(request, dog_id):
    '''
    Allows user to remove a specific dog from listings
    '''
    currentuser = request.user
    dog = Dog.objects.get(id = dog_id)
    dog_rented = DogRental.objects.filter(dog_id = dog_id)
    reviews = Review.objects.all()

    for rented in dog_rented:
        if rented.dog_id == dog.id:
            rented.delete()

    for review in reviews:
        if review.dog_id == dog.id:
            review.delete()

    dog.delete()

    messages.success(request, "Dog deleted successfully!")
    return HttpResponseRedirect(request.POST.get('next', f'/your_dog_list/{currentuser.id}'))

@login_required
def delete_review(request, review_id):
    '''
    Allows user to delete their dog review
    '''
    currentuser = request.user
    review = Review.objects.get(id = review_id)
    dog = review.dog_id
    review.delete()
    return HttpResponseRedirect(request.POST.get('next', f'/dog_detail/{dog}'))

def search_results(request):
    '''
    Allows user to search for specific dog breed
    '''
    template_name = 'search/search_results.html'
    dogs = Dog.objects.all()
    breeds = Breed.objects.all()
    query = request.GET.get('q', '')
    if query:
        # query example
        results = Breed.objects.filter(name__icontains=query).distinct()
    else:
        results = []
    return render(request, template_name, {'results': results, 'query': query, 'dogs': dogs, 'breeds': breeds})
