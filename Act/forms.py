
from .models import Notification,Act,NotificationState,SubActComments,ScreenImage
from django import forms
from django.forms import ModelForm

class InputDatetimeWidget(forms.Widget):
    def render(self,name, value, attrs=None, renderer=None):
        sv=value.strftime("%Y-%m-%dT%H:%M:%S")
        return f"<input type='datetime-local' name='{name}' class='ObjectPeriod'  value='{sv}' step='1'>"

class ReadOnlyText(forms.TextInput):
    input_type = 'text'
    def render(self,name, value, attrs=None, renderer=None):
        if value is None: 
            value = ''
        return value


class NotificationFormObject(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NotificationFormObject, self).__init__(*args, **kwargs)

    class Meta:
        model = Notification
        fields = '__all__'
        widgets = {
            "period":InputDatetimeWidget,
        }

class ActFormObject(ModelForm):
    shadow_pk = forms.CharField(widget=ReadOnlyText, label='Id',required=False)
    class Meta:
        model = Act
        fields = '__all__'
        widgets = {
            "period":InputDatetimeWidget,
            "shadow_pk":ReadOnlyText,
        }
    def as_div(self):
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)
    def as_separate_full_form(self):
        return "\
        <div class='div_act'> "+\
            self.as_div()+"\
            <div><button type='button' onclick='addComment({{act_data.pk}},this)'>Add</button></div>\
            </div>\
            <div class='actComments' id='actComments"+str(self['pk'].value())+"'>\
            </div>\
            <div style='width:100%;height:10px;background:orange;'></div>"


class SubActCommentsFormObject(ModelForm):
    shadow_pk = forms.CharField(widget=ReadOnlyText, label='Id',required=False)
    class Meta:
        model = SubActComments
        fields = '__all__'
        widgets = {
            "period":InputDatetimeWidget,
        }

    def as_div(self):
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)

    def as_separate_full_form(self):
        return self.as_div()












