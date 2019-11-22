from django import forms

class LoginForm(forms.Form):
   LOGIN_ID = forms.CharField(max_length = 100)
   PASSWORD = forms.CharField(widget = forms.PasswordInput())
   
class CommentForm(forms.Form):
	input_comment = forms.CharField()

class ReplyForm(forms.Form):
	input_reply = forms.CharField()

class AcceptForm(forms.Form):
	accept = forms.IntegerField()
	
	
class signUpForm(forms.Form):
   LOGIN_ID = forms.CharField(max_length = 50)
   PASSWORD = forms.CharField(widget = forms.PasswordInput())
   email = forms.EmailField()
   name = forms.CharField(max_length=30)
   institution = forms.CharField(max_length=50)
   profession = forms.CharField(max_length=30)
	
