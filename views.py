from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.urls import reverse
from django import forms
from Collab_Docs.forms import LoginForm, CommentForm, ReplyForm, AcceptForm, signUpForm
from Collab_Docs.models import Documents, LatestVersion, Comments, Users, Reply, Accept_Reject, User_Document, Title
import json
import datetime
import re
import nltk
import heapq


# Create your views here.

"""
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)
"""

def suggest(request):
	if request.method == 'POST':
		term = str(request.POST.get('title'))
		resp=[]
		titles = Title.objects.values('title')
		if term!='' and term!=' ':
			for t in titles:
				curr_t = t['title']
				if term in curr_t:
					resp.append(curr_t)
		return HttpResponse(json.dumps(resp), content_type="application/json")

def summarize(request):
	if request.method == 'POST':
		content = request.POST.get('content')
		# Removing Square Brackets and Extra Spaces
		content = re.sub(r'\[[0-9]*\]', ' ', content)
		content = re.sub(r'\s+', ' ', content)
		formatted_content = re.sub('[^a-zA-Z]', ' ', content)
		formatted_content = re.sub(r'\s+', ' ', formatted_content)
		sentence_list = nltk.sent_tokenize(content)
		stopwords = nltk.corpus.stopwords.words('english')
		word_frequencies = {}
		for word in nltk.word_tokenize(formatted_content):
			if word not in stopwords:
				if word not in word_frequencies.keys():
					word_frequencies[word] = 1
				else:
					word_frequencies[word] += 1
		maximum_frequncy = max(word_frequencies.values())
		for word in word_frequencies.keys():
			word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
		sentence_scores = {}
		for sent in sentence_list:
			for word in nltk.word_tokenize(sent.lower()):
				if word in word_frequencies.keys():
					if len(sent.split(' ')) < 30:
						if sent not in sentence_scores.keys():
							sentence_scores[sent] = word_frequencies[word]
						else:
							sentence_scores[sent] += word_frequencies[word]
		summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
		summary = ' '.join(summary_sentences)
		print(summary)
		return HttpResponse(summary, content_type='text/plain')

def DocumentView(request):
	docs = Documents.objects.all().order_by('docname')
	context = {
		'docs_list':docs
	}
	return render(request,'documents.html', context=context)
	
def EditorView(request,LOGIN_ID,id,version,role):
	# If this is a POST request then process the Form data
	user = Users.objects.get(LOGIN_ID = LOGIN_ID)
	if request.method == 'POST':
		
		try:
			if(request.POST['approve']):
				print("hereinapprove")
				docs = Documents.objects.filter(docID=id,version=version).update(approve=True)

		except:
			pass

		try:
			if(request.POST["input_comment"]): 
				#if comment is to be added
				print("In the funtion")
				form = CommentForm(request.POST)
				if form.is_valid():
					input_comment = request.POST.get('input_comment')
					#print(LOGIN_ID)
					#print(input_comment)
					newComment = Comments(userID=user, docID = id, version = version, comment=input_comment)
					newComment.save()
				#return HttpResponseRedirect(reverse('editor',kwargs={'LOGIN_ID':LOGIN_ID, 'id':id, 'version':version}))
		except: 
			pass
			
		try:
			if(request.POST["input_reply"]):
				print("Im here")
				form = ReplyForm(request.POST)
				if form.is_valid():
					print("Form valid")
					input_reply = request.POST.get('input_reply')

					reply_comment_id = Comments.objects.get(commentID=request.POST.get('reply_com_id'))
						
					reply = Reply(commentID =reply_comment_id, userID= user, reply =input_reply)
					print("SAVEIT")
					reply.save()
				#return HttpResponseRedirect(reverse('editor',kwargs={'LOGIN_ID':LOGIN_ID, 'id':id, 'version':version}))
		except: 
			pass
			
		try:
			if(request.POST['contents']):
			
				print("here1")
				newVersion = request.POST.getlist('versioning')
				
				x=request.POST["contents"]
				print(x)
					
				if(newVersion[0]=="No"):
					check=Documents.objects.filter(docID=id,version=version).update(content=x)
					print("check:",check)
					bla = Documents.objects.filter(docID=id,version=version).update(lock=0)
					return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
					
				else:
					doc = Documents.objects.filter(docID=id)
					trackVersion = 1.0
					for i in doc:
						lastDoc = i
					newVersionNumber = float(lastDoc.version)+1
					newDoc = Documents(docID=lastDoc.docID,docname=lastDoc.docname,version=newVersionNumber,content=x,lock=0) 
					newDoc.save()
					doc = LatestVersion.objects.filter(docVersionID__docID=id).update(latestVersion = newVersionNumber)
					return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
				#next = request.POST.get('next', '/')
				#return HttpResponseRedirect(next)
		except: 
			pass
		
		try:
			if(request.POST['accept']):
				form = CommentForm(request.POST)
				x = (request.POST.get('accept'))
				acc_comment_id = Comments.objects.get(commentID=request.POST.get('accepted_cmnt'))
				if(x == '0'):
					vote = Accept_Reject(commentID = acc_comment_id, userID = user, accept = 0, reject = 1)
				else:
					vote = Accept_Reject(commentID = acc_comment_id, userID = user, accept = 1, reject = 0)
				vote.save()

		except:
			pass
		
		try:
			if(request.POST['undo_cmnt']):
				undo_cmnt = (request.POST.get('undo_cmnt'))
				x = Accept_Reject.objects.get(commentID=undo_cmnt, userID= user)
				x.delete()
		except:
			pass

	# If this is a GET (or any other method) create the default form.
	print("here")
	doc = Documents.objects.filter(docID=id,version=version)
	#docObj = Documents.objects.get(docID=id,version=version)
	x = 0
	for x in doc:
		pass
	ReviewerName = None
	approved = False
	if(x.approve == True):
		Reviewer = User_Document.objects.get(docID__docID =id,ROLE="REVIEWER")
		ReviewerName = Reviewer.LOGIN_ID.name
		approved = True
	approvedDiffVersion = None
	docObjs = Documents.objects.filter(docID=id)
	for aDoc in docObjs:
		if (aDoc.approve==True):
			if(aDoc!=x):
				approvedDiffVersion = aDoc.version
				break
	comment = Comments.objects.filter(docID=id).order_by('-commentID')
	replies = []
	votes = []
	voted_comments = []
	p_voted=[]
	personal_votes=Accept_Reject.objects.filter(userID=user)
	t=Accept_Reject.objects.all().values('commentID')
	temp = personal_votes.values('commentID')
	for pv in temp:
		p_voted.append(pv['commentID'])
	for j in t:
		voted_comments.append(j['commentID'])
	for i in comment:
		reply = Reply.objects.filter(commentID=i.commentID)
		vote = Accept_Reject.objects.filter(commentID=i.commentID)
		replies.append(reply)
		#print("VOTESSS")
		#print(vote)
		votes.append(vote)
		#print(votes)
	flag = 0
	for i in doc:
		flag = i.lock
	if(flag==0):
		bla = Documents.objects.filter(docID=id,version=version).update(lock=1)
		lockingUser = LatestVersion.objects.filter(docVersionID__docID = i.docID).update(lockUser = user)
	latestVersion = LatestVersion.objects.filter(docVersionID__docID = i.docID)
	for x in latestVersion:
		pass
	#print(x.lockUser.LOGIN_ID)
	lUsername = ""
	if(x.lockUser):
		lUsername = x.lockUser.LOGIN_ID
	print(LOGIN_ID)
	print("done")
	print(approvedDiffVersion)
	context = { 'document':doc, 
				'latestVersion' : x.latestVersion, 
				'lockedUser' : lUsername,
				'lock':flag, 
				'LOGIN_ID': LOGIN_ID, 
				'comment': comment, 
				'replies':replies, 
				'votes':votes, 
				'personal_votes':personal_votes,
				'personal_v':p_voted,
				'voted_comments':voted_comments,
				'role':role,
				'ReviewerName':ReviewerName,
				'approved':approved,
				'approvedDiffVersion':approvedDiffVersion }
	return render(request,'editor_page.html', context=context )




def ReadonlyView(request,LOGIN_ID,id,version):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		print("here1")
		#next = request.POST.get('next', '/')
		#return HttpResponseRedirect(next)
		
	# If this is a GET (or any other method) create the default form.
	else:
		print("here")
		doc = Documents.objects.get(docID=id,version=version)
		latestVersion = LatestVersion.objects.filter(docVersionID__docID = doc.docID)
		for x in latestVersion:
			pass
		print("done")
		context = {'document':doc, 'latestVersion' : x.latestVersion}
		return render(request,'documents.html', context=context)



# Create your views here.
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		if form.is_valid():
			LOGIN_ID = request.POST.get('LOGIN_ID')
			PASSWORD = request.POST.get('PASSWORD')
			
			try:
				if models.Users.objects.get(pk=LOGIN_ID).PASSWORD == PASSWORD:
					print(LOGIN_ID+'/data')
					return redirect(reverse('data', kwargs={'LOGIN_ID':LOGIN_ID}))
				else:
					return render(request, 'mainpage.html', {"error":"Wrong Credentials. Login again"})
					print('\nwrong credentials\n')
					form = LoginForm()
					
			except Exception as e:
				#raise forms.ValidationError('Looks like a username with that email or password already exists')
				print('\n', e, '\nwrong credentials\n')
				form = LoginForm()
				return render(request, 'mainpage.html', {"error":"Something went wrong. Login again"})
	"""
	else:
		form = LoginForm()
	"""
	return render(request, 'mainpage.html')


def data(request, LOGIN_ID):
	COLLABORATOR, REVIEWER = [], []
	lis=[]
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='COLLABORATOR'):
		lis = models.Documents.objects.filter(docID=i.docID.docID)
		#print("LISSSSSSSSSS",lis)
		COLLABORATOR.append(lis)
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='REVIEWER'):
		lis = models.Documents.objects.filter(docID=i.docID.docID)
		REVIEWER.append(lis)
	context = {'COLLABORATOR' : COLLABORATOR, 'REVIEWER':REVIEWER, 'LOGIN_ID':LOGIN_ID}
	return render(request, 'landing.html', context)

def createDoc(request, LOGIN_ID):
	if request.method == 'POST':
		#print("where are youuuuuu")
		items=[None]*5
		for key,value in request.POST.items():   #loop through the entire post fields 
				if(key=="csrfmiddlewaretoken"):
					items[0]=value
					print(key,value)
				elif(key=="docname"):
					items[1]=value
					print(key,value)
				elif(key=="opt"):
					items[2]=value
					print(key,value)
				elif(key=="reviewer"):
					items[3]=value
					print(key,value)
				elif(key=="collaborator1"):
					items[4]=value
					print(key,value)

		print("item list:", items)
		#print("where are youuuuuu")
		docname = request.POST.get('docname')   #getdocname
		choice = request.POST.get('opt')         #ask if user wants to be reviewer or collaborator
		index=0
		collablist = [] 
		if choice == "collaborator" :
			reviewer = request.POST.get('reviewer')  #getreviewer
			try:
				rev = models.Users.objects.get(pk=reviewer)   #extract reviewer detail
				collablist.append(models.Users.objects.get(pk=LOGIN_ID))
				index=4
			except:
				return render(request, 'createnew.html', {'LOGIN_ID':LOGIN_ID,"error":"Wrong reviewer User ID"})
		else:
			index=4
			reviewer=LOGIN_ID
			rev=models.Users.objects.get(pk=LOGIN_ID)
		'''
		items=[]
		for key,value in request.POST.items():   #loop through the entire post fields 
				items.append(value)
				print(key,value)
		print("item list:", items)'''
		collaborator=list(set(items[index:])) #skip first 'index' fields and select only unique collaborators fields

		print(len(collaborator),collaborator)

		if reviewer in collaborator:   #if reviewer and collaborator are same 
			print("here")
			return render(request, 'createnew.html', {'LOGIN_ID':LOGIN_ID,"error":"same reviewer and collaborator"})
		#print(items)
		#print(collaborator)
		try:
			if not(collaborator==[""] and choice=="collaborator"):

				for x in collaborator:  
					try:
						print(x)
						i = models.Users.objects.get(pk=x) #if collaborator exists
						collablist.append(i)		
					except:  #throws exception when user doesnt exist
						print('\nwrong credentials\n')
						return render(request, 'createnew.html', {'LOGIN_ID':LOGIN_ID,"error":"Wrong collaborator User ID"})
					
				#else:
			doc=Documents(docname=docname,content={})
			doc.save()
			latestttt = LatestVersion(docVersionID=doc, latestVersion=1.0)
			latestttt.save()
			
			
			addRev = User_Document(LOGIN_ID=rev, docID=doc, ROLE = 'REVIEWER' )
			addRev.save()

			for i in collablist:
					print("3")
					addCollab = User_Document(LOGIN_ID=i, docID=doc, ROLE = 'COLLABORATOR')
					print("4")
					addCollab.save()
					
			return redirect(reverse('data', kwargs={'LOGIN_ID':LOGIN_ID}))
				
		except Exception as e:
			return render(request, 'createnew.html', {'LOGIN_ID':LOGIN_ID,"error":e})

	return render(request, 'createnew.html',{'LOGIN_ID':LOGIN_ID})

def signUp(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		print(5)
		form = signUpForm(request.POST)
		print(6)
		
		if form.is_valid():
			print(7)
			LOGIN_ID = request.POST.get('LOGIN_ID')
			PASSWORD = request.POST.get('PASSWORD')
			email=request.POST.get('email')
			name =request.POST.get('name')
			institution = request.POST.get('institution')
			profession = request.POST.get('profession')
			print(LOGIN_ID,PASSWORD,email,name,institution,profession)
			try:
				if models.Users.objects.get(pk=LOGIN_ID):  #if username already exists
					print("user already exists\n")
					form =signUpForm()
					return render(request, 'mainpage.html', {"error":"User already exists.Sign in again."})
					
			except Exception as e:
				print(1)
				newUser = Users(LOGIN_ID=LOGIN_ID,PASSWORD=PASSWORD,email=email,name=name,institution=institution,profession=profession)
				print(2)
				newUser.save()
				return redirect(reverse('data', kwargs={'LOGIN_ID':LOGIN_ID}))

	else:
		print(3)
		form =signUpForm()
		return render(request, 'mainpage.html', {"error":"Wrong credentials. Please sign in again."})
		

	#return render(request, 'mainpage.html')
