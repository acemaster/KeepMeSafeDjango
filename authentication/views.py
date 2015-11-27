from django.shortcuts import render
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile,UserMessages,UserLocation,User,UserSafetyList,UserStatus,UserNotifications,TweetUserLocation,ForgotPassword
import json
import hashlib
from random import randint
from django.core.mail import send_mail

from django.contrib import messages
# Create your views here.
def index(request):
	title="homepage"
	if request.user.is_authenticated():
		return render(request,'site/dashboard.html',{'page': 'dashboard'})
	else:
		return HttpResponseRedirect('/login')

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
	for f in friendslistfrom:
		friends.append(f.userfrom)
	for f in friendslistto:
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


def frequests(request):
	friendsto=UserSafetyList.objects.filter(userfrom=request.user)
	friendsfrom=UserSafetyList.objects.filter(userto=request.user,status=1)
	return render(request,'site/frequests.html',{'page': 'requests','friendsto':friendsto,'friendsfrom': friendsfrom})


def acceptreq(request):
	if request.method == 'POST':
		friend_id=request.POST['id']
	friend=User.objects.get(id=friend_id)
	frndreq=UserSafetyList.objects.get(userfrom=friend,userto=request.user)
	frndreq.status=2
	frndreq.save()
	return JsonResponse({'success': 1})


def rejectreq(request):
	if request.method == 'POST':
		friend_id=request.POST['id']
	friend=User.objects.get(id=friend_id)
	frndreq=UserSafetyList.objects.get(userfrom=friend,userto=request.user)
	frndreq.status=3
	frndreq.save()
	return JsonResponse({'success': 1})

def aroundme(request):
	friendslistfrom=UserSafetyList.objects.filter(userto=request.user).filter(status=2)
	friendslistto=UserSafetyList.objects.filter(userfrom=request.user).filter(status=2)
	friends=[]
	for f in friendslistfrom:
		friends.append(f.userfrom)
	for f in friendslistto:
		friends.append(f.userto)
	return render(request,'site/aroundme.html',{'page': 'aroundme','friends':friends})

def checksafe(request):
	message="Error"
	if request.method == 'POST':
		friend_id=request.POST['id']
		code=request.POST['code']
		us=UserStatus.objects.get(user=User.objects.get(id=friend_id))
		if us.safety_code == code:
			print "Success"
			us.safety_code=''
			us.safety_status=True
			us.save()
			message="Success"
			notifications=UserNotifications.objects.filter(userfrom=User.objects.get(id=friend_id))
			for n in notifications:
				n.read=2
				n.save()
		else:
			message="Incorrect code"
	response={}
	response['message']=message
	return HttpResponseRedirect('/')


def notsafe(request):
	try:
		us=UserStatus.objects.get(user=request.user)
	except:
		us=UserStatus()
	us.user=request.user
	us.safety_status=False
	st=request.user.first_name + str(request.user.id)
	# us.safety_code=hashlib.md5(st).hexdigest()
	if us.safety_code == '':
		us.safety_code=randint(1000, 9999)
	us.save()
	friendslistfrom=UserSafetyList.objects.filter(userto=request.user).filter(status=2)
	friendslistto=UserSafetyList.objects.filter(userfrom=request.user).filter(status=2)
	friends=[]
	for f in friendslistfrom:
		friends.append(f.userfrom)
	for f in friendslistto:
		friends.append(f.userto)
	for f in friends:
		try:
			temp=UserNotifications.objects.get(user=f,userfrom=request.user)
		except:
			temp=None
		if temp:
			temp.message=request.user.first_name + " is in trouble please help"
			temp.read=False
			temp.save()
		else:
			temp=UserNotifications()
			temp.user=f
			temp.userfrom=request.user
			temp.message=request.user.first_name + " is in trouble please help"
			temp.read=False
			temp.save()
	return render(request,'site/notsafe.html',{'page': 'notsafe','safety':us})


def getnotifications(request):
	response={}
	count=0
	try:
		temp=UserNotifications.objects.get(user=request.user,read=0)
	except UserNotifications.DoesNotExist:
		temp=None
	if temp:
		response['success']=1
		response['message']=temp.message
		response['from']=temp.userfrom.id
		response['id']=temp.id
	else:
		try:
			temp=UserNotifications.objects.get(user=request.user,read=1)
		except UserNotifications.DoesNotExist:
			temp=None
		if temp:
			response['success']=1
			response['message']=temp.message
			response['from']=temp.userfrom.id
			response['id']=temp.id
		else:
			response['success']=0
	print response
	return JsonResponse(response)


def readnotification(request):
	if request.method == 'POST':
		msg_id=request.POST['id']
		temp=UserNotifications.objects.get(id=msg_id)
		temp.read=2
		temp.save()
	return JsonResponse({'success':1})

def recievenotification(request):
	if request.method == 'POST':
		msg_id=request.POST['id']
		temp=UserNotifications.objects.get(id=msg_id)
		temp.read=1
		temp.save()
	return JsonResponse({'success':1})

def notifications(request):
	userstat=UserLocation.objects.get(user=request.user)
	lat=userstat.latitude
	longt=userstat.longt
	try:
		temp1=UserNotifications.objects.filter(user=request.user,read=0)
	except UserNotifications.DoesNotExist:
		temp1=None
	try:
		temp2=UserNotifications.objects.filter(user=request.user,read=1)
	except UserNotifications.DoesNotExist:
		temp2=None
	if temp1:
		temp=temp1
	elif temp2:
		temp=temp2
	else:
		temp=None
	return render(request,'site/notifications.html',{'page': 'notifications','notifications':temp,'lat':lat,'longt':longt})


def getnotificationcount(request):
	try:
		temp1=UserNotifications.objects.filter(user=request.user,read=0)
	except UserNotifications.DoesNotExist:
		temp1=None
	try:
		temp2=UserNotifications.objects.filter(user=request.user,read=1)
	except UserNotifications.DoesNotExist:
		temp2=None
	if temp1:
		temp=temp1
	elif temp2:
		temp=temp2
	else:
		temp=None
	if temp:
		count=len(temp)
	else:
		count=0
	return JsonResponse({'count':count})


def getcode(request):
	response={}
	response['success']=0
	if request.method =='POST':
		friend_id=request.POST['id']
		try:
			us=UserStatus.objects.get(user=User.objects.get(id=friend_id))
			print us
		except:
			us=None
		if us:
			response['code']=us.safety_code
			response['success']=1
		else:
			response['success']=0

	return JsonResponse(response)


def aroundmetweet(request):
	friendslistfrom=TweetUserLocation.objects.all()
	friends=[]
	for f in friendslistfrom:
		friends.append(f)
	return render(request,'site/aroundmetweet.html',{'page': 'aroundmetweet','friends':friends})

def forgotp(request):
	email=request.POST['email']
	us=User.objects.get(username=email)
	response={}
	success=0
	if us:
		try:
			us2=ForgotPassword.objects.get(user=us)
		except:
			us2=ForgotPassword()
			us2.user=us
		us2.code=randint(1000, 9999)
		us2.save()
		send_mail('Password code', 'Code is '+str(us2.code), 'webmaster@web.com',[us.username], fail_silently=False)
		success=1
	else:
		success=0
		response['message']="Invalid user"
	response['success']=success
	return JsonResponse(response)


def forgotv(request):
	email=request.POST['email']
	code=request.POST['code']
	us=User.objects.get(username=email)
	us2=ForgotPassword.objects.get(user=us)
	success=0
	if us2.code == code:
		success=1
	else:
		success=0
	return JsonResponse({'success': success})


def forgotnp(request):
	email=request.POST['email']
	password=request.POST['password']
	us=User.objects.get(username=email)
	us.password=password
	us.set_password(us.password)
	us.save()
	return JsonResponse({'success':1})

def forgotpassword(request):
	return render(request,'site/forgotpassword.html',{'page': 'forgotpassword'})


def checklocation(request):
	success=0
	lat=request.POST['lat']
	longt=request.POST['longt']
	us=UserLocation.objects.get(user=request.user)
	if us.latitude != lat or us.longt != longt:
		success=1
	else:
		success=0
	return JsonResponse({'success':success})

def getlocation(request):
	success=0
	response={}
	uid=request.POST['id']
	lat=request.POST['lat']
	longt=request.POST['longt']
	user=User.objects.get(id=uid)
	us=UserLocation.objects.get(user=user)
	if us.latitude != lat or us.longt != longt:
		response['success']=1
		response['lat']=us.latitude
		response['longt']=us.longt
	else:
		response['success']=0
	return JsonResponse(response)

def sendmessage(request):
	response={}
	success=0
	friendslistfrom=UserSafetyList.objects.filter(userto=request.user).filter(status=2)
	friendslistto=UserSafetyList.objects.filter(userfrom=request.user).filter(status=2)
	friends=[]
	for f in friendslistfrom:
		friends.append(f.userfrom)
	for f in friendslistto:
		friends.append(f.userto)
	for f in friends:
		send_mail('User has moved', 'Location is'+str(request.POST['lat'])+' : '+str(request.POST['longt']), 'webmaster@web.com',[f.username], fail_silently=False)
	success=1
	response['success']=success
	return JsonResponse(response)

