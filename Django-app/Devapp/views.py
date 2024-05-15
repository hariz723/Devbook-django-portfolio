from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'let"s learn python!'},
#     {'id': 2, 'name': 'design with me '},
#     {'id': 3, 'name': 'Let"s learn django!!'},

# ]

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username= request.POST.get('username').lower()
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
            messages.error(request, "Username or Password does not exist")
    context= {'page':page}
    return render(request, 'main/login&reg.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during Registration')
            
    return render(request, 'main/login&reg.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.all()
    
    context={'rooms':rooms,'topics':topics, 'room_count':room_count,'room_message':room_message}
    return render(request,'main/home.html',context)

# pk-primary key
def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    # print(context)
    return render(request,'main/room.html', context)

@login_required(login_url='login/')

def CreateRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'main/room_form.html',context)

@login_required(login_url='login/')

def UpdatedRoom(request, pk): 
    #pk --> primary key
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('User not allow to modify Rooms without login')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'main/room_form.html',context)

# for delete the post
@login_required(login_url='/login')

def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('User not allow to modify Rooms without login')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj':room})

@login_required(login_url='/login')

def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('User not allow to modify Rooms without login')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj':message})