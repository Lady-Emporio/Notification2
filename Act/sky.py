

from .forms import NotificationFormObject, ActFormObject,SubActCommentsFormObject
from django.shortcuts import redirect,render
from django.shortcuts import get_object_or_404
from .models import Notification,Act,SubActComments,ScreenImage

def openNotificationFullObject_GET(request,pk):
    n = get_object_or_404(Notification, pk=pk)
    acts=Act.objects.filter(parent=n)
    images=ScreenImage.objects.filter(parent=n)
    prefixNot=f"fnot_{pk}_"
    message=""

    formNot=NotificationFormObject(instance=n,prefix=prefixNot)
    actsDataForms=[]

    for a in acts:
        prefixA=f"fact_{a.pk}_"
        actform=ActFormObject(instance=a,prefix=prefixA,initial={"shadow_pk":a.pk})
        actComments=SubActComments.objects.filter(act=a)
        listComments=[]
        for ac in actComments:
            prefixActComment=f"factComment_{ac.pk}_"
            lac=SubActCommentsFormObject(instance=ac,prefix=prefixActComment,initial={"shadow_pk":ac.pk})
            listComments.append(lac)
        actsDataForms.append({
            "actform":actform,
            'pk': pk,
            "listComments":listComments,
            "pk":a.pk,
            })
    return render(request, "notification/FullForm.html", {
            'pk': pk,
            'form': formNot,
            "acts":actsDataForms,
            "message":message,
            "images":images,
            })


def openNotificationFullObject_POST(request,pk):
    n = get_object_or_404(Notification, pk=pk)
    acts=Act.objects.filter(parent=n)
    images=ScreenImage.objects.filter(parent=n)
    
    prefixNot=f"fnot_{pk}_"
    message=""

    formNot=NotificationFormObject(request.POST, request.FILES,instance=n,prefix=prefixNot)
    actsDataForms=[]

    for a in acts:
        prefixA=f"fact_{a.pk}_"
        actform=ActFormObject(request.POST, request.FILES,instance=a,prefix=prefixA,initial={"shadow_pk":a.pk})
        actComments=SubActComments.objects.filter(act=a)
        listComments=[]
        for ac in actComments:
            prefixActComment=f"factComment_{ac.pk}_"
            lac=SubActCommentsFormObject(request.POST, request.FILES,instance=ac,prefix=prefixActComment,initial={"shadow_pk":ac.pk})
            listComments.append(lac)
        actsDataForms.append({
            "actform":actform,
            'pk': pk,
            "listComments":listComments,
            "pk":a.pk,
            "images":images,
            })


    twilight=True
    if not formNot.is_valid():
        message+="Notification not valid\n"
        twilight=False
    for a_data in actsDataForms:
        if not a_data["actform"].is_valid():
            message+="aform not valid\n"
            twilight=False
        for acomform in a_data["listComments"]:
            if not acomform.is_valid():
                message+="a com form not valid\n"
                twilight=False
    if twilight:
        formNot.save()
        for a_data in actsDataForms:
            a_data["actform"].save()
            for acomform in a_data["listComments"]:
                acomform.save()
        return redirect('.') 
    return render(request, "notification/FullForm.html", {
            'form': formNot,
            'pk': pk,
            "acts":actsDataForms,
            "message":message,
            "images":images,
            })