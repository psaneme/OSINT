import json, mailbox,email,traceback,re

FILENAME = "PATH_TO_MBOX_FILE.mailbox"
FILERES  = "RESFILENAME.csv"


fRes = open(FILERES,"w")
mb = mailbox.mbox(FILENAME) 
relations = {}

def RealAddressFrom(email):
    if isinstance(email,str):
        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email)
        if len(match)>0:
            return match[0]
        else:
            return email

    else:
        return email

def RealAddressTo(email):
    if isinstance(email,str):

        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', email)
        return match
    else:
        return [email]


for mail in mb:
    try:
        fr = mail.get("From")
        if isinstance(fr,email.header.Header):
            fr = str(fr)
        fr = RealAddressFrom(fr)
        to = mail.get("To")
        to = RealAddressTo(to)

        getF = relations.get(fr)
        if getF:
            for t in to:
                if isinstance(t,email.header.Header):
                    t = str(t)
                getT = getF.get(t)
                if getT:
                    getF[t] += 1
                else:
                    getF[t] = 1
        else:
            dic = {}
            for t in to:
                if isinstance(t,email.header.Header):
                    t = str(t)
                dic[t]=1
            relations[fr]=dic
    except:
        traceback.print_exc()
        pass

for frk in relations.keys():
    tos = relations.get(frk)
    for to in tos.keys():
        value = tos.get(to)
        fRes.write(f"{frk};{to};{value}\n")
        fRes.flush()

fRes.close()