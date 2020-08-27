from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



class AccountManager(BaseUserManager):
	def create_user(self,firstname,lastname,account_type,email,password):
		if not firstname :
			raise ValueError("Firstname is required")
		if not lastname :
			raise ValueError("Lastname is required")
		if not account_type:
			raise ValueError("Account type  is required")
		if not email:
			raise ValueError("Email is required")
		if not password:
			raise("Password is required")
			
		acct = self.model(firstname = firstname, lastname = lastname, account_type = account_type, email = self.normalize_email(email))
		
		acct.set_password(password)
		
		
		
		acct.save(using = self._db)
		
		return acct
		
	def create_superuser(self,firstname,lastname,account_type,email,password):
		
		acct = self.create_user(firstname = firstname,lastname = lastname, account_type = account_type, email = email, password = password)
		
		if acct.account_type != "A":
			acct.delete()
			raise ValueError("A superuser's account_type must be an ADMIN")
		acct.is_admin = True
		
		acct.is_active = True
		
		acct.save()
		
		return acct
		
			
			
		
class Account(AbstractBaseUser):
	firstname = models.CharField(max_length = 15,blank = False,null = False)
	middlename = models.CharField(max_length = 15,blank = True,null = False)
	lastname = models.CharField(max_length = 15,blank = False,null = False)
	ACCT_TYPE = (
	("B","buyer"),
	("M","merchant"),
	("A","admin"),
				)
	account_type = models.CharField(max_length  = 1, blank = False, null = False	, default = "M",choices = ACCT_TYPE)
	date_joined = models.DateTimeField(auto_now_add = True,editable =False )
	email = models.EmailField(max_length = 255, blank = False, null= False, unique = True )
	
	is_active = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)
	last_login = models.DateTimeField(auto_now_add = True)
	
	objects = AccountManager()
	
	USERNAME_FIELD = 'email'
	
	REQUIRED_FIELDS = ['firstname','lastname','account_type']
	
	
	def __str__(self):
		return self.get_fullname()
		
	def is_buyer(self):
		if self.account_type == "B":
			return True
		return False
		
	def is_merchant(self):
		if self.account_type == "M":
			return True
		return False
		
		
	
	def get_fullname(self):
		
		return self.firstname + " " + self.lastname
	
		
	def get_short_name(self):
		return self.firstname
		
	@property
	def is_staff(self):
		return self.is_admin
		
	
	def has_perm(self,perm,obj = None):
		return True
		
	
	def has_module_perms(self,app_label):
		return True
		
	
	
		
	
	

	
		