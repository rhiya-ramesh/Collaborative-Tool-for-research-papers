from django.urls import path
from . import views
from django.conf.urls import url
from Collab_Docs.views import *

urlpatterns = [
    #url(r'^$', views.HomePageView.as_view()),
    path('suggest/title', views.suggest, name ='suggest'),
    path('summarize/intelligent_component', views.summarize, name='summ'),
    path('ajax/accept/<LOGIN_ID>/<id>/<version>/<role>', views.EditorView, name ='vote'),
    path('documents', views.DocumentView, name='documents'),
    path('documents/<LOGIN_ID>/<id>/<version>/<role>', views.EditorView, name='editor'),
    path('documents/<LOGIN_ID>/<id>/<version>/r', views.ReadonlyView, name='readonly'),
    path('<LOGIN_ID>',data, name='data'),
    path('createDoc/<LOGIN_ID>',createDoc, name='new'),
	path('',login, name='login'),
    path('signup/',signUp, name='signUp')
]
"""

"""
