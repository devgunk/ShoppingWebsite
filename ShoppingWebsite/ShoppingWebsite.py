from django.shortcuts import *
from django.http import *
import pymysql
from django.views.decorators.csrf import *
from connectionfile import *
from django.core.files.storage import *
from datetime import *
import http.client
import smtplib

def showreviewsaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    s = "select * from postedreview where pid = '" + request.GET['pid'] + "'"
    cr.execute(s)
    result = cr.fetchall()
    x = []
    for p in result:
        d = {}
        d['email'] = p[1]
        d['content'] = p[2]
        x.append(d)
    return JsonResponse(x,safe=False)

#----------------------------------------------------------TEMPLATE-----------------------------------------------------

def index(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    return render(request,'index.html',{"mydata": x})

def showaction(request):
    conn = connection.connection('')
    s = "select * from producttable order by pid DESC"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = (p[1]).upper()
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    return JsonResponse(x, safe=False)

def contact(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s1 = "select * from categorytable"
    cr.execute(s1)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
        return render(request, "contact.html", {"mydata": x})

@csrf_exempt
def contentaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    s = "INSERT INTO `content` (`id`, `email`, `name`, `phonono`, `content`) VALUES (NULL, '"+ request.POST['email'] +"', '"+ request.POST['name'] +"', '"+ request.POST['phoneno'] +"', '"+ request.POST['content'] +"')"
    cr.execute(s)
    conn.commit()
    d = {}
    d['message'] = "Message Sent"
    return JsonResponse(d, safe=False)

def about(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    return render(request, 'about.html', {"mydata": x})

def service(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    return render(request, 'service.html', {"mydata": x})

def shop(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    return render(request, 'shop.html', {"mydata": x})

def product(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s = "select * from categorytable"
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    d = {}
    d['cat'] = request.GET['category']
    x.append(d)
    return render(request, 'product.html', {"mydata": x})

def single(request):
    conn = connection.connection('')
    cr = conn.cursor()
    x = []
    s1 = "select * from categorytable"
    cr.execute(s1)
    result = cr.fetchall()
    for p in result:
        d = {}
        d["category"] = p[0]
        x.append(d)
    query = "select * from producttable where pid = '" + request.GET['pid'] + "'"
    cr.execute(query)
    r = cr.fetchone()
    d = {}
    d['pid'] = r[0]
    d['pname'] = r[1]
    d['description'] = r[2]
    d['price'] = r[3]
    d['mrp'] = r[4]
    d['photo'] = r[5]
    x.append(d)
    if request.session.has_key('USEREMAIL'):
        s = "select * from usersignup where email = '"+ request.session['USEREMAIL'] +"'"
        cr.execute(s)
        p = cr.fetchone()
        d = {}
        d['email'] = p[0]
        x.append(d)
        return render(request, "single.html", {"mydata": x})
    else:
        return render(request, 'single.html', {"mydata": x})

@csrf_exempt
def reviews(request):
    conn = connection.connection('')
    cr = conn.cursor()
    s = "select photo from producttable where pid = '" + request.POST['pid'] + "'"
    cr.execute(s)
    result = cr.fetchone()
    s1 = "INSERT INTO `reviews` (`pid`, `email`, `content` , `photo`) VALUES (NULL,'" + request.POST['pid'] + "', '" + request.POST['email'] + "', '" + request.POST['content'] + "', '" + result[0] + "')"
    cr.execute(s1)
    conn.commit()
    d = {}
    d['message'] = 'Message Sent'
    return JsonResponse(d, safe=False)

@csrf_exempt
def addtocartquickviewaction(request):
    CARTLIST = []
    if request.session.has_key('MYCART'):
        CARTLIST = request.session['MYCART']
    conn = connection.connection('')
    s = "select * from producttable where pid = '" + request.POST['pid'] + "'"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    flag = 0
    for product in CARTLIST:
        if product['pid'] == int(request.POST['pid']):
            flag = 1
            break
    if flag == 0:
        for p in result:
            d = {}
            d['pid'] = p[0]
            d['pname'] = p[1]
            d['description'] = p[2]
            d['price'] = p[3]
            d['mrp'] = p[4]
            d['photo'] = p[5]
            d['categoryname'] = p[6]
            d['qty'] = request.POST['qty']
            d['amount'] = float(p[3]) * float(request.POST['qty'])
            CARTLIST.append(d)
    else:
        for product in CARTLIST:
            if product['pid'] == int(request.POST['pid']):
                product['qty'] = int(product['qty']) + int(request.POST['qty'])
                product['amount'] = float(product['price']) * int(product['qty'])
    request.session['MYCART'] = CARTLIST
    return JsonResponse(request.session['MYCART'], safe=False)

#------------------------------------------------------END-TEMPLATE-----------------------------------------------------
#----------------------------------------------------------------------ADMIN---------------------------------------------------------------------

def AdminHomePage(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        query1 = "select * from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(query1)
        result = cr.fetchone()
        d = {}
        d["email"] = result[0]
        d["password"] = result[1]
        d["fullname"] = result[2]
        d["admintype"] = result[3]
        return render(request, "AdminHomePage.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def InsertRecord(request):
    if request.session.has_key("ADMINEMAIL"):
        d={}
        d['sadmintype'] = request.GET["sadmintype"]
        return render(request, "InsertRecord.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def OnInsertClick(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        query1 = "select * from adminrecord"
        cr.execute(query1)
        result = cr.fetchall()
        flag = 0
        for p in result:
            if p[0] == request.GET["email"]:
                flag = 1
                break
        if flag == 0:
            email = request.GET['email']
            email = email.lower()
            password = request.GET['password']
            fullname = request.GET['fullname']
            admintype = request.GET['admintype']
            query = "insert into adminrecord values('" + email + "','" + password + "','" + fullname + "','" + admintype + "')"
            cr.execute(query)
            conn.commit()
            conn.close()
            d = {}
            d['message'] = "Data inserted"
            return JsonResponse(d, safe=False)
        else:
            d = {}
            d['message'] = "Data already exist"
            return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

def ViewRecord(request):
    if request.session.has_key("ADMINEMAIL"):
        conct = connection.connection('')
        cr = conct.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        query = "select * from adminrecord"
        cr.execute(query)
        result = cr.fetchall()
        for p in result:
            d = {}
            d["email"] = p[0]
            d["password"] = p[1]
            d["fullname"] = p[2]
            d["admintype"] = p[3]
            d["editurl"] = "EditRecord?email="+p[0]
            d["deleteurl"] = "DeleteRecord?email="+p[0]
            x.append(d)
        return render(request, "ViewRecord.html", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

def viewcontacts(request):
    if request.session.has_key("ADMINEMAIL"):
        conct = connection.connection('')
        cr = conct.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        query = "select * from content"
        cr.execute(query)
        result = cr.fetchall()
        for p in result:
            d = {}
            d['id'] = p[0]
            d["email"] = p[1]
            d["name"] = p[2]
            d["phoneno"] = p[3]
            d["content"] = p[4]
            d["deleteurl"] = "DeleteContent?id="+str(p[0])
            x.append(d)
        return render(request, "viewcontacts.html", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

def viewreviews(request):
    if request.session.has_key("ADMINEMAIL"):
        conct = connection.connection('')
        cr = conct.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        query = "select * from reviews"
        cr.execute(query)
        result = cr.fetchall()
        i = 0
        for p in result:
            d = {}
            d['sno'] = i + 1
            i = i + 1
            d['pid'] = p[0]
            d["email"] = p[1]
            d["content"] = p[2]
            d['photo'] = p[3]
            d["posturl"] = "PostReview?id="+str(p[0])
            d["deleteurl"] = "DeleteReviewsx?id="+str(p[0])+"&content="+p[2]
            x.append(d)
        return render(request, "viewreviews.html", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

def DeleteContent(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "DELETE FROM content WHERE `id` = '" + request.GET["id"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("viewcontacts")
    else:
        return HttpResponseRedirect("loginadmin")

def PostReview(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s1 = "select * from reviews where pid = '" + request.GET['id'] + "'"
        cr.execute(s1)
        p = cr.fetchone()
        s = "INSERT INTO `postedreview` (`pid`, `email`, `content`, `photo`) VALUES ('" + request.GET['id'] + "', '" + p[1] + "', '" + p[2] + "', '" + p[3] + "')"
        cr.execute(s)
        conn.commit()
        query1 = "DELETE FROM reviews WHERE `content` = '" + request.GET["content"] + "' and `pid` = '" + request.GET["id"] + "'"
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("viewreviews")
    else:
        return HttpResponseRedirect("loginadmin")

def postedreviews(request):
    if request.session.has_key("ADMINEMAIL"):
        conct = connection.connection('')
        cr = conct.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        query = "select * from postedreview"
        cr.execute(query)
        result = cr.fetchall()
        i = 0
        for p in result:
            d = {}
            d['id'] = i + 1
            i = i + 1
            d["email"] = p[1]
            d["content"] = p[2]
            d["pid"] = p[0]
            d["photo"] = p[3]
            d["deleteurl"] = "Deletepostedreview?id="+str(p[0])+"&content="+p[2]
            x.append(d)
        return render(request, "postedreviews.html", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

def Deletepostedreview(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "DELETE FROM postedreview WHERE `content` = '" + request.GET["content"] + "' and `pid` = '" + request.GET["id"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("postedreviews")
    else:
        return HttpResponseRedirect("loginadmin")

def DeleteReviews(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "DELETE FROM reviews WHERE `id` = '" + request.GET["id"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("viewreviews")
    else:
        return HttpResponseRedirect("loginadmin")

def EditRecord(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d={}
        d['sadmintype'] = sadmintype[0]
        email = request.GET['email']
        query = "select * from adminrecord where email = '" + email + "'"
        cr.execute(query)
        result = cr.fetchone()
        d["email"] = result[0]
        d["password"] = result[1]
        d["fullname"] = result[2]
        d["admintype"] = result[3]
        return render(request, "EditRecord.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

@csrf_exempt
def OnClickEditRecord(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        query1 = "update `adminrecord` set `email` = '" + request.POST["Textbox1"] + "', `password` = '" + request.POST["Textbox2"] + "', `fullname` = '" + request.POST["Textbox3"] + "', `admintype` = '" + request.POST["Textbox4"] + "' where `email` = '" + request.POST["Textbox1"] + "'"
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("ViewRecord")
    else:
        return HttpResponseRedirect("loginadmin")

def DeleteRecord(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "DELETE FROM `adminrecord` WHERE `email` = '" + request.GET["email"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("ViewRecord")
    else:
        return HttpResponseRedirect("loginadmin")

def loginadmin(request):
    return render(request,"loginadmin.html")

@csrf_exempt
def adminloginaction(request):
    conn = connection.connection('')
    email = request.POST['email']
    password = request.POST['password']
    query = "select * from adminrecord"
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    d = {}
    for p in result:
        if p[0] == email and p[1] == password:
            d['message'] = "Login Success"
            request.session['ADMINEMAIL'] = email
            #python manage.py migrate
            return JsonResponse(d, safe=False)
    d['message'] = "Invalid Login"
    return JsonResponse(d, safe=False)

def adminlogout(request):
    if request.session.has_key("ADMINEMAIL"):
        request.session.pop("ADMINEMAIL")
        return HttpResponseRedirect("loginadmin")
    else:
        return HttpResponseRedirect("loginadmin")

def editadminprofile(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d = {}
        d['sadmintype'] = sadmintype[0]
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select * from `adminrecord` where `email` = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        result = cr.fetchone()
        d['email'] = result[0]
        d['password'] = result[1]
        d['fullname'] = result[2]
        d['admintype'] = result[3]
        return render(request,"editadminprofile.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def changepassword(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d = {}
        d['sadmintype'] = sadmintype[0]
        query = "select * from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(query)
        result = cr.fetchone()
        d["email"] = result[0]
        d["password"] = result[1]
        d["fullname"] = result[2]
        d["admintype"] = result[3]
        return render(request, "changepassword.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

@csrf_exempt
def OnClickChangePassword(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select `password` from `adminrecord` where `email` = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        password = cr.fetchone()
        if password[0] != request.POST['password']:
            d={}
            d['message'] = "Wrong Password"
            return JsonResponse(d, safe=False)
        else:
            query1 = "update `adminrecord` set  `password` = '" + request.POST["newpassword"] + "' where `email` = '" + request.session['ADMINEMAIL'] + "'"
            cr.execute(query1)
            conn.commit()
            d = {}
            d['message'] = "Success"
            return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

@csrf_exempt
def OnClickChangeName(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "update `adminrecord` set `fullname` = '" + request.POST["fullname"] + "' where `email` = '" + request.session['ADMINEMAIL'] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("AdminHomePage")
    else:
        return HttpResponseRedirect("loginadmin")

def pendingorderpage(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d = {}
        d['admintype'] = sadmintype[0]
        return render(request,"pendingorderpage.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def pendingordersaction(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select * from ordertable where status = 'Pending' order by id DESC"
        cr.execute(s)
        result = cr.fetchall()
        x=[]
        for p in result:
            d={}
            d['id'] = p[0]
            d['email'] = p[1]
            d['fullname'] = p[2]
            d['mobileno'] = p[3]
            d['address'] = p[4]
            d['city'] = p[5]
            d['netamount'] = p[6]
            d['dateoforder'] = p[7]
            d['paymentmode'] = p[9]
            x.append(d)
        return JsonResponse(x, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

def approve_reject_action(request):
    if request.session.has_key("ADMINEMAIL"):
        orderid = request.GET['orderid']
        status = request.GET['status']
        mobileno = request.GET['mobileno']
        conn = connection.connection('')
        cr = conn.cursor()
        s = "update ordertable set status = '" + status + "' where id = '" + str(orderid) + "'"
        cr.execute(s)
        conn.commit()
        s2 = "select customeremail from ordertable where id = '" + orderid + "'"
        cr.execute(s2)
        email = cr.fetchone()
        #--------------------------------------------MESSAGE------------------------------------------------------------
        msg = "Your Order with Order ID " + str(orderid) + " has been " + str(status) + " .Your order will be delivered after order approval. Thank You"
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',"/VMMCloudMessaging/AWS_SMS_Sender?username=ExamSystem&password=S4J5LT3C&message=" + msg + "&phone_numbers=" + mobileno)
        response = conn1.getresponse()
        print(response.read())
        #-----------------------------------------END-MESSAGE-----------------------------------------------------------
        #----------------------------------------------EMAIL------------------------------------------------------------
        sender = 'karandevgunsharma@gmail.com'
        receiver = email
        password = 'iwannabear'
        # https://serverfault.com/questions/635139/how-to-fix-send-mail-authorization-failed-534-5-7-14
        # two steps are reuqired------------
        # 1. allow less secure apps - 'ON' this service
        # 2. enable captcha - using the above link
        # all these changes are required in the account, from where you want to send the mail.
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(sender, password)
            body = "\nYour Order with Order ID " + str(orderid) + " has been " + str(status) + " . Your order will be delivered after order approval. Thank You\n\n"
            subject = "Subject:Online Shopping "
            msg = subject + body
            smtpserver.sendmail(sender, receiver, msg)
            print('Sent')
            smtpserver.close()
        except smtplib.SMTPException:
            print("Not Sent")
        #--------------------------------------------END-EMAIL----------------------------------------------------------
        d={}
        d['message'] = "Order Updated"
        return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

#-----------------------------------------------------------ADMIN-END----------------------------------------------------------------------
#-----------------------------------------------------------CATEGORY-----------------------------------------------------------------------

def InsertCT(request):
    if request.session.has_key("ADMINEMAIL"):
        d = {}
        d['sadmintype'] = request.GET["sadmintype"]
        return render(request, "InsertCT.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def OnClickInsertCT(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        category = request.GET["category"]
        description = request.GET["description"]
        request.GET["description"]
        cr = conn.cursor()
        query1 = " select * from categorytable"
        cr.execute(query1)
        result = cr.fetchall()
        x = []
        flag = 0
        for p in result:
            if p[0] == category:
                flag = 1
        if flag == 0:
            query2 = "insert into categorytable values('" + category + "','" + description + "')"
            cr.execute(query2)
            conn.commit()
            conn.close()
            d = {}
            d['message'] = "Data Inserted"
            return JsonResponse(d, safe=False)
        else:
            d = {}
            d['message'] = "Data Already Exist"
            return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

def ViewCT(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        query = "select * from categorytable"
        cr.execute(query)
        result = cr.fetchall()
        for p in result:
            d = {}
            d["categoryname"] = p[0]
            d["description"] = p[1]

            d['editurl'] = "EditCT?c="+p[0]
            d['deleteurl'] = "DeleteCT?c="+p[0]
            x.append(d)
        return render(request, "ViewCT.html", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

def EditCT(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d={}
        d['sadmintype'] = sadmintype[0]
        query = "select * from categorytable where categoryname='"+request.GET['c']+"'"
        cr.execute(query)
        result = cr.fetchone()
        d["categoryname"] = result[0]
        d["description"] = result[1]
        return render(request, "EditCT.html", d)
    else:
        return HttpResponseRedirect("loginadmin")

def OnClickEditCT(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "update `categorytable` set `CategoryName` = '" + request.GET["Textbox1"] + "', `Description` = '" + request.GET["Textbox2"] + "' where `CategoryName` = '" + request.GET["Textbox1"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("ViewCT")
    else:
        return HttpResponseRedirect("loginadmin")

def DeleteCT(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        query1 = "DELETE FROM `categorytable` WHERE `CategoryName` = '" + request.GET["c"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        return HttpResponseRedirect("ViewCT")
    else:
        return HttpResponseRedirect("loginadmin")

#----------------------------------------------------END-CATEGORY----------------------------------------------------------------
#----------------------------------------------------------PRODUCT---------------------------------------------------------------

def addproductpage(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        s = "select * from categorytable"
        cr.execute(s)
        result = cr.fetchall()
        for p in result :
            d={}
            d["categoryname"] = p[0]
            x.append(d)
        return render(request,"addproductpage.html", {'mydata' : x })

@csrf_exempt
def addproductaction(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        categoryname = request.POST["categoryname"]
        pname = request.POST["pname"]
        price = request.POST["price"]
        mrp = request.POST["mrp"]
        description = request.POST["description"]
        photo = request.FILES["photo"]
        fs = FileSystemStorage()
        filename = fs.save(photo.name,photo)
        location = fs.url(filename)
        s = "insert into producttable values (null,'" + pname + "','" + description + "','" + price + "','" + mrp + "','" + filename + "','" + categoryname + "')"
        result = cr.execute(s)
        conn.commit()
        conn.close()
        d = {}
        d['message'] = "Data Saved"
        return JsonResponse( d, safe = False)
    else:
        return HttpResponseRedirect("loginadmin")

def viewproductpage(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d = {}
        d['sadmintype'] = sadmintype[0]
        return render(request, 'viewproductpage.html', d)
    else:
        return HttpResponseRedirect("loginadmin")

def viewproductaction(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s1 = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s1)
        x = []
        sadmintype = cr.fetchone()
        da = {}
        da['sadmintype'] = sadmintype[0]
        x.append(da)
        s = "select * from producttable"
        cr.execute(s)
        result = cr.fetchall()
        conn.close()
        for p in result:
            d = {}
            d['pid'] = p[0]
            d['pname'] = p[1]
            d['description'] = p[2]
            d['price'] = p[3]
            d['mrp'] = p[4]
            d['photo'] = p[5]
            d['categoryname'] = p[6]
            x.append(d)
        return JsonResponse(x, safe=False)
    else:
        return HttpResponseRedirect("loginadmin")

def deleteproductaction(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        pid = request.GET['pid']
        cr = conn.cursor()
        s = "delete from producttable where pid='" + str(pid) + "'"
        cr.execute(s)
        conn.commit()
        conn.close()
        return HttpResponseRedirect('viewproductpage')
    else:
        return HttpResponseRedirect("loginadmin")

def editproductpage(request): 
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        pid = request.GET['pid']
        s = "select admintype from adminrecord where email = '" + request.session['ADMINEMAIL'] + "'"
        cr.execute(s)
        sadmintype = cr.fetchone()
        d = {}
        d['sadmintype'] = sadmintype[0]
        print(sadmintype[0])
        query = "select * from producttable where pid = '" + str(pid) + "'"
        cr.execute(query)
        result = cr.fetchone()
        d['pid'] = result[0]
        d['pname'] = result[1]
        d['description'] = result[2]
        d['price'] = result[3]
        d['mrp'] = result[4]
        d['photo'] = result[5]
        d['categoryname'] = result[6]
        x = []
        x.append(d)
        s = "select * from categorytable"
        cr.execute(s)
        result = cr.fetchall()
        for p in result:
            d2 = {}
            d2["category"] = p[0]
            x.append(d2)
        return render(request, "editproductpage.html", { 'mydata' : x})
    else:
        return HttpResponseRedirect("loginadmin")

def editproductaction(request):
    if request.session.has_key("ADMINEMAIL"):
        conn = connection.connection('')
        if request.GET["photo"]:
            photo = request.GET["photo"]
        else:
            photo = request.GET["cphoto"]
        query1 = "update `producttable` set `pname` = '" + request.GET["pname"] + "', `description` = '" + request.GET["description"] + "', `price` = '" + request.GET["price"] + "', `mrp` = '" + request.GET["mrp"] + "', `photo` = '" + photo + "', `categoryname` = '" + request.GET["categoryname"] + "' where `pid` = '" + request.GET["pid"] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        s = "select * from producttable"
        cr = conn.cursor()
        cr.execute(s)
        result = cr.fetchall()
        conn.close()
        x = []
        for p in result:
            d = {}
            d['pid'] = p[0]
            d['pname'] = p[1]
            d['description'] = p[2]
            d['price'] = p[3]
            d['mrp'] = p[4]
            d['photo'] = p[5]
            d['categoryname'] = p[6]
            x.append(d)
        return HttpResponseRedirect("viewproductpage", {"mydata": x})
    else:
        return HttpResponseRedirect("loginadmin")

#--------------------------------------------------------END-PRODUCTS------------------------------------------------------------------
#------------------------------------------------------------USER----------------------------------------------------------------------

def usersignupaction(request):
    conn = connection.connection('')
    cr = conn.cursor()
    query1 = "select * from usersignup"
    cr.execute(query1)
    email = request.GET['uemail']
    email = email.lower()
    result = cr.fetchall()
    flag = 0
    d = {}
    for p in result:
        if p[0] == email:
            flag = 1
            break
    if flag == 0:
        fullname = request.GET['fullname']
        mobileno = request.GET['mobileno']
        address = request.GET['address']
        city = request.GET['city']
        password = request.GET['upassword']
        s = "insert into usersignup values ('" + email + "','" + fullname + "','" + mobileno + "','" + address + "','" + city + "','" + password + "')"
        cr.execute(s)
        conn.commit()
        d['message'] = "Data saved"
        request.session['USEREMAIL'] = email
    else:
        d['message'] = "Data Already Exist"
    return JsonResponse(d, safe=False)

def userlogin(request):
    return render(request,"userlogin.html")

@csrf_exempt
def userloginaction(request):
    email = request.POST['email']
    email = email.lower()
    password = request.POST['password']
    conn = connection.connection('')
    s = "select * from usersignup"
    cr = conn.cursor()
    flag =False
    cr.execute(s)
    result = cr.fetchall()
    for p in result:
        if p[0] == email and p[5] == password:
            request.session['USEREMAIL'] = email
            flag = True
            break
    d = {}
    if flag == False:
        d['message'] = "Invalid Login"
    else:
        d['message'] = "Login Success"
    return JsonResponse(d, safe = False)

def userlogout(request):
    if request.session.has_key("USEREMAIL"):
        request.session.pop("USEREMAIL")
    return HttpResponseRedirect("index")

def edituserprofile(request):
    if request.session.has_key("USEREMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select * from `usersignup` where `email` = '" + request.session['USEREMAIL'] + "'"
        cr.execute(s)
        result = cr.fetchone()
        d = {}
        d['email'] = result[0]
        d['fullname'] = result[1]
        d['phoneno'] = result[2]
        d['address'] = result[3]
        d['city'] = result[4]
        d['password'] = result[5]
        return render(request, 'edituserprofile.html', d)
    else:
        return HttpResponseRedirect("userlogin")

def showallproductaction(request):
    conn = connection.connection('')
    s = "select * from producttable"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    return JsonResponse(x, safe=False)

@csrf_exempt
def showcat(request):
    conn = connection.connection('')
    s = "select * from producttable where categoryname = '" + request.POST['cat'] + "'"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    x = []
    for p in result:
        d = {}
        d['pid'] = p[0]
        d['pname'] = p[1]
        d['description'] = p[2]
        d['price'] = p[3]
        d['mrp'] = p[4]
        d['photo'] = p[5]
        d['categoryname'] = p[6]
        x.append(d)
    return JsonResponse(x, safe=False)

def changeuserpassword(request):
    if request.session.has_key("USEREMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        query = "select * from `usersignup` where `email` = '" + request.session['USEREMAIL'] + "'"
        cr.execute(query)
        result = cr.fetchone()
        return render(request, "changeuserpassword.html")
    else:
        return HttpResponseRedirect("userlogin")

@csrf_exempt
def OnClickChangeUserPassword(request):
    if request.session.has_key("USEREMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select `password` from `usersignup` where `email` = '" + request.session['USEREMAIL'] + "'"
        cr.execute(s)
        password = cr.fetchone()
        if password[0] != request.POST['password']:
            d = {}
            d['message'] = "Wrong Password"
            return JsonResponse(d, safe=False)
        else:
            query1 = "update `usersignup` set  `password` = '" + request.POST["newpassword"] + "' where `email` = '" + request.session['USEREMAIL'] + "'"
            cr.execute(query1)
            conn.commit()
            d = {}
            d['message'] = "Success"
            return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("userlogin")

@csrf_exempt
def OnClickChangeUserName(request):
    if request.session.has_key("USEREMAIL"):
        conn = connection.connection('')
        query1 = "update `usersignup` set `fullname` = '" + request.POST["fullname"].strip() + "', `mobileno` = '" + request.POST["phoneno"] + "', `address` = '" + request.POST["address"] + "', `city` = '" + request.POST["city"] + "' where `email` = '" + request.session['USEREMAIL'] + "'"
        cr = conn.cursor()
        cr.execute(query1)
        conn.commit()
        d = {}
        d['message'] = 'Data Updated'
        return JsonResponse(d, safe=False)
    else:
        return HttpResponseRedirect("userlogin")

def myorders(request):
    if request.session.has_key("USEREMAIL"):
        return render(request, "myorders.html")
    else:
        return HttpResponseRedirect("userlogin")

def myordersaction(request):
    if request.session.has_key("USEREMAIL"):
        email = request.GET['email']
        conn = connection.connection('')
        cr = conn.cursor()
        s = "select * from ordertable where customeremail = '" + email + "' order by id DESC"
        cr.execute(s)
        result = cr.fetchall()
        flag = 0
        for p in result:
            if p[1] == email:
                flag = 1
                break
        if flag == 0:
            d = {}
            d['message'] = 'No Product Ordered'
            return JsonResponse(d, safe=False)
        x=[]
        for p in result:
            d={}
            d['id'] = p[0]
            d['email'] = p[1]
            d['fullname'] = p[2]
            d['mobileno'] = p[3]
            d['address'] = p[4]
            d['city'] = p[5]
            d['netamount'] = p[6]
            d['dateoforder'] = p[7]
            d['status'] = p[8]
            d['paymentmode'] = p[9]
            x.append(d)
        return JsonResponse(x, safe=False)
    else:
        return HttpResponseRedirect("userlogin")

#----------------------------------------------------------END-USER-------------------------------------------------------------------
#------------------------------------------------------------CART---------------------------------------------------------------------

def addtocartaction(request):
    CARTLIST = []
    if request.session.has_key('MYCART'):
        CARTLIST = request.session['MYCART']
    pid = int(request.GET['pid'])
    qty = 1
    price = int(request.GET['price'])
    conn = connection.connection('')
    s = "select * from producttable where pid = '" + str(pid) + "'"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    conn.close()
    flag = 0
    for product in CARTLIST:
        if product['pid'] == pid:
            flag = 1
            break
    if flag == 0:
        for p in result:
            d = {}
            d['pid'] = p[0]
            d['pname'] = p[1]
            d['description'] = p[2]
            d['price'] = p[3]
            d['mrp'] = p[4]
            d['photo'] = p[5]
            d['categoryname'] = p[6]
            d['qty'] = qty
            d['amount'] = float(p[3]) *float(qty)
            CARTLIST.append(d)
    else:
        for product in CARTLIST:
            if product['pid'] == pid:
                product['qty'] = product['qty'] + 1
                product['amount'] = price * product['qty']
    request.session['MYCART'] = CARTLIST
    return JsonResponse(request.session['MYCART'], safe=False)

def mycart(request):
    return render(request, "mycart.html")

def mycartaction(request):
    if request.session.has_key('MYCART'):
        return JsonResponse( request.session['MYCART'], safe = False)
    else:
        d = {}
        d['message'] = 'No Product'
        return JsonResponse(d, safe=False)

#---------------------------------------------------------END-CART-------------------------------------------------------------
#---------------------------------------------------------PAYMENT--------------------------------------------------------------

def proceedtopay(request):
    if request.session.has_key('USEREMAIL'):
        k = "/billinginfo"
    else:
        k = "/userlogin"
    return HttpResponseRedirect(k)

def billinginfo(request):
    if request.session.has_key("USEREMAIL"):
        conn = connection.connection('')
        cr = conn.cursor()
        flag = False
        s = "select * from usersignup where email = '" + request.session['USEREMAIL'] + "'"
        cr.execute(s)
        result = cr.fetchone()
        d={}
        d["fullname"] = result[1]
        d['mobileno'] = result[2]
        d['address'] = result[3]
        d['city'] = result[4]
        netamount = 0
        for i  in range(0,len(request.session['MYCART'])):
            ar = request.session['MYCART']
            netamount = netamount + ar[i]['amount']
        d['netamount'] = netamount
        return render(request,'billinginfo.html',d)
    else:
        return HttpResponseRedirect("userlogin")

@csrf_exempt
def checkoutaction(request):
    if request.session.has_key("USEREMAIL"):
        email  = request.POST['email']
        fullname = request.POST['fullname']
        netamount = request.POST['netamount']
        mobileno = request.POST['mobileno']
        address = request.POST['address']
        city = request.POST['city']
        paymentmode = request.POST['paymentmode']
        conn = connection.connection('')
        cr = conn.cursor()
        dt = datetime.now().date()
        s = "insert into ordertable values (null,'"+email+"','"+fullname+"','"+mobileno+"','"+address+"','"+city+"','"+str(netamount)+"','"+str(dt)+"','Pending','"+paymentmode+"')"
        cr.execute(s)
        conn.commit()
        orderid = cr.lastrowid
        for i in range(0, len(request.session['MYCART'])):
            ar = request.session['MYCART']
            s1 = "insert into orderdetail values (null,'"+str(orderid)+"','"+str(ar[i]['pid'])+"','"+ar[i]['pname']+"','"+str(ar[i]['price'])+"','"+str(ar[i]['qty'])+"','"+str(ar[i]['amount'])+"')"
            cr.execute(s1)
            conn.commit()
        #---------------------------------------------MESSAGE-----------------------------------------------------------
        msg = "Your Order with Order ID " + str(orderid) + " has been placed for Rs." + str(netamount) + " .Your order will be delivered after order approval. Thank You"
        msg = msg.replace(" ", "%20")
        conn1 = http.client.HTTPConnection("server1.vmm.education")
        conn1.request('GET',"/VMMCloudMessaging/AWS_SMS_Sender?username=ExamSystem&password=S4J5LT3C&message=" + msg + "&phone_numbers=" + mobileno)
        response = conn1.getresponse()
        print(response.read())
        #-------------------------------------------END-MESSAGE---------------------------------------------------------
        #----------------------------------------------EMAIL------------------------------------------------------------
        sender = 'karandevgunsharma@gmail.com'
        receiver = request.session['USEREMAIL']
        password = 'iwannabear'
        #https://serverfault.com/questions/635139/how-to-fix-send-mail-authorization-failed-534-5-7-14
        #two steps are reuqired------------
        #1. allow less secure apps - 'ON' this service
        # 2. enable captcha - using the above link
        # all these changes are required in the account, from where you want to send the mail.
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(sender, password)
            subject = "Subject:Online Shopping "
            body = "\nYour Order with Order ID " + str(orderid) + " has been placed for Rs." + str(netamount) + " . Your order will be delivered after order approval. Thank You\n\n"
            msg = subject + body
            smtpserver.sendmail(sender, receiver, msg)
            print('Sent')
            smtpserver.close()
        except smtplib.SMTPException:
            print("Not Sent")
        #-------------------------------------------END-EMAIL-----------------------------------------------------------
        del request.session['MYCART']
        d={}
        d['message'] = "Data Saved"
        return JsonResponse(d,safe=False)
    else:
        return HttpResponseRedirect("userlogin")

#--------------------------------------------------END-THANKS-----------------------------------------------------------