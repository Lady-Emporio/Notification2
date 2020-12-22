from django.shortcuts import render

from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime
from django.db import connection
from django.http import JsonResponse

from django.core import serializers
import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.forms import Textarea
from .models import Notification,Act,SubActComments,ScreenImage
from .views_functions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .forms import NotificationFormObject, ActFormObject,SubActCommentsFormObject
from django.shortcuts import redirect
from django.http import HttpResponse

from .sky import openNotificationFullObject_GET,openNotificationFullObject_POST

@csrf_exempt
def showNotification(request,IsFilter):
    sqlText="""
    SELECT 
        q.nId as nId,
        q.nName as nName,
        q.NBegin as nBegin,
        q.NBegin as nIsActive,
        q.aId as aId,
        q.aName as aName,
        q.aParent as aParent,
        q.aState as aState,
        q.aState as aIsActive,
        s.name as sName,
        s.id as sId,
        s.red as sRed,
        s.green as sGreen,
        s.blue as sBlue,
        s.background_red as sBackground_red,
        s.background_green as sBackground_green,
        s.background_blue as sBackground_blue,

        h.period as hPeriod,
        h.id as hId,
        h.act as hAct,
        h.state as hState,
        sh.id as shId,
        sh.name as shName,
        sh.red as shRed,
        sh.green as shGreen,
        sh.blue as shBlue,
        sh.background_red as shBackground_red,
        sh.background_green as shBackground_green,
        sh.background_blue as shBackground_blue

        FROM (
        SELECT 
        n.id as nId,
        n.name as nName,
        n.begin as nBegin,
        n.isActive as nIsActive,
        a.id as aId,
        a.name as aName,
        a.parent as aParent,
        a.state as aState,
        a.isActive as aIsActive
        FROM Notification as n
        JOIN Act  as a ON a.parent=n.id

        UNION ALL 

        SELECT 
        n.id,
        n.name,
        n.begin,
        n.isActive,
        null,
        null,
        null,
        null,
        null
        FROM Notification as n 
        WHERE NOT EXISTS 
        ( SELECT 1 FROM act as a WHERE a.parent = n .id) 

        UNION ALL

        SELECT 
        null,
        null,
        null,
        null,
        a.id,
        a.name,
        a.parent,
        a.state,
        a.isActive
        FROM act as a WHERE NOT EXISTS ( SELECT 1 FROM Notification as n WHERE a.parent = n .id)

        ) as q

        left join NotificationState as s on q.aState=s.id
        left join NotificationHistory as h on h.act=q.aId
        left join NotificationState as sh on h.state=sh.id
        
        WHERE 1 
            [f1]
            [f2]
            [f3]

        ORDER BY nId, aId,h.period DESC
        """
    sqlText=sqlText.replace("[f1]"," AND (q.nIsActive or q.aIsActive) ")
    sqlText=sqlText.replace("[f2]","")
    sqlText=sqlText.replace("[f3]","")


    data=[]
    with connection.cursor() as c:
        c.execute(sqlText)
        result=c.fetchall()

        colNombers={}
        for i in range(len(c.cursor.description)):
            colNombers[c.cursor.description[i][0]]=i

        

        LastNotId=-1
        LastActId=-1

        for row in result:

            if  LastNotId==row[colNombers["nId"]]:
                #Продолжается эта группа. Может быть новая задача в этой строке или новая история.
                if LastActId==row[colNombers["aId"]]:
                    # просто новая история
                    if "active"!=IsFilter:
                        saveHistory(data,colNombers,row)
                else:
                    #Просто новая задача
                    LastActId=row[colNombers["aId"]]
                    createNewQuest(data,colNombers,row)
                    if "active"!=IsFilter:
                        saveHistory(data,colNombers,row)
            else:
                #Новая группа
                LastNotId=row[colNombers["nId"]]
                createNewGroup(data,colNombers,row)
                LastActId=row[colNombers["aId"]]
                createNewQuest(data,colNombers,row)
                if "active"!=IsFilter:
                    saveHistory(data,colNombers,row)

    return render(request,"mainPage.html",{"content":data,"filter":IsFilter})

def openListNotification(request):
    contact_list = Notification.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        listObjects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        listObjects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        listObjects = paginator.page(paginator.num_pages)
        
    return render(request, "notification/notificationList.html", {'listObjects': listObjects})

def openNotificationFullObject(request,pk):
    if request.method == "POST":
        return openNotificationFullObject_POST(request,pk)
    if request.method == 'GET':
        return openNotificationFullObject_GET(request,pk)
    else:
        return HttpResponse("method not supported")


def api_AddComment(request):
    if request.method != "POST":
        return HttpResponse("method not supported")
    json_string=request.body.decode(errors="ignore");
    data = json.loads(json_string)
    id=data["pk"]
    act = get_object_or_404(Act, pk=id)
    actCom=SubActComments(act=act)
    actCom.save()
    prefixActComment=f"factComment_{actCom.pk}_"
    formAc=SubActCommentsFormObject(instance=actCom,prefix=prefixActComment,initial={"shadow_pk":actCom.pk})
    return HttpResponse(formAc.as_div())

def api_AddAct(request):
    if request.method != "POST":
        return HttpResponse("method not supported")
    json_string=request.body.decode(errors="ignore");
    data = json.loads(json_string)
    id=data["pk"]
    notif = get_object_or_404(Notification, pk=id)
    NewAct=Act(parent=notif)
    NewAct.save()
    prefixA=f"fact_{NewAct.pk}_"
    formAc=ActFormObject(instance=NewAct,prefix=prefixA,initial={"shadow_pk":NewAct.pk})
    return HttpResponse(formAc.as_separate_full_form())

def api_AddImage(request):
    if request.method != "POST":
        return HttpResponse("method not supported")
    json_string=request.body.decode(errors="ignore");
    data = json.loads(json_string)
    id=data["pk"]
    image_base64=data["image_base64"]
    if not image_base64.startswith("data:image/png;base64,"):
        return HttpResponse("Not 'data:image/png;base64,'.") 
    notif = get_object_or_404(Notification, pk=id)
    si=ScreenImage(parent=notif)
    si.image_base64=image_base64;
    si.save()
    return HttpResponse("Twilight")


def createNotificationFullObject(request):
    message=""
    if request.method == "POST":
        formNot=NotificationFormObject(request.POST, request.FILES,prefix="newNot")
        if formNot.is_valid():
            newNot=formNot.save()
            return HttpResponseRedirect(newNot.get_form_url()) 
        else:
            message="Not valid !!!!!!!!!!!!!!!!!!"
            return render(request, "notification/FullForm.html", {
            'form': formNot,
            "acts":[],
            "message":message,
            })
    formNot=NotificationFormObject(prefix="newNot")
    return render(request, "notification/FullForm.html", {
            'form': formNot,
            "acts":[],
            "message":message,
            })


















