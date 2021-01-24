import asyncio
import json
import datetime
def sortByLength(inputStr):
    return len(inputStr)
async def handle_echo(reader, writer):
    data = await reader.read(1024)
    data = data.decode('utf-8')
    print(data)
    file = json.load(open("data.json"))
    users=file['users']
    if data in users:
        writer.write('ok\n'.encode('utf-8'))
    else:
        for i in users:
            if data ==i+" connect":
                txt =""
                for a in users:
                    if a !=i:
                        txt = txt + a + " "

                writer.write(txt.encode('utf-8'))
        if " make connected update " in data:
            data = data.replace(" make connected update "," ")
            index = data.index(" ")
            count =[]
            count.append(data[:index])
            count.append(data[index+1:])
            count.sort(key=sortByLength)
            msg=""
            ok =False
            for i in file["history"]:
                if i["users"] == count:
                    for a in i["history"]:
                        try:
                            msg = msg+a['author']+"\\"+a["time"]+" "+a["text"]+"\n"
                        except:
                            msg = msg + a['author'] + "\\" + a["time"] + " " + a["text"] + "\n"
                    ok =True
            if not ok:
                time = str(datetime.datetime.utcnow()+datetime.timedelta(hours=3))
                time=time[:19]
                history = file["history"]
                dictation={"users": [count[0],count[1]], "history":[{"author":"admin","time":time,"text":"Начало переписки"}]}
                history.append(dictation)
                file["history"]=history
                with open("data.json","w") as f:
                    f.write(json.dumps(file,indent=4))
                txt ="admin"+'/'+time+" Начало переписки"
                txt = txt.replace('/',"\\")
                writer.write(txt.encode("utf-8"))
            writer.write(msg.encode("utf-8"))
        elif data[:5]=="send ":
            data=data[5:]
            index=data.index("\\")
            author=data[:index]
            data=data[index+1:]
            index=data.index("\\")
            text=data[:index]
            data = data[index+1:]
            time = data[:19]
            user=data[20:]
            count=[]
            count.append(user)
            count.append(author)
            count.sort(key=sortByLength)
            print(text)
            for i in file["history"]:
                if i["users"]==count:
                    key= file["history"].index(i)
                    file["history"][key]["history"].append({"author":author,"time":time,"text":text})
            with open("data.json","w") as f:
                f.write(json.dumps(file,indent=4))
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo,"192.168.1.149", 10001,loop=loop)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()