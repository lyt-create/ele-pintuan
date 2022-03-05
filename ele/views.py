import datetime
import json
import random

from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ele.models import Myuser, Pinsubject, Pinmodel, Pindata


def order(request):
    pin = Pinsubject.objects.filter(yunum__gt=0).order_by("-createtime")
    if pin:
        if len(pin) > 3:
            pindata = pin[:3]
        else:
            pindata = pin
        return render(request, "order.html", {'pindata': pindata})
    pindata = []
    pindict = {"name": "这里什么也没有，快去发起拼团吧！", "id": "#"}
    pindata.append(pindict)
    pindata.append(pindict)
    pindata.append(pindict)
    return render(request, "order.html", {'pindata': pindata})

@login_required
def cook(request):
    uid = request.user.id
    pindata = Pindata.objects.filter(uid=uid).exclude(state="已结束")
    pidlist = []
    for p in pindata:
        pidlist.append(p.pinid)
    subjectlist = []
    levellist = []
    datalist_all = []
    pricelist_all = []
    alldata = []
    alldict = []
    moneylist = []
    ptemp_all = []
    for a in pidlist:
        datadict = {}
        pa = Pinsubject.objects.get(pid=a)
        subjectlist.append(pa.name)
        if pa.userid == uid:
            levellist.append(1)
        else:
            levellist.append(0)
        pb = Pindata.objects.filter(pinid=a)
        datalist = []
        ptemp = []
        for b in pb:
            datadict = {}
            datadict["name"]=b.username
            datadict["progress"] = str(pa.yunum)+'/'+str(pa.num)
            datadict["state"] = b.state
            cost = 0
            for c in json.loads(b.content.replace("'", '"')):
                ptemp.append(c)
                cost += int(c.get("price")) * int(c.get("count"))
            datadict["cost"] = cost
            datalist.append(datadict)
        ptemp_all.append(ptemp)
        datalist_all.append(datalist)

    namelist_all = []
    for d in ptemp_all:
        namelist = []
        for m in d:
            if m.get("name") not in namelist:
                namelist.append(m.get("name"))
        namelist_all.append(namelist)
    pricedict = {}
    pricelist_all = []
    for e in range(len(namelist_all)):
        pricelist = []
        for n in namelist_all[e]:
            g = 0
            pricedict = {}
            for f in ptemp_all[e]:
                if n == f.get("name"):
                    g += int(f.get("count"))
                    pricedict["price"] = f.get("price")
            pricedict["num"] = g
            pricedict["name"] = n
            pricedict["count"] = int(pricedict["num"]) * int(pricedict["price"])
            pricelist.append(pricedict)
        pricelist_all.append(pricelist)

    for h in pricelist_all:
        money = 0
        for k in h:
            money += int(k.get("count"))
        moneylist.append(money)
    for j in range(len(subjectlist)):
        alldict = {"subject": subjectlist[j],
                   "pid": pidlist[j],
                   "level": levellist[j],
                   "data": datalist_all[j],
                   "money": moneylist[j],
                   "price": pricelist_all[j]}
        alldata.append(alldict)
    print(alldata)
    return render(request, "cook.html", {'alldata': alldata})

@login_required()
def me(request):
    return render(request, "me.html")


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        tel = request.POST.get('tel')
        user = Myuser.objects.filter(username=username)
        if user:
            tips = "提示：用户名已被占用，请更换用户名！"
            return render(request, 'register.html', {'tips': tips})
        if password != confirmpassword:
            tips = "提示：两次输入的密码不一致！"
            return render(request, 'register.html', {'tips': tips})
        Myuser.objects.create_user(username=username, password=password,tel=tel)
        return redirect('login.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session.set_expiry(10080 * 60)  # 60分钟后失效
            return redirect('order.html')
        else:
            tips = '提示：账号或密码错误！'
            return render(request, 'login.html', {'tips': tips})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login.html')


@login_required()
def orderdata(request):
    return render(request, "orderdata.html")

@login_required()
def mydata(request):
    if request.method == "GET":
        data = Myuser.objects.get(id=request.user.id)
        return render(request, "mydata.html", {'data': data})
    else:
        tel = request.POST.get("tel")
        user = Myuser.objects.get(id=request.user.id)
        user.tel = tel
        user.save()
        return redirect("me.html")

@login_required()
def myorder(request):
    uid = request.user.id
    pindata = Pindata.objects.filter(uid=uid)
    pidlist = []
    for p in pindata:
        pidlist.append(p.pinid)
    subjectlist = []
    levellist = []
    datalist_all = []
    pricelist_all = []
    alldata = []
    alldict = []
    moneylist = []
    ptemp_all = []
    for a in pidlist:
        datadict = {}
        pa = Pinsubject.objects.get(pid=a)
        subjectlist.append(pa.name)
        if pa.userid == uid:
            levellist.append(1)
        else:
            levellist.append(0)
        pb = Pindata.objects.filter(pinid=a)
        datalist = []
        ptemp = []
        for b in pb:
            datadict = {}
            datadict["name"] = b.username
            datadict["progress"] = str(pa.yunum) + '/' + str(pa.num)
            datadict["state"] = b.state
            datalist.append(datadict)
            for c in json.loads(b.content.replace("'", '"')):
                ptemp.append(c)
        ptemp_all.append(ptemp)
        datalist_all.append(datalist)

    namelist_all = []
    for d in ptemp_all:
        namelist = []
        for m in d:
            if m.get("name") not in namelist:
                namelist.append(m.get("name"))
        namelist_all.append(namelist)
    pricedict = {}
    pricelist_all = []
    for e in range(len(namelist_all)):
        pricelist = []
        for n in namelist_all[e]:
            g = 0
            pricedict = {}
            for f in ptemp_all[e]:
                if n == f.get("name"):
                    g += int(f.get("count"))
                    pricedict["price"] = f.get("price")
            pricedict["num"] = g
            pricedict["name"] = n
            pricedict["count"] = int(pricedict["num"]) * int(pricedict["price"])
            pricelist.append(pricedict)
        pricelist_all.append(pricelist)

    for h in pricelist_all:
        money = 0
        for k in h:
            money += int(k.get("count"))
        moneylist.append(money)
    for j in range(len(subjectlist)):
        alldict = {"subject": subjectlist[j],
                   "pid": pidlist[j],
                   "level": levellist[j],
                   "data": datalist_all[j],
                   "money": moneylist[j],
                   "price": pricelist_all[j]}
        alldata.append(alldict)
    return render(request, "myorder.html", {'alldata': alldata})


@login_required()
def cookset(request):
    return render(request, "cookset.html")

@login_required()
def start(request):
    if request.method == "GET":
        mdata = Pinmodel.objects.filter(userid=request.user.id)
        return render(request, "start.html", {'mdata': mdata})

    else:
        name = request.POST.get("name")
        num = request.POST.get("num")
        pm = request.POST.get("pm")
        remark = request.POST.get("remark")
        shu = ""
        for i in range(0, 4):
            shu += str(random.randint(0, 9))
        pid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")[:18] + shu
        psb = Pinsubject(
            pid=pid,
            name=name,
            userid=request.user.id,
            username=request.user.username,
            usertel=request.user.tel,
            num=int(num),
            yunum=int(num),
            pmodel=pm,
            state="拼团中",
            remark=remark,
            createtime=datetime.datetime.now()
        )
        psb.save()
        return render(request, "success.html", {'pid': pid, 'data': name})


@login_required()
def createmodel(request):
    if request.method == "GET":
        tip = "创建模板"
        return render(request, "createmodel.html", {'tip': tip})
    else:
        name = request.POST.get('name')
        w1 = request.POST.get("w1")
        p1 = request.POST.get("p1")
        w2 = request.POST.get("w2")
        p2 = request.POST.get("p2")
        w3 = request.POST.get("w3")
        p3 = request.POST.get("p3")
        w4 = request.POST.get("w4")
        p4 = request.POST.get("p4")
        w5 = request.POST.get("w5")
        p5 = request.POST.get("p5")
        w6 = request.POST.get("w6")
        p6 = request.POST.get("p6")
        w7 = request.POST.get("w7")
        p7 = request.POST.get("p7")
        w8 = request.POST.get("w8")
        p8 = request.POST.get("p8")
        w9 = request.POST.get("w9")
        p9 = request.POST.get("p9")
        w10 = request.POST.get("w10")
        p10 = request.POST.get("p10")
        w11 = request.POST.get("w11")
        p11 = request.POST.get("p11")
        w12 = request.POST.get("w12")
        p12 = request.POST.get("p12")
        w13 = request.POST.get("w13")
        p13 = request.POST.get("p13")
        w14 = request.POST.get("w14")
        p14 = request.POST.get("p14")
        w15 = request.POST.get("w15")
        p15 = request.POST.get("p15")
        w16 = request.POST.get("w16")
        p16 = request.POST.get("p16")
        conlist = []
        if w1:
            condict = {"name": w1, "price": p1}
            conlist.append(condict)
        if w2:
            condict = {"name": w2, "price": p2}
            conlist.append(condict)
        if w3:
            condict = {"name": w3, "price": p3}
            conlist.append(condict)
        if w4:
            condict = {"name": w4, "price": p4}
            conlist.append(condict)
        if w5:
            condict = {"name": w5, "price": p5}
            conlist.append(condict)
        if w6:
            condict = {"name": w6, "price": p6}
            conlist.append(condict)
        if w7:
            condict = {"name": w7, "price": p7}
            conlist.append(condict)
        if w8:
            condict = {"name": w8, "price": p8}
            conlist.append(condict)
        if w9:
            condict = {"name": w9, "price": p9}
            conlist.append(condict)
        if w10:
            condict = {"name": w10, "price": p10}
            conlist.append(condict)
        if w11:
            condict = {"name": w11, "price": p11}
            conlist.append(condict)
        if w12:
            condict = {"name": w12, "price": p12}
            conlist.append(condict)
        if w13:
            condict = {"name": w13, "price": p13}
            conlist.append(condict)
        if w14:
            condict = {"name": w14, "price": p14}
            conlist.append(condict)
        if w15:
            condict = {"name": w15, "price": p15}
            conlist.append(condict)
        if w16:
            condict = {"name": w16, "price": p16}
            conlist.append(condict)
        wp = Pinmodel(
            name=name,
            content=conlist,
            userid=request.user.id,
            username=request.user.username,
            createtime=datetime.datetime.now()
        )
        wp.save()
        return redirect("start.html")



@login_required()
def join(request):
    if request.method == "GET":
        pid = request.GET.get("pid")
        if pid:
            pdata = Pinsubject.objects.get(pid=pid)
            ddata = Pindata.objects.filter(pinid=pid)
            for d in ddata:
                if d.uid == request.user.id:
                    tips = "Error:您已经参与过本次拼团，无法再次参加！"
                    return render(request, "error.html", {'tips': tips})

            wdata = Pinmodel.objects.get(id=pdata.pmodel)
            productdata = wdata.content.replace("'", '"')
            product = json.loads(productdata)
            return render(request, "join.html", {'pdata': pdata, 'product': product})
        else:
            return render(request, "alllist.html")
    else:
        pinid = request.POST.get("pinid")
        tel = request.POST.get("tel")
        remark = request.POST.get("remark")
        w1 = request.POST.get("w1")
        p1 = request.POST.get("p1")
        c1 = request.POST.get("c1")
        if not c1:
            c1 = 0
        w2 = request.POST.get("w2")
        p2 = request.POST.get("p2")
        c2 = request.POST.get("c2")
        if not c2:
            c2 = 0
        w3 = request.POST.get("w3")
        p3 = request.POST.get("p3")
        c3 = request.POST.get("c3")
        if not c3:
            c3 = 0
        w4 = request.POST.get("w4")
        p4 = request.POST.get("p4")
        c4 = request.POST.get("c4")
        if not c4:
            c4 = 0
        w5 = request.POST.get("w5")
        p5 = request.POST.get("p5")
        c5 = request.POST.get("c5")
        if not c5:
            c5 = 0
        w6 = request.POST.get("w6")
        p6 = request.POST.get("p6")
        c6 = request.POST.get("c6")
        if not c6:
            c6 = 0
        w7 = request.POST.get("w7")
        p7 = request.POST.get("p7")
        c7 = request.POST.get("c7")
        if not c7:
            c7 = 0
        w8 = request.POST.get("w8")
        p8 = request.POST.get("p8")
        c8 = request.POST.get("c8")
        if not c8:
            c8 = 0
        w9 = request.POST.get("w9")
        p9 = request.POST.get("p9")
        c9 = request.POST.get("c9")
        if not c9:
            c9 = 0
        w10 = request.POST.get("w10")
        p10 = request.POST.get("p10")
        c10 = request.POST.get("c10")
        if not c10:
            c10 = 0
        w11 = request.POST.get("w11")
        p11 = request.POST.get("p11")
        c11 = request.POST.get("c11")
        if not c11:
            c11 = 0
        w12 = request.POST.get("w12")
        p12 = request.POST.get("p12")
        c12 = request.POST.get("c12")
        if not c12:
            c12 = 0
        w13 = request.POST.get("w13")
        p13 = request.POST.get("p13")
        c13 = request.POST.get("c13")
        if not c13:
            c13 = 0
        w14 = request.POST.get("w14")
        p14 = request.POST.get("p14")
        c14 = request.POST.get("c14")
        if not c14:
            c14 = 0
        w15 = request.POST.get("w15")
        p15 = request.POST.get("p15")
        c15 = request.POST.get("c15")
        if not c15:
            c15 = 0
        w16 = request.POST.get("w16")
        p16 = request.POST.get("p16")
        c16 = request.POST.get("c16")
        if not c16:
            c16 = 0
        conlist = []
        if int(c1) > 0:
            condict = {"name": w1, "price": p1, "count": c1}
            conlist.append(condict)
        if int(c2) > 0:
            condict = {"name": w2, "price": p2, "count": c2}
            conlist.append(condict)
        if int(c3) > 0:
            condict = {"name": w3, "price": p3, "count": c3}
            conlist.append(condict)
        if int(c4) > 0:
            condict = {"name": w4, "price": p4, "count": c4}
            conlist.append(condict)
        if int(c5) > 0:
            condict = {"name": w5, "price": p5, "count": c5}
            conlist.append(condict)
        if int(c6) > 0:
            condict = {"name": w6, "price": p6, "count": c6}
            conlist.append(condict)
        if int(c7) > 0:
            condict = {"name": w7, "price": p7, "count": c7}
            conlist.append(condict)
        if int(c8) > 0:
            condict = {"name": w8, "price": p8, "count": c8}
            conlist.append(condict)
        if int(c9) > 0:
            condict = {"name": w9, "price": p9, "count": c9}
            conlist.append(condict)
        if int(c10) > 0:
            condict = {"name": w10, "price": p10, "count": c10}
            conlist.append(condict)
        if int(c11) > 0:
            condict = {"name": w11, "price": p11, "count": c11}
            conlist.append(condict)
        if int(c12) > 0:
            condict = {"name": w12, "price": p12, "count": c12}
            conlist.append(condict)
        if int(c13) > 0:
            condict = {"name": w13, "price": p13, "count": c13}
            conlist.append(condict)
        if int(c14) > 0:
            condict = {"name": w14, "price": p14, "count": c14}
            conlist.append(condict)
        if int(c15) > 0:
            condict = {"name": w15, "price": p15, "count": c15}
            conlist.append(condict)
        if int(c16) > 0:
            condict = {"name": w16, "price": p16, "count": c16}
            conlist.append(condict)

        if len(conlist) == 0:
            tips = "Error:您未选择拼团数量，请重新选择后提交！"
            return render(request, "error.html", {'tips': tips})

        pdata = Pinsubject.objects.get(pid=pinid)
        if pdata.yunum == 1:
            pdata.yunum -= 1
            pdata.state = "已结束"
            pdata.save()
        elif pdata.yunum > 1:
            pdata.yunum -= 1
            pdata.save()
        else:
            tips = "Error:犹豫了一秒，拼团人数已满！"
            return render(request, "error.html", {'tips': tips})

        pindata = Pindata(
            uid = request.user.id,
            username=request.user.username,
            pinid=pinid,
            tel=tel,
            content=conlist,
            remark=remark,
            state="未支付",
            createtime=datetime.datetime.now()
        )
        pindata.save()
        return redirect("cook.html")

@login_required()
def modelset(request):
    data = Pinmodel.objects.filter(userid=request.user.id)
    return render(request, "modelset.html", {'data': data})

@login_required()
def modelchange(request):
    if request.method == "GET":
        pid = request.GET.get("pid")
        pdata = Pinmodel.objects.get(id=pid)
        plist = []
        plist.append(pdata.name)
        pindata = pdata.content.replace("'", '"')
        pjson = json.loads(pindata)
        for d in pjson:
            plist.append(d.get("name"))
            plist.append(d.get("price"))
        tip = "更新模板"
        nid = pid
        return render(request, "createmodel.html", {'plist': plist, 'tip': tip, 'nid': nid})
    else:
        nid = request.POST.get("nid")
        name = request.POST.get('name')
        w1 = request.POST.get("w1")
        p1 = request.POST.get("p1")
        w2 = request.POST.get("w2")
        p2 = request.POST.get("p2")
        w3 = request.POST.get("w3")
        p3 = request.POST.get("p3")
        w4 = request.POST.get("w4")
        p4 = request.POST.get("p4")
        w5 = request.POST.get("w5")
        p5 = request.POST.get("p5")
        w6 = request.POST.get("w6")
        p6 = request.POST.get("p6")
        w7 = request.POST.get("w7")
        p7 = request.POST.get("p7")
        w8 = request.POST.get("w8")
        p8 = request.POST.get("p8")
        w9 = request.POST.get("w9")
        p9 = request.POST.get("p9")
        w10 = request.POST.get("w10")
        p10 = request.POST.get("p10")
        w11 = request.POST.get("w11")
        p11 = request.POST.get("p11")
        w12 = request.POST.get("w12")
        p12 = request.POST.get("p12")
        w13 = request.POST.get("w13")
        p13 = request.POST.get("p13")
        w14 = request.POST.get("w14")
        p14 = request.POST.get("p14")
        w15 = request.POST.get("w15")
        p15 = request.POST.get("p15")
        w16 = request.POST.get("w16")
        p16 = request.POST.get("p16")
        conlist = []
        if w1:
            condict = {"name": w1, "price": p1}
            conlist.append(condict)
        if w2:
            condict = {"name": w2, "price": p2}
            conlist.append(condict)
        if w3:
            condict = {"name": w3, "price": p3}
            conlist.append(condict)
        if w4:
            condict = {"name": w4, "price": p4}
            conlist.append(condict)
        if w5:
            condict = {"name": w5, "price": p5}
            conlist.append(condict)
        if w6:
            condict = {"name": w6, "price": p6}
            conlist.append(condict)
        if w7:
            condict = {"name": w7, "price": p7}
            conlist.append(condict)
        if w8:
            condict = {"name": w8, "price": p8}
            conlist.append(condict)
        if w9:
            condict = {"name": w9, "price": p9}
            conlist.append(condict)
        if w10:
            condict = {"name": w10, "price": p10}
            conlist.append(condict)
        if w11:
            condict = {"name": w11, "price": p11}
            conlist.append(condict)
        if w12:
            condict = {"name": w12, "price": p12}
            conlist.append(condict)
        if w13:
            condict = {"name": w13, "price": p13}
            conlist.append(condict)
        if w14:
            condict = {"name": w14, "price": p14}
            conlist.append(condict)
        if w15:
            condict = {"name": w15, "price": p15}
            conlist.append(condict)
        if w16:
            condict = {"name": w16, "price": p16}
            conlist.append(condict)
        pdata = Pinmodel.objects.get(id=nid)
        pdata.name = name
        pdata.content = conlist
        pdata.save()
        return redirect("modelset.html")


@login_required()
def success(request):
    pid = request.GET.get("pid")
    if not pid:
        tips = "Error:发生未知错误，请返回！"
        return render(request, "error.html", {'tips': tips})
    pdata = Pinsubject.objects.get(pid=pid)
    data = pdata.name
    return render(request, "success.html", {'pid': pid, "data": data})


@login_required()
def error(request):
    tips = "2022, 虎虎生威"
    return render(request, "error.html", {'tips': tips})

@login_required()
def alllist(request):
    if request.method == "GET":
        pdata = Pinsubject.objects.all().order_by("-state")
        return render(request, "alllist.html", {'pdata': pdata})
    else:
        pid = request.POST.get('search')
        pdata = Pinsubject.objects.filter(pid=pid)
        return render(request, "alllist.html", {'pdata': pdata, 'pid': pid})


@login_required()
def tuanlist(request):
    if request.method == "GET":
        userid = request.user.id
        pdata = Pinsubject.objects.filter(userid=userid)
        return render(request, 'tuanlist.html', {'pdata': pdata})
    else:
        pid = request.POST.get('search')
        pdata = Pinsubject.objects.filter(pid=pid, userid=request.user.id)
        return render(request, 'tuanlist.html', {'pdata': pdata})


@login_required()
def look(request):
    pid = request.GET.get("pid")
    name = request.GET.get("name")
    if not pid or not name:
        tips = "Error:出现错误，请返回！"
        return render(request, "error.html", {'tips': tips})
    else:
        pdata = Pinsubject.objects.get(pid=pid)
        xdata = Pindata.objects.get(pinid=pid, username=name)
        product = json.loads(xdata.content.replace("'", '"'))
        return render(request, "look.html", {"pdata": pdata, "xdata": xdata, "product": product})

@login_required()
def deal(request):
    pid = request.GET.get("pid")
    name = request.GET.get("name")
    if not pid or not name:
        tips = "Error:出现位置错误，请返回！"
        return render(request, "error.html", {'tips': tips})
    else:
        xdata = Pindata.objects.get(pinid=pid, username=name)
        xdata.state = "已支付"
        xdata.save()
        ndata = Pindata.objects.filter(pinid=pid)
        t = 0
        for n in ndata:
            if n.state == "已支付":
                t += 1
        if len(ndata) == t:
            ydata = Pindata.objects.filter(pinid=pid)
            for x in ydata:
                x.state = "已结束"
                x.save
            mdata = Pinsubject.objects.get(pid=pid)
            mdata.state = "已结束"
            mdata.save()
        return redirect("cook.html")


@login_required()
def delit(request):
    pid = request.GET.get("pid")
    name = request.GET.get("name")
    if not pid or not name:
        tips = "Error:发生未知错误，请返回！"
        return render(request, "error.html", {'tips': tips})
    pdata = Pindata.objects.get(pinid=pid, username=name)
    pdata.delete()
    xdata = Pinsubject.objects.get(pid=pid)
    xdata.yunum += 1
    xdata.state = "拼团中"
    xdata.save()
    return redirect("cook.html")
