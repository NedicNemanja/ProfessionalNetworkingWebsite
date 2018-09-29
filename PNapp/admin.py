from django.contrib import admin
from .models import *
from django.template.loader import render_to_string
from django.http import HttpResponse



class ConversationAdmin(admin.ModelAdmin):
    list_display = ('creator', 'receiver', 'creation_date')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('creator', 'text', 'creation_date', 'conversation')

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('creator', 'receiver', 'accepted')

class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'creator', 'creation_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'creator', 'post_id', 'creation_date')

class InterestAdmin(admin.ModelAdmin):
    list_display = ('creator', 'post', 'creation_date')

class AdvertismentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'details' ,'creation_date')

# Export method
def export_xml(modeladmin, request, queryset):
    # xml template that will be used
    template_name = 'PNapp/xml_template.xml'
    # users that have been checked from admins page to be exported
    users = queryset
    #render them into the template
    xml = render_to_string(template_name, {'users': users,})
    #create a new file or overwrite the existing one
    myFile = open("FinalXML.xml", "w")
    #write in there the xml template
    myFile.write(xml)
    myFile.close()
    #open it again
    myFile = open("FinalXML.xml", "r")
    #and send it back as response to the admin's action
    response = HttpResponse(myFile, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=FXML.xml'
    return response

# Export XML will be the name of the action admin will see
export_xml.short_description = u"Export XML"

# Admin's model
class MyModelAdmin(admin.ModelAdmin):
    #add to admins action our new function
    actions = [export_xml]
    list_display = ('id', 'email', 'email_public', 'password', 'name', 'surname', 'phone', 'phone_public', 'profile_photo', 'university', 'university_public', 'degree_subject', 'degree_subject_public',
    'company', 'company_public', 'position', 'position_public')

# Register your models here.
admin.site.register(User, MyModelAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Skill)
admin.site.register(Advertisment, AdvertismentAdmin)