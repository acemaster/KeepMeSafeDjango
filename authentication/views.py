from django.shortcuts import render
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile,UserMessages,UserLocation,User,UserSafetyList
import json

from django.contrib import messages
# Create your views here.
def index(request):
	title="homepage"
	return render(request,'site/index.html',{'title':title})

def _login(request):
	title="Login"
	return render(request,'site/login.html',{'title':title})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _loginuser(request):
	if request.method=="POST":
		username=request.POST.get('email',False)
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				user.lastLoginDate=datetime.now()
				user.status=True
				user.save()
				if not request.POST.get('remember_me', None):
					request.session.set_expiry(0)
				messages.info(request,'Welcome '+user.username)
				return HttpResponseRedirect('/dashboard/')
			else:
				messages.info(request,'Your account is inactive. Contact webmaster')
				return HttpResponseRedirect('/')
		else:
			messages.error(request,'Invalid username/password')
			return HttpResponseRedirect('/')

def register(request):	
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		print profile_form
		print request.FILES['picture']
		if user_form.is_valid() and profile_form.is_valid():
			
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			if request.FILES['picture']:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
			messages.info(request,str(user_form.errors)+str(profile_form.errors))
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request,'site/register.html',{'title':'Sign Up','current_page':'register',\
		'user_form':user_form,'profile_form':profile_form,'registered':registered})


def dashboard(request):
	return render(request,'site/dashboard.html',{'page': 'dashboard'})

def _logout(request):
	logout(request)
	return HttpResponseRedirect('/')


def addLocation(request):
	success=0
	if request.method == 'POST':
		latitude=request.POST['lat']
		longt=request.POST['longt']
		current_user=request.user
		us=UserLocation.objects.filter(user=current_user)
		if(len(us) == 0):
			user_loc=UserLocation()
			user_loc.latitude=latitude
			user_loc.longt=longt
			user_loc.user=current_user
			user_loc.save()
		else:
			us=UserLocation.objects.get(user=current_user)
			us.latitude=latitude
			us.longt=longt
			us.save()
		# print user_loc
		success=1
	return JsonResponse({'success': success})


def safetylist(request):
	friendslistfrom=UserSafetyList.objects.filter(userto=request.user).filter(status=2)
	friendslistto=UserSafetyList.objects.filter(userfrom=request.user).filter(status=2)
	friends=[]
	for f in friendslistto:
		friends.append(f.userfrom)
	for f in friendslistfrom:
		friends.append(f.userto)
	return render(request,'site/safetylist.html',{'page': 'safety','friends':friends})

def getlist(request):
	search_term=''
	if request.method == 'POST':
		search_term=request.POST['search_term']
	if len(search_term) == 0:
		users=User.objects.all()
	else:
		users=User.objects.filter(first_name__startswith=search_term)
	print users
	response={}
	response['users']=[]
	for u in users:
		if u.is_superuser == False:
			response['users'].append({'name': u.first_name,'picture': u.userprofile.picture.url,'id':u.id,'email':u.username})
	return JsonResponse(response)

def makefriend(request):
	if request.method == 'POST':
		friend_id=request.POST['id']
	friend=User.objects.get(id=friend_id)
	frndreq=UserSafetyList()
	frndreq.userto=friend
	frndreq.userfrom=request.user
	frndreq.status=1
	frndreq.save()
	return JsonResponse({'success': 1})



