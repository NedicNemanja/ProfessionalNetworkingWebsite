from django.contrib import admin
from .models import *
from django.template.loader import render_to_string
from django.http import HttpResponse

# class InterestAdmin(admin.ModelAdmin):
#     list_display = ('creator', 'post', 'creation_date')

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

# Register your models here.
admin.site.register(User, MyModelAdmin)
admin.site.register(Post)
admin.site.register(Connection)
admin.site.register(Comment)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Interest)
admin.site.register(Skill)
admin.site.register(Advertisment)