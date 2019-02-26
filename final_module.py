import apiai
import os
import dialogflow
import requests
import json
import pusher
from pymongo import MongoClient
import json, pprint
import urllib.request
import urllib.parse
import requests
import time




client1 = MongoClient()
client1 = MongoClient('localhost', 27017)
db = client1.gov_data
result1= db.policies.find({})
# print(result1)
description_list=[]
link_list=[]
document_list=[]
number1=0

while(True):

    Access_token ="0f8f425da1e94bf898d4cb65de3ced33"
    client=apiai.ApiAI(Access_token)
    with open('sessions.json', 'r') as f:
            print("yes opened")
            session = json.load(f)

    def get_context(message, number):
        req=client.text_request()
        print(req)
        req.lang="de"
        # req.session_id= response["sessionId"]
        req.query=message
        
        # print(response)
        
        

        with open('sessions.json', 'r') as f:
            print("yes opened")
            data = json.load(f)
            flag=0
            for i in range(0,len(data["sessionId"])):

                if str(number)==str(data["phoneNo"][i]):
                    print("in if")
                    print(str(number)+":"+str(data["phoneNo"][i]))
                    req.session_id=data["sessionId"][i]
                    myreq=req.getresponse().read().decode('utf-8')
                    response=json.loads(myreq)
                    flag=1
                    break
            if(flag==0):
                print(str(number)+":"+str(data["phoneNo"][i]))
                print("else")
                myreq=req.getresponse().read().decode('utf-8')
                response=json.loads(myreq)
                
                req.session_id= response["sessionId"]
                
                
                
                with open('sessions.json', 'w') as outfile:
                    session["sessionId"].append(response["sessionId"])
                    session["phoneNo"].append(number)
                    print("yes writing")
                    json.dump(session,outfile)
        

        print(req.session_id)

        
        
        responseStatus = response['status']['code']
        print(responseStatus)
        if responseStatus==200 or 206 :
            print(response['result']['fulfillment']['speech'])
            message1= response['result']['fulfillment']['speech']

            k=1
            l=1
            n=1
            flag=0
            if 'Policy' in response['result']['parameters']:
                description_list.clear()
                link_list.clear()
                document_list.clear()
                for i in range(0, 20):
                
                    if(response['result']['parameters']['Policy'].lower() in [i.lower() for i in result1[i]['keywords']]):
                        # print(result1[i]["Title"])
                        message1+=" "+str(k)+" :"+(result1[i]["Title"])
                        description_list.insert(k, result1[i]["Description"])
                        link_list.insert(n, result1[i]["Links"])

                        
                        document_list.insert(l, result1[i]["docs"])
                        l+=1
                        flag=1
                        k+=1
                        n+=1
                        # print(document_list)

                        
                        
                        # print(description_list)

            elif 'number' in response['result']['parameters']:
                global number1
                # print(response['result']['parameters']['number'])
                number1 = response['result']['parameters']['number']
                print(number1)
                # print(description_list)
                try:
                    message1+=""+description_list[int(response['result']['parameters']['number'])-1]
                except:
                    print("out of range but kek")

            elif 'links' in response['result']['parameters']:
                
                try:
                    print(number1)
                    print(response['result']['parameters']['links'])
                    message1+=link_list[int(number1)-1]
                except:
                    print("out of range but kek")



            elif 'documents' in response['result']['parameters']:
                print(response['result']['parameters']['documents'])
                print(document_list)
                print(number1)
                for i in range(0, len(document_list)):
                    if i==(int(number1)-1):
                        for j in range(0,len(document_list[i])):
                            message1+=" "+str(j+1)+" : "+ document_list[i][j]
                            print(message1)
                        
                
                # print("out of range but kek")

        

            print(message1)
            hi1 =sendSMS('7JppUgkDJCY-kr4NbUxPxwc8G76PqG9EYSvgPPB2hq', number,'TXTLCL', ''+message1)
            print(hi1)
            print("message sent")
        else:
            print("error")
    

    def sendSMS(apikey, numbers, sender, message):
        data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
            'message' : message, 'sender': sender})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return(fr)


    def getInboxes(apikey):
        data =  urllib.parse.urlencode({'apikey': apikey})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/get_inboxes/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return(fr)
    
    resp =  getInboxes('7JppUgkDJCY-kr4NbUxPxwc8G76PqG9EYSvgPPB2hq')
    # print (resp)

    def getMessages(apikey, inboxID):
        data =  urllib.parse.urlencode({'apikey': apikey, 'inbox_id' : inboxID})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/get_messages/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        hi = json.loads(fr.decode('utf-8'))
        # print(hi)
        data={"id": []}
        for i in range(0, len(hi['messages'])):
            y = hi['messages'][i]['message'].replace('C6A3Q','')
            
            # print(hi["messages"][i]["number"])
            # print(hi["messages"][i]["id"])
            

            with open('id.json') as f:
                data = json.load(f)
                # print(data["id"])
                if hi["messages"][i]["id"] not in data["id"]:
                    print("true")
                    
                    get_context(hi['messages'][i]['message'], hi["messages"][i]["number"])
                    data["id"].append(hi["messages"][i]["id"])
                    with open('id.json', 'w') as outfile:
                    
                        json.dump(data,outfile)
                    
            print(hi['messages'][i]['number'], y)
        return(fr)


    resp =  getMessages('7JppUgkDJCY-kr4NbUxPxwc8G76PqG9EYSvgPPB2hq', '10')
    time.sleep(10)
    # print(resp)