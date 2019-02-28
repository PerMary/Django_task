from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from myapp.models import Demand

def logout_view(request): 
	logout(request)	
	return render(request, 'users/logout.html')
