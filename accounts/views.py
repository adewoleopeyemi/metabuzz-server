from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.views import View
from .forms import SignInForm,SignUpForm
from django.contrib import messages
from buyers.models import *
from .models import Account


_cart_id = "CART_ID" 


class SignIn(View):
	def get(self,request):
		form = SignInForm()
		
		return render(request,'accounts/sign_in.html',{'form':form})
		
	def post(self,request):
		form = SignInForm(request.POST)
		#print(request.POST)
		if form.is_valid():
			user = authenticate(username = form.cleaned_data.get('email'),password  = form.cleaned_data.get('password'))
			if user is not None and (user.account_type == 'B'):
				login(request,user)
				if form.cleaned_data.get('keep_me_signed_in') == True:
					
					print(form.cleaned_data.get('keep_me_signed_in'))
					request.session.set_expiry(60* 60 * 24 * 30)
				else:
					request.session.set_expiry(0)
				if request.POST['redirect_to']:
					return redirect(request.POST.get('redirect_to'))
				else:
					return redirect('/')
				
				messages.success(request,"Sign In Successful")
			else:
				messages.warning(request,"Invalid Login details")
				return render(request,'accounts/sign_in.html',{'form':form})
		
				
				
		else:
			messages.warning(request,"Invalid fields!")
			return render(request,'accounts/sign_in.html',{'form':form})
		
			
		



class SignUp(View):
	def get(self,request):
		form = SignUpForm()
		
		return render(request,'accounts/sign_up.html',{'form':form})
		
	def post(self,request):
		form = SignUpForm(request.POST)
		if form.is_valid():
			
			cd = form.cleaned_data
			
			fn = cd.get("firstname")
			
			ln = cd.get("lastname")
			
			mn = cd.get("middlename")
			
			eml = cd.get("email")
			
			p1 = cd.get("password1")
			
			p2 = cd.get("password2")
			
			re = cd.get("receive_emails") 
			
			if not (p1 and p1 ) or (p1 != p2):
				messages.warning(request,"Password fields did not match")
				return render(request,'accounts/sign_up.html',{'form':form})
		
			
			
			if not( _cart_id in list(request.session.keys())):
			
				#print("Anonymous user,creating a new user!")
				
				
				user = Account.objects.create_user(firstname = fn,  lastname = ln,account_type = 'B',email = eml, password = p2)
				
				user.middlename = mn
				
				user.is_active = True
			
				user.save()
				
				buyer = Buyer.objects.create(account = user,  receive_emails = re )
				
				buyer.save()
				
				
				login(request,user)
				request.session.set_expiry(60* 60 * 24 * 30)
				
				if request.POST['redirect_to']:
					return redirect(request.POST.get('redirect_to'))
				else:
					return redirect(reverse("whitehouse:frontpage"))
			
				
			
			else:
				#print("acquaintance user")
				
				
				existing_cart = get_object_or_404(Cart,cart_id = request.session.get(_cart_id))
				
				user = Account.objects.create_user(firstname = fn,  lastname = ln,email = eml, account_type = "B" ,password = p2 )
				
				user.is_active = True
			
				user.save()
				
				buyer = Buyer.objects.create(account = user, cart = existing_cart ,receive_emails = re )
				
				buyer.save()
				
				
				request.session.flush()
				
				login(request,user)
				
				return redirect(reverse("whitehouse:frontpage"))
				
		else:
			messages.warning(request,"Invalid Fields")
			print(form.errors)
			return render(request,'accounts/sign_up.html',{'form':form})
		
			
			