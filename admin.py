from django.contrib import admin

# Register your models here.

from Collab_Docs.models import Users, Documents, User_Document, LatestVersion, Comments, Reply, Accept_Reject, Title

admin.site.register(Users)
admin.site.register(Documents)
admin.site.register(User_Document)
admin.site.register(LatestVersion)
admin.site.register(Comments)
admin.site.register(Reply)
admin.site.register(Accept_Reject)
admin.site.register(Title)

