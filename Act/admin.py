from django.contrib import admin	
from .models import *	

class NotificationStateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',"red","green","blue","background_red","background_green","background_blue"]

admin.site.register(NotificationState,NotificationStateAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',"isActive","begin"]
    ordering = ['begin',"id"]
    actions = []

admin.site.register(Notification,NotificationAdmin)	

class SubActHistoryInline(admin.TabularInline):
	model = ActHistory
	extra= 0

class SubActCommentsInline(admin.TabularInline):
	model = SubActComments
	extra= 0

class ActAdmin(admin.ModelAdmin):	
	list_display = ("id","name","parent","period","state","isActive","comment")
	list_display_link = ("id")
	search_fields = ("name","parent__name")
	list_filter = ("state","period","isActive")
	save_as =True #replace Save and add another
	ordering = ['id']
	inlines = [
		SubActCommentsInline,
        SubActHistoryInline,
    ]
	save_on_top=True

admin.site.register(Act,ActAdmin)	


admin.site.register(HistorySubActComments)

from django import forms

class ShadowImageWidget(forms.Widget):
    def render(self,name, value, attrs=None, renderer=None):
        return f" <image src='{value}'>"


class StopAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StopAdminForm, self).__init__(*args, **kwargs)
        self["shadow_image_base64"].initial=self["image_base64"].value()

    shadow_image_base64 = forms.CharField(widget=ShadowImageWidget, label='Image',required=False)
    class Meta:
        model = ScreenImage
        widgets = {
        'shadow_image_base64': ShadowImageWidget(),
        }
        fields = '__all__'

class ScreenImageAdmin(admin.ModelAdmin):
	form = StopAdminForm
    #list_display = ['id', 'parent',"image_base64","period"]

admin.site.register(ScreenImage,ScreenImageAdmin)
