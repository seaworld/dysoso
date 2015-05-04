#coding=utf8

from django.shortcuts import render
import pymongo
import datetime
from bson.objectid import ObjectId

from dysoso import settings

if settings.INLOCALE:
    con = pymongo.MongoClient(host='192.168.1.116')
    staticdebughost='http://192.168.1.116'
else:
    con = pymongo.MongoClient()
    staticdebughost=''

db=con['dysoso']

def indexhtml(request):
    newlist = db.film.find().sort("updatetime",-1)[:10]
    newlist = [getmongoid(x) for x in newlist]
    #月排行榜，向前推5天换这个月的。
    today = datetime.date.today()-datetime.timedelta(days=5)
    hotmonthlist = db.viewinfo.find().sort(str(today.year)+str(today.month),-1)[:10]
    #这是个游标,只能读一次
    hotmonthlist = [x for x in hotmonthlist]
    hotmonth = db.film.find({"_id":{"$in":[x['_id'] for x in hotmonthlist]}})
    hotmonth = [x for x in hotmonth]
    hotmonth = [ y for x in hotmonthlist for y in hotmonth if x['_id']==y['_id']]
    hotmonth = [ getmongoid(x) for x in hotmonth ] 
    
    nph = getpaihang("nowplaying",0,10)
    top100 = getpaihang("top100",0,10)

    return render(request,'index.html',{'newlist':newlist,'hotmonth':hotmonth,'nowplaying':nph,"top100":top100})

def detailhtml(request,dyid):
    onedy =  db.film.find_one({"_id": ObjectId(dyid)})
    if onedy:
        getimage(onedy)
        onedy["staticdebughost"]=staticdebughost
        today = datetime.date.today()
        db.viewinfo.update({"_id":onedy["_id"]},{"$inc":{"count":1,str(today.year)+str(today.month):1,str(today.year)+"."+str(today.month)+"."+str(today.day):1},"$set":{"updatedate":datetime.datetime.now()}},upsert = True)
        onedy["url"] = onedy["url"].replace("http://www.ffdy.cc/","http://www.poxiao.com/")
    return render(request,'detail.html',onedy)

def listhtml(request,search_type):
    page = request.GET.get('page',"1")
    page = int(page) if page.isdigit() and int(page)> 0  else 1
    kw = request.GET.get('kw',"")
    kw = "".join([x for x in kw if x.isalnum()])
    if search_type == "newest.html":
        dylist =  db.film.find().sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "yuelist.html":
        dylist,pagecount  =  getyuelist(page)
    elif search_type == "country":
        dylist =  db.film.find({"country":{"$regex":kw}}).sort("updatedate",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "year":
        dylist =  db.film.find({"year":{"$regex":kw}}).sort("updatedate",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "type":
        dylist =  db.film.find({"mtype":{"$regex":kw}}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    else:
        dylist = db.film.find()[:10]
        pagecount=1
    dylist = [ getmongoid(x) for x in dylist ]
    dylist = [getimage(x) for x in dylist]
    pagelist = range(page-3 if page>3 else 1 , page+4 if page<pagecount-3 else pagecount+1)
    return render(request,'list.html',{'dylist':dylist,"pagenow":page,"pagecount":pagecount,"pagelist":pagelist,"kw":kw,"staticdebughost":staticdebughost})


def typehtml(request,search_type):
    page = request.GET.get('page',"1")
    page = int(page) if page.isdigit() and int(page)> 0  else 1
    mtype = request.GET.get("mtype")
    if mtype:
        mtype  = "".join([x for x in mtype if x.isalnum()])
    if search_type == "dsj":
        if mtype:
            dylist = db.film.find({"atype":"电视剧","mtype":{"$regex":mtype}}).sort("updatetime",-1)[(page-1)*10:page*10]
        else:
            dylist =  db.film.find({"atype":"电视剧"}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "anim":
        if mtype:
            dylist = db.film.find({"atype":{"$regex":"动画"},"mtype":{"$regex":mtype}}).sort("updatetime",-1)[(page-1)*10:page*10]
        else:
            dylist =  db.film.find({"atype":{"$regex":"动画"}}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "zongyi":
        if mtype:
            dylist = db.film.find({"atype":"综艺","mtype":{"$regex":mtype}}).sort("updatetime",-1)[(page-1)*10:page*10]
        else:
            dylist =  db.film.find({"atype":"综艺"}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "3d":
        if mtype:
            dylist = db.film.find({"atype":{"$regex":"3D"},"mtype":{"$regex":mtype}}).sort("updatetime",-1)[(page-1)*10:page*10]
        else:
            dylist =  db.film.find({"atype":{"$regex":"3D"}}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10
    elif search_type == "yugao":
        if mtype:
            dylist = db.film.find({"atype":{"$regex":"预告"},"mtype":{"$regex":mtype}}).sort("updatetime",-1)[(page-1)*10:page*10]
        else:
            dylist =  db.film.find({"atype":{"$regex":"预告"}}).sort("updatetime",-1)[(page-1)*10:page*10]
        pagecount = (dylist.count()+9)/10

    else:
        dylist = db.film.find()[:10]
        pagecount=1
    dylist = [ getmongoid(x) for x in dylist ]
    dylist = [ getimage(x) for x in dylist]
    pagelist = range(page-3 if page>3 else 1 , page+4 if page<pagecount-3 else pagecount+1)
    return render(request,'list.html',{'dylist':dylist,"pagenow":page,"pagecount":pagecount,"pagelist":pagelist,"staticdebughost":staticdebughost})


def search(request):

    page = request.GET.get('page',"1")
    page = int(page) if page.isdigit() and int(page)> 0  else 1
    kw = request.GET.get('kw',"")
    kw = "".join([x for x in kw if x.isalnum()])
    did = request.GET.get('did',"")
    dinfo=None
    if did:
        dinfo = db.douban.find_one({"id":did})
    dylist =  db.film.find({"$or":[{"title":{"$regex":kw}},{"alt_title":{"$regex":kw}},{"cast":{"$regex":kw}},{"director":{"$regex":kw}},{"writer":{"$regex":kw}}]}).sort("_id",-1)[(page-1)*10:page*10]
    pagecount = (dylist.count()+9)/10
    dylist = [ getmongoid(x) for x in dylist ]
    dylist = [ getimage(x) for x in dylist]
    pagelist = range(page-3 if page>3 else 1 , page+4 if page<pagecount-3 else pagecount+1)
    #搜索统计
    db.searchinfo.insert({"kw":kw,"sdate":datetime.datetime.now()})
    return render(request,'search.html',{'dylist':dylist,"pagenow":page,"pagecount":pagecount,"kw":kw,"pagelist":pagelist,"staticdebughost":staticdebughost,"dinfo":dinfo})

def paihanghtml(request,paihang_type):
    if paihang_type == 'playing':
        nph = getpaihang("nowplaying") 
        lph = getpaihang("laterplaying") 
        npph = getpaihang("guoneipiaofang")
        return render(request,'nowplaying.html',{'nowplaying':nph,"laterplaying":lph,"guoneipiaofang":npph})
    if paihang_type =="top100":
        dylist = getpaihang("top100")
        return render(request,'top100.html',{'dylist':dylist})
    return "404"

def getyuelist(page):
    #月排行榜，向前推5天换这个月的。
    today = datetime.date.today()-datetime.timedelta(days=5)
    hotmonthlist = db.viewinfo.find().sort(str(today.year)+str(today.month),-1)[(page-1)*10:page*10]
    hotmonthlistCount = hotmonthlist.count()
    #这是个游标,只能读一次
    hotmonthlist = [x for x in hotmonthlist]
    hotmonth = db.film.find({"_id":{"$in":[x['_id'] for x in hotmonthlist]}})
    hotmonth = [x for x in hotmonth]
    hotmonth = [ y for x in hotmonthlist for y in hotmonth if x['_id']==y['_id']]
    return hotmonth , hotmonthlistCount


def getpaihang(pname,start=0,end=0):
    paihang = db.plist.find({"pname":pname}).sort("today",-1)
    if paihang and paihang[0].get('plist'):
        plist = paihang[0]['plist']
        if end!=0:
            plist = plist[start:end]
        return plist
    return None   
         

def getmongoid(x):
    x['id']=x['_id']
    return x

def getimage(x):
    if x["images"]:
        x["image"]=x["images"][0].get("path")
    return x
