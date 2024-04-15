from django.shortcuts import render,redirect
from .forms import LoginForm,CreateUserForm,CreateRecordForm,UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from .models import Record

from django.contrib.auth.decorators import login_required
from django.contrib import messages
def home(request):
    return render(request,'webapp/index.html')



def register(req):
    form = CreateUserForm()
    if req.method == "POST":
        form  = CreateUserForm(req.POST)

        if form.is_valid():
            form.save()
            messages.success(req,"Account created successfully")
            return redirect('my-login')

    context = {'form' : form}
    return render (req,'webapp/register.html',context = context)



# login a user
def my_login(req):
    form = LoginForm()
    if req.method =="POST":
        form = LoginForm(req, data = req.POST)

        if form.is_valid():
            username  = req.POST.get('username')
            password = req.POST.get('password')

            user = authenticate(req , username = username , password = password)
            if user is not None:
                auth.login(req,user)
                return redirect('dashboard')
    context = {'form' : form}

    return render(req,'webapp/my-login.html',context = context)


#  user logout 
def user_logout(req):
    auth.logout(req)
    messages.success(req,"User logout successfully")
    return redirect('my-login')



# dashboard 
@login_required(login_url='my-login')
def dashboard(req):
    my_record  = Record.objects.all()
    context = {'records' : my_record}
    return render(req,'webapp/dashboard.html',context = context)



# Create  record 

@login_required(login_url="my-login")
def create_record(req):
    form = CreateRecordForm()
    if req.method == "POST":
        
        form = CreateRecordForm(req.POST)
        if form.is_valid():

            form.save()
            
            messages.success(req," Your record was created")

            return redirect("dashboard")
        
    context = {"form" : form}
    return render(req,'webapp/create-record.html',context = context)
    
#update a record

@login_required(login_url="my-login")
def update_record(req, pk):
    record = Record.objects.get(id = pk)
    form = UpdateRecordForm(instance = record)
    
    if req.method == "POST":
        form = UpdateRecordForm(req.POST,instance = record)

        if form.is_valid():

            form.save()

            messages.success(req,"Your record has been updated ")
            
            return redirect('dashboard')
    context = {"form" : form }
    return render(req,'webapp/update-record.html',context = context)


# read/view a single record
@login_required(login_url='my-login')

def singular_record(req, pk):
    all_records = Record.objects.get(id = pk)
    context = {'record' : all_records}

    return render(req,'webapp/view-record.html',context=context)


# delete  record

@login_required(login_url="my-login")
def delete_record(req,pk):
    record  = Record.objects.get(id = pk)
    record.delete()

    messages.success(req,"Your record has been deleted successfully")

    return redirect("dashboard")


# user logout

def user_logout(req):
    auth.logout(req)
    messages.success(req,"Logout Successfully")

    return redirect("my-login")