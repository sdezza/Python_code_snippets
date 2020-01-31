import pandas as pd
import numpy as np
import csv  
import sys
import json
import urllib.request
import urllib.parse
import http.client

headers={"Content-Type":"application/json",
        "Trackingmore-Api-Key":"KEY",
        'X-Requested-With':'XMLHttpRequest'
        }

class track:

    def trackingmore(requestData, urlStr, method):

        if method == "get":

            url = 'http://api.trackingmore.com/v2/trackings/get'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl, headers=headers)
            result = urllib.request.urlopen(req).read()

        elif method == "post":

            url = 'http://api.trackingmore.com/v2/trackings/post'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "batch":

            url = 'http://api.trackingmore.com/v2/trackings/batch'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "codeNumberGet":

            url = 'http://api.trackingmore.com/v2/trackings'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="GET")
            result = urllib.request.urlopen(req).read()

        elif method == "codeNumberPut":

            url = 'http://api.trackingmore.com/v2/trackings'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="PUT")
            result = urllib.request.urlopen(req).read()

        elif method == "codeNumberDelete":

            url = 'http://api.trackingmore.com/v2/trackings'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="DELETE")
            result = urllib.request.urlopen(req).read()

        elif method == "realtime":

            url = 'http://api.trackingmore.com/v2/trackings/realtime'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "carriers":

            url = 'http://api.trackingmore.com/v2/carriers'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="GET")
            result = urllib.request.urlopen(req).read()

        elif method == "carriers/detect":

            url = 'http://api.trackingmore.com/v2/carriers/detect'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="GET")
            result = urllib.request.urlopen(req).read()

        elif method == "update":

            url = 'http://api.trackingmore.com/v2/trackings/update'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "getuserinfo":

            url = 'http://api.trackingmore.com/v2/trackings/getuserinfo'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="GET")
            result = urllib.request.urlopen(req).read()

        elif method == "getstatusnumber":

            url = 'http://api.trackingmore.com/v2/trackings/getstatusnumber'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="GET")
            result = urllib.request.urlopen(req).read()

        elif method == "notupdate":

            url = 'http://api.trackingmore.com/v2/trackings/notupdate'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "remote":

            url = 'http://api.trackingmore.com/v2/trackings/remote'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "costtime":

            url = 'http://api.trackingmore.com/v2/trackings/costtime'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "delete":

            url = 'http://api.trackingmore.com/v2/trackings/delete'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        elif method == "updatemore":

            url = 'http://api.trackingmore.com/v2/trackings/updatemore'
            RelUrl = url + urlStr
            req = urllib.request.Request(RelUrl,requestData.encode('utf-8'), headers=headers,method="POST")
            result = urllib.request.urlopen(req).read()

        return result

# Get SAP DL DataFrame
df = pd.read_csv('FILE.txt', sep='|', skiprows=4).drop(['Unnamed: 0'],axis=1)
df.columns = df.columns.str.strip()
df["Status"] = ""


df = df[['Delivery','Name 1','Bill of lading', 'Status']]
df.columns = ['Delivery', 'Ship-to', 'carrier', 'Bill of lading', 'Status']
# To do once:
df.to_csv('tracking.csv', index=False, header=True)

print("Getting batch job..")
# Get Tracking built DataFrame and compare with initial df
df_tracking = pd.read_csv('tracking.csv', sep=',', encoding='latin-1')

existingDl = [line for line in df_tracking['Delivery']]


new = []
for row in df.iterrows():
    dl = row[1]['Delivery']
    if dl not in new and dl not in existingDl:
       new.append(dl)
    
# Write the added lines in file 
df_new = df[df['Delivery'].isin(new)] 
with open('tracking.csv', 'a', encoding='utf-8') as f:
    df_new.to_csv(f, header=False, index=False)

print("Writing new lines into tracking file...")

def f(row):
    global result

    if row['Status'] == 'delivered':
        print(row['Delivery'] + ' - no touch')
        pass

    elif pd.isna(row['Status']):
        print(row['Delivery'] + " - Status vide")
        try:
            row['Bill of lading'] = int(row['Bill of lading'])
        except ValueError:
            print(row['Delivery'] + " - Mauvais tracking")
            return "nop"

        # if no status, create it in dashboard 
        if pd.isna(row['Bill of lading']) :
            result = "Invalid Tracking"
            print(row['Delivery'] & " - déja, pas de tracking....")
        else:
            print("ddd")
            tracking = row['Bill of lading']
            carrier = "TNT"
            urlStr = ""
            requestData = "{\"tracking_number\": \""+str(tracking)+"\",\"carrier_code\":\""+carrier+"\",\"title\":\"test\"}"
            result = track.trackingmore(requestData, urlStr, "post")
            data = json.loads(result)
            print(row['Delivery'] + ' - Connection...')

            # code 4016, tracking already created
            if data['meta']['code'] == 4016:
                #5 Get tracking results of a single tracking.
                urlStr = "/TNT/"+str(tracking)+"/"
                requestData = ""
                result = track.trackingmore(requestData, urlStr, "codeNumberGet")
                data = json.loads(result)
                result = data['data']['status']
                print(row['Delivery'] + ' - Already created')

            # code 200, tracking successfully created
            elif data['meta']['code'] == 200:
                #5 Get tracking results of a single tracking.
                urlStr = "/TNT/"+str(tracking)+"/"
                requestData = ""
                result = track.trackingmore(requestData, urlStr, "codeNumberGet")
                data = json.loads(result)
                result = data['data']['status']
                print(row['Delivery'] & ' - Created')
            else:
                result = data['meta']['message']
                


    else:
        # If a status different than Delivered, update it
        #5 Get tracking results of a single tracking.
        carrier = "TNT"
        tracking = row['Bill of lading']
        urlStr = "/"+carrier+"/"+str(tracking)+"/"
        requestData = ""
        result = track.trackingmore(requestData, urlStr, "codeNumberGet")
        data = json.loads(result)
        result = data['data']['status']
        print(row['Delivery'] + ' - Status updaté')
        
    return result

df_tracking['Status'] = df_tracking.apply(f, axis=1)
df_tracking.to_csv('tracking.csv', index=False)



#7 Update Tracking item(更新一个单号)
#urlStr = "/china-ems/EA152565241CN"
#requestData = "{\"title\": \"testtitle\",\"customer_name\":\"python test\",\"customer_email\":\"942632688@qq.com\",\"order_id\":\"#1234567\",\"logistics_channel\":\"chase chen python\",\"customer_phone\":\"+86 13873399982\",\"destination_code\":\"US\",\"status\":\"7\"}"
#result = tracker.trackingmore(requestData, urlStr, "codeNumberPut")

