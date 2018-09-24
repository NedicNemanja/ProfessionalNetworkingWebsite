from django.contrib import admin
from .models import *
from django.template.loader import render_to_string
from django.http import HttpResponse


# Export method
def export_xml(modeladmin, request, queryset):
    template_name = 'PNapp/xml_template.xml'
    users = queryset
    xml = render_to_string(template_name, {'users': users})
    myFile = open("FinalXML.xml", "w")
    myFile.write(xml)
    myFile.close()
    myFile = open("FinalXML.xml", "r")
    response = HttpResponse(myFile, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=FXML.xml'
    return response

export_xml.short_description = u"Export XML"

# Admin's model
class MyModelAdmin(admin.ModelAdmin):
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
