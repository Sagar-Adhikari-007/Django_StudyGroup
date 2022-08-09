from multiprocessing import context
from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from .models import Message, Room, Topic, User
from .forms import RoomForm, userForm, myUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = myUserCreationForm()
    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           login(request, user)
           return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__contains=q) |
        Q(description__icontains=q)
    )
    
    room_count = rooms.count()
    topic = Topic.objects.all()[0:5]
    comments = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = { 'rooms': rooms , 'topic': topic, 'room_count': room_count, 'comments': comments}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        comment =   Message.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get('body')
        )
        comment.save()
        room.participants.add(request.user)
        return redirect('room', pk=pk)



    context = { 'room': room , 'comments': comments, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    comments = user.message_set.all()
    topic = Topic.objects.all()
    context = { 'user': user, 'rooms': rooms, 'comments': comments, 'topic': topic}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topic = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),          
        )
        return redirect('home')


    context = {'form': form,'topic': topic,}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topic = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
           
    context = {'form': form, 'topic': topic, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteComment(request,pk):
    comment = Message.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('You are not authorized to delete this comment')
  

    if request.method == 'POST':
        comment.delete()
        return redirect('room', pk=comment.room.id)
    return render(request, 'base/delete.html', {'obj': comment})
                        


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = userForm(instance=user)

    if request.method == 'POST':
        form = userForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', pk=user.id)
        


    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topic = Topic.objects.filter(name__icontains=q)
    context = {'topic': topic}
    return render(request, 'base/topics.html', context)
      
def activityPage(request):
    # q = request.GET.get('q') if request.GET.get('q')!=None else ''
    comments = Message.objects.all()
    context = {'comments': comments}
    return render(request, 'base/activity.html', context)    
    
      


