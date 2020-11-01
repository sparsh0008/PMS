from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random
# Create your views here.


def Index(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'index.html', d)



def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    lasts = today - timedelta(7)

    tv = Vehicle.objects.filter(pdate=today).count()
    yv = Vehicle.objects.filter(pdate=yesterday).count()
    ls = Vehicle.objects.filter(pdate__gte=lasts,pdate__lte=today).count()
    totalv = Vehicle.objects.all().count()

    d = {'tv':tv,'yv':yv,'ls':ls,'totalv':totalv}
    return render(request,'admin_home.html',d)



def Logout(request):
    logout(request)
    return redirect('index')


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'changepassword.html',d)


def search(request):
    q = request.GET.get('searchdata')

    try:
        vehicle = Vehicle.objects.filter(Q(parkingnumber=q))
        vehiclecount = Vehicle.objects.filter(Q(parkingnumber=q)).count()

    except:
        vehicle = ""
    d = {'vehicle': vehicle,'q':q,'vehiclecount':vehiclecount}
    return render(request, 'search.html',d)


def add_category(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    if request.method=="POST":
        cn = request.POST['categoryname']
        try:
            Category.objects.create(categoryname=cn)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_category.html', d)


def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('index')
    category = Category.objects.all()
    d = {'category':category}
    return render(request, 'manage_category.html', d)


def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('manage_category')




def add_vehicle(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    category1 = Category.objects.all()
    if request.method=="POST":
        pn = str(random.randint(10000000, 99999999))
        ct = request.POST['category']
        vc = request.POST['vehiclecompany']
        rn = request.POST['regno']
        on = request.POST['ownername']
        oc = request.POST['ownercontact']
        pd = request.POST['pdate']
        it = request.POST['intime']
        status = "In"
        category = Category.objects.get(categoryname=ct)

        try:
            Vehicle.objects.create(parkingnumber=pn,category=category,vehiclecompany=vc,regno=rn,ownername=on,ownercontact=oc,pdate=pd,intime=it,outtime='',parkingcharge='',remark='',status=status)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category1':category1}
    return render(request, 'add_vehicle.html', d)


def manage_incomingvehicle(request):
    if not request.user.is_authenticated:
        return redirect('index')
    vehicle = Vehicle.objects.filter(status="In")
    d = {'vehicle':vehicle}
    return render(request, 'manage_incomingvehicle.html', d)

def manage_outgoingvehicle(request):
    if not request.user.is_authenticated:
        return redirect('index')
    vehicle = Vehicle.objects.filter(status="Out")
    d = {'vehicle':vehicle}
    return render(request, 'manage_outgoingvehicle.html', d)


def view_incomingdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    vehicle = Vehicle.objects.get(id=pid)
    if request.method == 'POST':
        rm = request.POST['remark']
        ot = request.POST['outtime']
        pc = request.POST['parkingcharge']
        status = "Out"
        try:
            vehicle.remark = rm
            vehicle.outtime = ot
            vehicle.parkingcharge = pc
            vehicle.status = status
            vehicle.save()
            error = "no"
        except:
            error = "yes"

    d = {'vehicle': vehicle,'error':error}
    return render(request,'view_incomingdetail.html', d)



def view_outgoingdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request,'view_outgoingdetail.html', d)


def print_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request,'print.html', d)


def betweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'betweendate_reportdetails.html')



def betweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        vehicle = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td))
        vehiclecount = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td)).count()
        d = {'vehicle': vehicle,'fd':fd,'td':td,'vehiclecount':vehiclecount}
        return render(request, 'betweendate_reportdetails.html', d)
    return render(request, 'betweendate_report.html')