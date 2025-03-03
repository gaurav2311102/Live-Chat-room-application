from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,Membership
from django.views.generic import CreateView,DeleteView
from django.urls import reverse_lazy
from .forms import RoomForm,CreateUserForm,UpdateMessageForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
class SignupCreteView(CreateView):
    model = User
    template_name ="signup.html"
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        return super().form_valid(form)
    
    
def UserLogin(request):
    
    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or Password")
        
    return render(request,'login_page.html')

@login_required
def user_profile(request,pk):
    user = get_object_or_404(User,id=pk)
    rooms = user.joined_rooms.all()
    chat_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    page = request.GET.get('page',1)
    paginator = Paginator(rooms,3)
    try:
        rooms = paginator.page(page)
    except:
        rooms = paginator.page(1)
    
    context = {'user':user,'rooms':rooms,'chat_messages':chat_messages,'topics':topics}
    return render(request,'user_profile.html',context)  

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.prefetch_related('topics').filter(Q(topics__name__icontains=q) | Q(name__icontains =q ) | Q(description__icontains = q)).distinct()
    room_count = rooms.count()
    topics = Topic.objects.all()
    chat_messages = Message.objects.filter(Q(room__name__icontains = q))
    
    
    page = request.GET.get('page',1)
    paginator = Paginator(rooms,3)
    try:
        rooms = paginator.page(page)
    except:
        rooms = paginator.page(1)
        
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'chat_messages':chat_messages}
    return render(request , 'home.html',context)


    
def room(request,pk):
    room = get_object_or_404(Room,pk = pk)
    participant_count = room.participants.all().count()
    messages = room.message_set.all()
    is_member = Membership.objects.filter(user=request.user , room=room).exists() if request.user.is_authenticated else False
    
    return render(request,'room.html',{'room':room,'messages':messages,'is_member':is_member,'participant_count':participant_count})



class RoomCreateView(LoginRequiredMixin,CreateView  ):
    model = Room
    template_name = 'room_create.html'
    form_class = RoomForm
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create a New Room"
        context["page_type"] = "create"
        return context
    
    def form_valid(self, form):
        form.instance.host = self.request.user
        response = super().form_valid(form)
        Membership.objects.create(user = self.request.user , room = self.object)
        return response
    
    def get_success_url(self):
        return reverse_lazy('room',kwargs ={'pk': self.object.pk})
    
    
class RoomDeleteView(UserPassesTestMixin ,DeleteView ):
    model = Room
    template_name ='delete.html'
    success_url = reverse_lazy('home')
    context_object_name = "room"
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        room_id = self.object.id
        context = super().get_context_data(**kwargs)
        context["obj"] = "room"
        context['room_id'] = room_id 
        return context
    
    def test_func(self):
        room = self.get_object()
        return self.request.user == room.host or self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect('home')
    



@login_required(login_url='login')
def UpdateRoom(request,pk):
    room = get_object_or_404(Room,pk=pk)
    form = RoomForm(instance=room)
        
    if request.user != room.host and not request.user.is_superuser :
        return redirect('home')
    
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('room',pk=room.id)
        
    else:
        page_title = "Modify your room here" 
        context = {"form":form ,"page_title":page_title,"page_type":"update"} 
        return render(request,'room_create.html',context)
    

    
@login_required   
def create_message(request):
    
    if request.method == "POST":
        room_id = request.POST.get('room_id')
        user = request.user
        text = request.POST.get('text')
        room = get_object_or_404(Room,id=room_id)
    
        if text:
            Message.objects.create(user=user,room=room,text=text)
            return redirect('room',pk = room_id)
        
    else:
        return redirect('home')
    
    
@login_required
def update_message(request,pk):
    message = get_object_or_404(Message , pk=pk)
    
    if request.user == message.user:
        
        room_id = message.room.id
        if request.method == 'POST':
            form = UpdateMessageForm(request.POST,instance=message)
            
            if form.is_valid():
            
                form.save()
                return redirect('room',pk=room_id)
            
        else:
            form = UpdateMessageForm(instance=message)
            return render(request,'message_update.html',{'form':form})
        
class MessageDeleteView(UserPassesTestMixin,DeleteView):
    model = Message
    template_name = 'delete.html'
    
    def get_context_data(self, **kwargs):
        room_id = self.object.room.id
        context = super().get_context_data(**kwargs)
        context["obj"] = "message"
        context['room_id'] = room_id
        return context
    
    def get_success_url(self):
        return reverse_lazy('room',kwargs={'pk':self.object.room.id})
    
    def test_func(self):
        message = self.get_object()
        return self.request.user == message.user or self.request.user.is_superuser
    
    def handle_no_permission(self):
        return reverse_lazy('home')
    
@login_required
def join_room(request,pk):
    room = get_object_or_404(Room, id=pk)
    
    if Membership.objects.filter(user = request.user , room=room).exists():
        pass
    else:
        Membership.objects.create(user = request.user , room=room)
        
        return redirect('room',pk=pk)
    
@login_required
def leave_room(request,pk):
    room = get_object_or_404(Room,id=pk)
    membership = Membership.objects.filter(user = request.user , room = room)
    
    if membership.exists():
        membership.delete()
        

    return redirect('room',pk=pk)