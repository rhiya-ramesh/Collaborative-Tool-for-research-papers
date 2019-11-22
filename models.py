from django.db import models
from django_mysql.models import JSONField
from django import forms
from datetime import datetime
import django

# Create your models here.
class Title(models.Model):
	title = models.CharField(max_length=150)

	def __str__(self):
		return self.title

class Users(models.Model):
	LOGIN_ID = models.CharField(max_length=50,primary_key=True)
	PASSWORD = models.CharField(max_length=30) #, widget=forms.PasswordInput)
	email = models.EmailField()
	name = models.CharField(max_length=30)
	institution = models.CharField(max_length=50)
	profession = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name

class Documents(models.Model):
	class Meta:
		unique_together = (("docID","version"),)
		
	docID = models.DateTimeField(default=django.utils.timezone.now)
	version = models.FloatField(default=1.0)
	docname = models.CharField(max_length=50)
	content = JSONField()
	lock = models.IntegerField(default=0)
	approve = models.BooleanField(default=False)
	
	"""
	myID = models.IntegerField(default=0)
	
	def save(self, *args, **kwargs):
		if self._state.adding:
			last_id = self.objects.all().aggregate(largest=models.Max('myID'))['largest']
			if (last_id is not None) and (self.version==1.0):
				self.myID = last_id + 1
		super(MyModel, self).save(*args, **kwargs)
	"""
	def __str__(self):
		return self.docname+" "+str(self.version)+str(self.docID)
		
	
class User_Document(models.Model):
	LOGIN_ID = models.ForeignKey(Users, on_delete=models.CASCADE)
	docID = models.ForeignKey(Documents, on_delete=models.CASCADE)
	ROLE = models.CharField(max_length=50, choices = [('COLLABORATOR','C'),('REVIEWER','R')], default='COLLABORATOR')
	
	"""
	def __str__(self):
		return self.LOGIN_ID + str(self.docID)
	"""
	
	class Meta:
		unique_together = (("docID","LOGIN_ID"),)
		
		 
class LatestVersion(models.Model):
	docVersionID = models.ForeignKey(Documents, on_delete=models.CASCADE)
	latestVersion = models.FloatField(default=1.0)
	lockUser = models.ForeignKey(Users, on_delete=models.CASCADE, default = None, blank = True, null = True)

class Comments(models.Model):
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    docID = models.DateTimeField()
    commentID =models.AutoField('Comment ID',primary_key=True)
    version = models.FloatField()
    comment = models.TextField()
    comment_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
	    #return self.userID.LOGIN_ID+self.comment
    	return str(self.commentID)

class Reply(models.Model):
    replyID = models.AutoField('Reply ID',primary_key=True)
    commentID = models.ForeignKey(Comments, on_delete=models.CASCADE)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    reply = models.TextField()

    def __str__(self):
    	return self.userID.LOGIN_ID+self.reply

class Accept_Reject(models.Model):
    commentID = models.ForeignKey(Comments, on_delete=models.CASCADE)
    userID = models.ForeignKey(Users, on_delete=models.CASCADE)
    accept = models.IntegerField()
    reject = models.IntegerField()

    def __str__(self):
    	return self.userID.LOGIN_ID+str(self.accept)+str(self.reject)
    
 
