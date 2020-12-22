

def getThisGroup(data):
    return data[-1]

def getThisQuest(data):
    return data[-1]["acts"][-1]

def createNewGroup(data,colNombers,row):
    GroupData={
            "nId":row[colNombers["nId"]],
            "nName":row[colNombers["nName"]],
            "nBegin":row[colNombers["nBegin"]],
            "nIsActive":row[colNombers["nIsActive"]],
            "acts":[],
        }
    data.append(GroupData)

def createNewQuest(data,colNombers,row):
    GroupData=getThisGroup(data)

    questData={

            "aId":row[colNombers["aId"]],
            "aName":row[colNombers["aName"]],
            "aParent":row[colNombers["aParent"]],
            "aState":row[colNombers["aState"]],
            "aIsActive":row[colNombers["aIsActive"]],
            "sName":row[colNombers["sName"]],
            "sId":row[colNombers["sId"]],
            "history":[],
    }
    for i in ["Red","Green","Blue"]:
        val=row[colNombers["s"+i]]
        questData[i]=val if val!=None else 255

    for i in ["Background_red","Background_green","Background_blue"]:
        val=row[colNombers["s"+i]]
        questData[i]=val if val!=None else 0

    GroupData["acts"].append(questData)

def saveHistory(data,colNombers,row):
    historyData={
            "period":row[colNombers["hPeriod"]],
            "state":row[colNombers["shName"]],
    }

    for i in ["Red","Green","Blue"]:
        val=row[colNombers["sh"+i]]
        historyData[i]=val if val!=None else 255

    for i in ["Background_red","Background_green","Background_blue"]:
        val=row[colNombers["sh"+i]]
        historyData[i]=val if val!=None else 0

    nowQuetst=getThisQuest(data)
    nowQuetst["history"].append(historyData)
