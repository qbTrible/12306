from tkinter import *
from PIL import ImageTk,Image
import requests
import time
import datetime
import random
from json import loads
from prettytable import PrettyTable
import re
from urllib import parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
'''禁用安全请求警告'''
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def load_ua():
    ua_file = 'user_agents.txt'
    uas = []
    with open(ua_file, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    _ua = random.choice(uas)
    return _ua

session = requests.Session()
headers = {'User-Agent':load_ua()}

sanzima_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9025"
resq = requests.get(url=sanzima_url, headers=headers)
dict = resq.content.decode('utf-8')
dict = dict.split('|')
sanzima = {}
for i in range(len(dict)):
    if (i - 1) % 5 == 0:
        sanzima[dict[i]] = dict[i + 1]
rsanzima = {}
for key in sanzima:
    rsanzima[sanzima[key]] = key

def chaxun():
    root = Tk()
    isstudent = StringVar()
    isstudent.set("0")

    def execute():
        text1.delete(1.0, END)
        start1 = entry1.get()
        to1 = entry2.get()
        date = entry3.get()
        if len(date)==0:
            entry3.delete(0, END)
            date=str(time.strftime("%Y-%m-%d"))
            entry3.insert(END,time.strftime("%Y-%m-%d"))
        if len(start1)==0 or len(to1)==0:
            text3.insert(END,"请输入出发地和目的地\n")
            raise Exception
        if (isstudent.get() == "0"):
            student = "ADULT"
        else:
            student = "0X00"
        try:
            start = sanzima[start1]
            to = sanzima[to1]
        except Exception:
            text3.insert(END,"请正确输入地名\n")
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + \
              start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
        try:
            res = requests.get(url=url, headers=headers)
        except Exception:
            text3.insert(END,"ip无法访问\n")
        data = res.content.decode('utf-8')
        patcode = '订\|.*?\|(.*?)\|'
        code = re.compile(patcode).findall(data, re.S)  # 车次
        patfrom = '订\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        fromname = re.compile(patfrom).findall(data, re.S)  # 出发站名
        patto = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        toname = re.compile(patto).findall(data, re.S)  # 到达站名
        patstime = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        stime = re.compile(patstime).findall(data, re.S)  # 出发时间
        patatime = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        atime = re.compile(patatime).findall(data, re.S)  # 到达时间
        patltime = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        ltime = re.compile(patltime).findall(data, re.S)  # 历时
        seat_yideng = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yideng = re.compile(seat_yideng).findall(data, re.S)  # 一等座

        for i in range(len(yideng)):
            if yideng[i] == '':
                yideng[i] = '--'
        seat_erdeng = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        erdeng = re.compile(seat_erdeng).findall(data, re.S)  # 二等座
        for i in range(len(erdeng)):
            if erdeng[i] == '':
                erdeng[i] = '--'
        seat_yingzuo = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yingzuo = re.compile(seat_yingzuo).findall(data, re.S)  # 硬座
        for i in range(len(yingzuo)):
            if yingzuo[i] == '':
                yingzuo[i] = '--'
        seat_yingwo = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yingwo = re.compile(seat_yingwo).findall(data, re.S)  # 硬卧
        for i in range(len(yingwo)):
            if yingwo[i] == '':
                yingwo[i] = '--'
        seat_wu = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        wu = re.compile(seat_wu).findall(data, re.S)  # 无座
        for i in range(len(wu)):
            if wu[i] == '':
                wu[i] = '--'
        seat_ruanzuo = '订\|.*?\|\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        ruanzuo = re.compile(seat_ruanzuo).findall(data, re.S)  # 软座
        for i in range(len(ruanzuo)):
            if ruanzuo[i] == '':
                ruanzuo[i] = '--'
        seat_ruanwo = '订\|.*?\|\|.*?\|.*?\|(.*?)\|.*?"'
        ruanwo = re.compile(seat_ruanwo).findall(data, re.S)  # 软卧
        for i in range(len(ruanwo)):
            if ruanwo[i] == '':
                ruanwo[i] = '--'
        result = PrettyTable(["车次", "出发站名", "到达站名", "出发时间", "达到时间", "历时", "一等座",
                              "二等座", "硬卧", "软卧", "硬座", "软座", "无座"])
        for i in range(0, len(code)):
            result.add_row([code[i], rsanzima[fromname[i]], rsanzima[toname[i]], stime[i], atime[
                i], ltime[i], yideng[i], erdeng[i], yingwo[
                                i], ruanwo[i], yingzuo[i], ruanzuo[i], wu[i]])
            row = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " "]
            result.add_row(row)
        text1.insert(END, result)

    def shuapiao():
        global info,checi,zuowei,date,code
        text1.delete(1.0, END)
        text3.delete(1.0, END)
        start1 = entry1.get()
        to1 = entry2.get()
        date = entry3.get()
        checi=entry4.get()
        zuowei=entry5.get()
        if len(date)==0:
            entry3.delete(0, END)
            date=str(time.strftime("%Y-%m-%d"))
            entry3.insert(END,time.strftime("%Y-%m-%d"))
        if len(start1)==0 or len(to1)==0:
            text3.insert(END,"请输入出发地和目的地\n")
            raise Exception
        if (isstudent.get() == "0"):
            student = "ADULT"
        else:
            student = "0X00"
        try:
            start = sanzima[start1]
            to = sanzima[to1]
        except Exception:
            text3.insert(END,"请正确输入地名\n")
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + \
              start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
        try:
            res = requests.get(url=url, headers=headers)
        except Exception:
            text3.insert(END,"ip无法访问\n")
        data = res.content.decode('utf-8')
        patcode = '订\|.*?\|(.*?)\|'
        code = re.compile(patcode).findall(data, re.S)  # 车次
        patfrom = '订\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        fromname = re.compile(patfrom).findall(data, re.S)  # 出发站名
        patto = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        toname = re.compile(patto).findall(data, re.S)  # 到达站名
        seat_yideng = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yideng = re.compile(seat_yideng).findall(data, re.S)  # 一等座
        seat_erdeng = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        erdeng = re.compile(seat_erdeng).findall(data, re.S)  # 二等座
        seat_yingzuo = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yingzuo = re.compile(seat_yingzuo).findall(data, re.S)  # 硬座
        seat_yingwo = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        yingwo = re.compile(seat_yingwo).findall(data, re.S)  # 硬卧
        seat_wu = '订\|.*?\|\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        wu = re.compile(seat_wu).findall(data, re.S)  # 无座
        seat_ruanzuo = '订\|.*?\|\|.*?\|.*?\|.*?\|(.*?)\|.*?"'
        ruanzuo = re.compile(seat_ruanzuo).findall(data, re.S)  # 软座
        seat_ruanwo = '订\|.*?\|\|.*?\|.*?\|(.*?)\|.*?"'
        ruanwo = re.compile(seat_ruanwo).findall(data, re.S)  # 软卧
        info={}
        for i in range(0, len(code)):
            info[code[i]]={"一等座":yideng[i],"二等座":erdeng[i],"硬卧":yingwo[i],"软卧":ruanwo[i],"硬座":yingzuo[i],
                           "软座":ruanzuo[i],"无座":wu[i]}
    def jiankong():
        shuapiao()
        execute()
        num=0
        dic=[]
        for key in info:
            for key1 in info[key]:
                if info[key][key1]!="无" and info[key][key1]!="":
                    num+=1
                    dic.append(key)
                    break
        if num!=0:
            text3.delete(1.0,END)
            text3.insert(END,"成功查到"+date+"的"+dic[0]+"次等"+str(num)+"趟车有票")
        else:
            jiankong()

    def shua():
        text3.delete(1.0,END)
        text3.insert(END,"刷票中，请耐心等待...")
        def shua_piao():
            minutes=entry6.get()
            root4.destroy()
            count = 0
            while count <= eval(minutes)*60:
                shuapiao()
                execute()
                if len(checi) == 0:
                    text3.insert(END, "请输入车次\n")
                else:
                    if checi not in code:
                        text3.insert(END, "请正确输入车次\n")
                    else:
                        if len(zuowei) == 0:
                            text3.delete(1.0, END)
                            text3.insert(END, "请输入座位类型\n")
                            raise Exception
                        else:
                            if zuowei in ["一等座", "二等座", "硬卧", "软卧", "硬座", "无座", "软座"]:
                                if info[checi][zuowei] != "":
                                    pass
                                else:
                                    text2.insert(END, "该列车无此座位")
                                    raise Exception
                            else:
                                text3.delete(1.0, END)
                                text3.insert(END, "请正确输入座位类型\n")
                                raise Exception("请正确输入座位类型")

                if info[checi][zuowei] != "无" and info[checi][zuowei] != "":
                    text3.delete(1.0, END)
                    text3.insert(END, checi+"车次"+zuowei+"的票刷票成功！剩余票数：" + info[checi][zuowei] + "，请及时订票!\n")
                    break
                else:
                    text3.delete(1.0, END)
                    text3.insert(END, "很遗憾，未刷到"+checi+"次"+zuowei+"的票！您可以换个姿势再来一次。\n")
                    seconds = random.randint(1, 5)
                    time.sleep(seconds)
                    count += seconds

        root4 = Tk()
        root4.geometry("300x200+450+200")
        title = root4.title("设置刷票时间")
        fm = Frame(root4)
        label9 = Label(fm, text="设置").grid(row=0, column=0, pady=20)
        entry6 = Entry(fm, width=6)
        entry6.grid(row=0, column=1, padx=3, pady=20)
        label10 = Label(fm, text="分钟后停止刷票").grid(row=0, column=2, pady=20)
        fm.grid(row=0, column=0, padx=60, pady=20, sticky="ns")
        button6 = Button(root4, text="确定", width=10, command=shua_piao, bg="skyblue").grid(row=1, column=0, columnspan=3, pady=10)
        root4.mainloop()

    title = root.title("12306火车票订票系统")
    root.geometry("880x650+180+20")

    def piaojia():
        global start1,to1,date,start,to,traindata,traindata2,traindata3,student
        text2.delete(0, END)
        text3.delete(1.0, END)
        start1 = entry1.get()
        to1 = entry2.get()
        date = entry3.get()
        if (isstudent.get() == "0"):
            student = "ADULT"
        else:
            student = "0X00"
        start = sanzima[start1]
        to = sanzima[to1]
        session = requests.Session()
        bookurl = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + \
                  start + "&leftTicketDTO.to_station=" + to + "&purpose_codes=" + student
        res = session.get(bookurl, headers=headers)
        dic = res.content.decode('utf-8')
        patcode1 = '订\|.*?\|(.*?)\|'
        code1 = re.compile(patcode1).findall(dic, re.S)  # 车次
        patstime = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        stime = re.compile(patstime).findall(dic, re.S)  # 出发时间
        patfrom = '订\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        fromname = re.compile(patfrom).findall(dic, re.S)  # 出发站名
        patto = '订\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|'
        toname = re.compile(patto).findall(dic, re.S)  # 到达站名
        dic = loads(dic)
        dic = dic['data']['result']
        traindata = {}
        traindata2 = {}
        traindata3={}
        train_no = []
        fs_no = []
        ts_no = []
        sec = []
        seattype = []
        for i in dic:
            dict = i.split('|')
            train_no.append(dict[2])
            fs_no.append(dict[16])
            ts_no.append(dict[17])
            seattype.append(dict[-2])
            sec.append(dict[0])
        for i in range(len(code1)):
            traindata2[code1[i]] = [train_no[i], fs_no[i], ts_no[i], seattype[i]]
            traindata[code1[i]] = sec[i]
            traindata3[code1[i]]=[stime[i],fromname[i],toname[i]]
        seat = entry5.get()
        checi = entry4.get()
        if len(checi)==0:
            text3.insert(END,"请输入车次\n")
        else:
            if checi not in code1:
                text3.insert(END,"请正确输入车次\n")
        checkurl = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=" + traindata2[checi][0] + "&from_station_no=" \
                   + traindata2[checi][1] + "&to_station_no=" + traindata2[checi][2] + "&seat_types=" + \
                   traindata2[checi][3] + "&train_date=" + date
        resq1 = session.get(url=checkurl, headers=headers)
        dict1 = resq1.content.decode('utf-8')
        dict1 = loads(dict1)
        s_type = {"硬座": "A1", "软座": "A2", "硬卧": "A3", "软卧": "A4", "一等座": "M", "二等座": "O", "无座": "WZ"}
        if len(seat)==0:
            text3.delete(1.0,END)
            text3.insert(END,"请输入座位类型\n")
            raise Exception
        else:
            if seat in ["一等座", "二等座", "硬卧", "软卧", "硬座", "无座","软座"]:
                if s_type[seat] in dict1["data"]:
                    price = dict1["data"][s_type[seat]]
                    text2.insert(END, price)
                else:
                    text2.insert(END,"该列车无此座位")
                    raise Exception
            else:
                text3.delete(1.0, END)
                text3.insert(END, "请正确输入座位类型\n")
                raise Exception("请正确输入座位类型")

    def dingpiao():
        text3.delete(1.0, END)
        if len(entry5.get())==0 or len(entry4.get())==0:
            text3.insert(END,"请输入车次和座位类型\n")
        piaojia()
        tk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        tkdata = {'appid': 'otn', "_json_att": ""}
        resp3 = session.post(tk_url, data=tkdata, headers=headers)
        response3 = resp3.content.decode('utf-8')
        response3 = loads(response3)
        if response3["result_code"] == 0:
            text3.insert(END, "第一次验证通过\n")
            newapptk = response3['newapptk']
            yz2data = {'tk': newapptk, "_json_att": ""}
            client_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            resp4 = session.post(client_url, data=yz2data, headers=headers)
            response4 = resp4.content.decode('utf-8')
            response4 = loads(response4)
            if response4["result_code"] == 0:
                text3.insert(END, "第二次验证通过\n")
            else:
                root.destroy()
                startmain()
        else:
            root.destroy()
            startmain()

        '''确认用户状态'''
        checkurl = "https://kyfw.12306.cn/otn/login/checkUser"
        checkdata = {"_json_att": ""}
        res4 = session.post(url=checkurl, headers=headers, data=checkdata, verify=False)
        dic4 = res4.content.decode('utf-8')
        dic4 = loads(dic4)
        if dic4["data"]["flag"] == True:
            text3.insert(END, "用户状态确认成功\n")
        else:
            root.destroy()
            startmain()
        '''座位类型函数'''
        seat_type = {"一等座": "M", "二等座": "O", "硬卧": "3", "软卧": "4", "硬座": "1", "无座": "1"}

        '''进行"预订"提交'''
        thiscode = entry4.get()
        seatStr = entry5.get()
        seat = seat_type[seatStr]
        backdate = datetime.datetime.now()
        backdate = backdate.strftime("%Y-%m-%d")
        submiturl = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        submitdata = {
            "secretStr": parse.unquote(traindata[thiscode]),
            "train_date": date,
            "back_train_date": backdate,
            "tour_flag": "dc",
            "purpose_codes": student,
            "query_from_station_name": start1,
            "query_to_station_name": to1,
            "undefined": ""
        }
        res5 = session.post(url=submiturl, headers=headers, data=submitdata, verify=False)
        dic5 = res5.content.decode('utf-8')
        dic5 = loads(dic5)
        if dic5["status"] == True:
            text3.insert(END, "提交预订请求成功\n")
        else:
            root.destroy()
            startmain()

        '''获取Token'''
        initdcurl = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        initdcdata = {"_json_att": ""}
        res6 = session.post(url=initdcurl, headers=headers, data=initdcdata, verify=False)
        dic6 = res6.content.decode('utf-8')
        # 获取token
        pattoken = "globalRepeatSubmitToken = '(.*?)'"
        tokenall = re.compile(pattoken).findall(dic6)
        if (len(tokenall) != 0):
            token = tokenall[0]
        else:
            text3.insert(END, "Token获取失败，请重试\n")
        # 获取leftTicketStr
        patleft = "'leftTicketStr':'(.*?)'"
        leftstrall = re.compile(patleft).findall(dic6)
        if (len(leftstrall) != 0):
            leftstr = leftstrall[0]
        else:
            text3.insert(END, "leftTicketStr 获取失败，请重试\n")
        # 获取key_check_isChange
        patkey = "'key_check_isChange':'(.*?)'"
        keyall = re.compile(patkey).findall(dic6)
        if (len(keyall) != 0):
            key = keyall[0]
        else:
            text3.insert(END, "key_check_isChange 获取失败，请重试\n")
        # 获取train_location
        pattrain_location = "'train_location':'(.*?)'"
        train_locationall = re.compile(pattrain_location).findall(dic6)
        if (len(train_locationall) != 0):
            train_location = train_locationall[0]
        else:
            text3.insert(END, "train_location 获取失败，请重试\n")

        '''获取乘客信息'''
        piurl = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
        pidata = {"_json_att": "",
                  "REPEAT_SUBMIT_TOKEN": token}
        res2 = session.post(url=piurl, headers=headers, data=pidata)
        dic2 = res2.content.decode('utf-8')
        patname = '"passenger_name":"(.*?)"'
        name = re.compile(patname).findall(dic2)  # 提取姓名
        patsex = '"sex_name":"(.*?)"'
        sex = re.compile(patsex).findall(dic2)  # 提取性别
        patid = '"passenger_id_no":"(.*?)"'
        id = re.compile(patid).findall(dic2)  # 提取身份证号
        pattype = '"passenger_type_name":"(.*?)"'
        type = re.compile(pattype).findall(dic2)  # 提取乘客类型
        patcountry = '"country_code":"(.*?)"'
        country = re.compile(patcountry).findall(dic2)  # 提取乘客所在国家
        patmobile = '"mobile_no":"(.*?)"'
        mobile = re.compile(patmobile).findall(dic2)  # 提取乘客手机号

        def tijiao():
            chooseno = entry.get()
            if len(chooseno)==0:
                text3.delete(5.0, END)
                text3.insert(END, "\n请输入选择的用户序号\n")
            else:
                if chooseno.isdigit():
                    if int(chooseno)>len(name):
                        text3.delete(5.0,END)
                        text3.insert(END,"\n请正确输入选择的用户序号\n")
                    thisno = int(chooseno) - 1
                else:
                    text3.delete(5.0, END)
                    text3.insert(END, "\n请正确输入选择的用户序号\n")

            '''提交订单，第一次请求'''
            checkOrderurl = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
            checkOderdata = {
                "cancel_flag": "2",
                "bed_level_order": "000000000000000000000000000000",
                "passengerTicketStr": seat + ",0,1" + "," + str(name[thisno]) + ",1" + "," + str(
                    id[thisno]) + "," + str(
                    mobile[thisno]) + "," + str(country[thisno]),
                "oldPassengerStr": str(name[thisno]) + ",1" + "," + str(id[thisno]) + ",1_",
                "tour_flag": "dc",
                "randCode": "",
                "whatsSelect": "1",
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token
            }

            res7 = session.post(url=checkOrderurl, headers=headers, data=checkOderdata)
            dic7 = res7.content.decode('utf-8')
            dict7 = loads(dic7)
            if dict7["status"] == True:
                pass
            else:
                root.destroy()
                startmain()
            root1.destroy()
            '''提交订单，第二次请求'''
            getqueurl = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
            thisdate = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            gmt = "%a %b %d %Y"
            thisgmtdate = thisdate.strftime(gmt)  # 转化为格林时间
            getquedata = {
                "train_date": str(thisgmtdate) + " 00:00:00 GMT+0800",
                "train_no": traindata2[thiscode][0],
                "stationTrainCode": thiscode,
                "seatType": seat,
                "fromStationTelecode": start,
                "toStationTelecode": to,
                "leftTicket": leftstr,
                "purpose_codes": "00",
                "train_location": train_location,
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token
            }
            res8 = session.post(url=getqueurl, headers=headers, data=getquedata)
            dic8 = res8.content.decode('utf-8')
            dict8 = loads(dic8)
            if dict8["status"] == True:
                pass
            else:
                root.destroy()
                startmain()

            '''确认订单，第一次请求'''
            confurl = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
            confdata = {
                "passengerTicketStr": seat + ",0,1" + "," + str(name[thisno]) + ",1" + "," + str(
                    id[thisno]) + "," + str(
                    mobile[thisno]) + "," + str(country[thisno]),
                "oldPassengerStr": str(name[thisno]) + ",1," + str(id[thisno]) + ",1_",
                "randCode": "",
                "purpose_codes": "00",
                "key_check_isChange": key,
                "leftTicketStr": leftstr,
                "train_location": train_location,
                "choose_seats": "",
                "seatDetailType": "000",
                "whatsSelect": "1",
                "roomType": "00",
                "dwAll": "N",
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token
            }
            res9 = session.post(url=confurl, headers=headers, data=confdata)
            dic9 = res9.content.decode('utf-8')
            time1 = time.time()
            '''确认订单，第二次请求'''
            while True:
                time2 = time.time()
                if ((time2 - time1) // 60 > 5):
                    text3.insert(END, "获取orderid超时，正在进行新一次抢购\n")
                    break
                getorderidurl = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=" + str(
                    token)
                res10 = session.get(url=getorderidurl, headers=headers)
                dic10 = res10.content.decode('utf-8')
                patorderid = '"orderId":"(.*?)"'
                orderidall = re.compile(patorderid).findall(dic10)
                if (len(orderidall) == 0):
                    continue
                else:
                    orderid = orderidall[0]
                    break

            '''确认订单，第三次请求'''
            resulturl = "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
            resultdata = {
                "orderSequence_no": orderid,
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token
            }
            res11 = session.post(url=resulturl, headers=headers, data=resultdata)
            dic11 = res11.content.decode('utf-8')

            '''确认订单，第四次请求'''
            payurl = "https://kyfw.12306.cn/otn//payOrder/init"
            paydata = {
                "_json_att": "",
                "REPEAT_SUBMIT_TOKEN": token
            }
            res12 = session.post(url=payurl, headers=headers, data=paydata)
            dic12 = res12.content.decode('utf-8')
            text3.insert(END, "订单提交成功，请及时支付！30分钟内未支付，将自动取消订单。\n" + name[thisno] + "的订单号："
                         + orderid + "\n车次：" + rsanzima[traindata3[thiscode][1]] + "到" + rsanzima[traindata3[thiscode][2]] + " " + thiscode +
                         "\n座位类型：" + seatStr + "\n列车时间：" + date + " " + traindata3[thiscode][0] + "开\n")

        root1=Tk()
        title = root1.title("选择用户")
        root1.geometry("550x220+300+150")
        fm = Frame(root1)
        s = Scrollbar(fm)
        s.grid(row=0, column=1, sticky=N + S)
        text = Text(fm, width=70, height=10, padx=5, pady=5, yscrollcommand=s.set)
        text.grid(row=0, column=0)
        s.config(command=text.yview)
        fm.grid(row=0, padx=10, pady=10)
        fm1 = Frame(root1)
        label = Label(fm1, text="请选择第").grid(row=0, column=0, padx=5)
        entry = Entry(fm1, width=3)
        entry.grid(row=0, column=1)
        label1 = Label(fm1, text="位用户").grid(row=0, column=2, padx=5)
        button = Button(fm1, text="确定",command=tijiao, bg="skyblue").grid(row=0, column=3, padx=5)
        fm1.grid(row=1, padx=10)

        for i in range(len(name)):
            if country[i] == "CN":
                country[i] = "N"
                text.insert(END,"第" + str(i + 1) + "位用户： 姓名：" + str(name[i]) + ", 身份证号：" + str(id[i]) + ",乘客类型：" + str(type[i])+"\n")
        root1.mainloop()

    def checktk():
        root3 = Tk()
        root3.geometry("300x200+400+200")
        root3.title("确认取消")

        def quxiao():
            root3.destroy()
            '''查看订单'''
            orderurl = "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete"
            orderdata = {"_json_att": ""}
            orderres = session.post(url=orderurl, headers=headers, data=orderdata)
            orderdic = orderres.content.decode('utf-8')
            orderdic = loads(orderdic)
            orderid = orderdic["data"]["orderDBList"][0]["sequence_no"]
            '''取消订单'''
            cancelurl = "https://kyfw.12306.cn/otn/queryOrder/cancelNoCompleteMyOrder"
            canceldata = {
                "_json_att": "",
                "cancel_flag": "cancel_order",
                "sequence_no": orderid
            }
            cancelres = session.post(url=cancelurl, headers=headers, data=canceldata)
            canceldic = cancelres.content.decode('utf-8')
            canceldic = loads(canceldic)
            if canceldic["status"] == True:
                text3.insert(END, "订单取消成功\n")
            else:
                text3.insert(END, "订单取消失败\n")

        def destory():
            root3.destroy()

        fm1 = Frame(root3)
        label = Label(fm1, text="当天3次取消订单，当天将无法继续订票，是否确定取消", fg="red", font=("宋体", 15), wraplength=250)
        label.grid(row=0, column=0, pady=30)
        fm1.grid(row=0, column=0, padx=20, sticky="ns")
        fm2 = Frame(root3)
        button1 = Button(fm2, text="确定", bg="skyblue", command=quxiao)
        button1.grid(row=1, column=0, padx=50, pady=10)
        button2 = Button(fm2, text="取消", bg="skyblue", command=destory)
        button2.grid(row=1, column=1, padx=50, pady=10)
        fm2.grid(row=1, column=0, padx=20, sticky="ns")
        root3.mainloop()

    def cancelcheck():
        '''查看订单'''
        tk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        tkdata = {'appid': 'otn', "_json_att": ""}
        resp3 = session.post(tk_url, data=tkdata, headers=headers)
        response3 = resp3.content.decode('utf-8')
        response3 = loads(response3)
        if response3["result_code"] == 0:
            newapptk = response3['newapptk']
            yz2data = {'tk': newapptk, "_json_att": ""}
            client_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            resp4 = session.post(client_url, data=yz2data, headers=headers)
        checkurl = "https://kyfw.12306.cn/otn/login/checkUser"
        checkdata = {"_json_att": ""}
        res4 = session.post(url=checkurl, headers=headers, data=checkdata, verify=False)
        orderurl = "https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete"
        orderdata = {"_json_att": ""}
        orderres = session.post(url=orderurl, headers=headers, data=orderdata)
        orderdic = orderres.content.decode('utf-8')
        try:
            orderdic = loads(orderdic)
        except Exception:
            root.destroy()
            startmain()
        if "data" not in orderdic:
            text3.delete(1.0,END)
            text3.insert(END, "您没有未支付的订单，请先订票\n")
            raise Exception
        else:
            checktk()

    fm0 = Frame(root)
    r1 = Radiobutton(fm0, text="普通", variable=isstudent, value="0")
    r1.grid(row=0, column=0, padx=20, pady=10)
    r2 = Radiobutton(fm0, text="学生", variable=isstudent, value="1")
    r2.grid(row=1, column=0)

    label1 = Label(fm0, text="出发地").grid(row=0, column=1, padx=10)
    entry1 = Entry(fm0, width=10)
    entry1.grid(row=0, column=2)

    label2 = Label(fm0, text="目的地").grid(row=0, column=3, padx=10)
    entry2 = Entry(fm0, width=10)
    entry2.grid(row=0, column=4)

    label3 = Label(fm0, text="出发日期 (如: 2018-07-15)").grid(row=0, column=5, padx=8)
    entry3 = Entry(fm0, width=15)
    entry3.grid(row=0, column=6)

    button = Button(fm0, text="查询", width=7, command=execute, fg="green").grid(row=0, column=7, padx=30)
    button4 = Button(fm0, text="定位刷票", width=10, command=shua, bg="skyblue").grid(row=1, column=7, padx=30)
    button5 = Button(fm0, text="自动查票", command=jiankong, width=10, bg="skyblue").grid(row=1, column=6, padx=30)

    def gettime():
        var.set(time.strftime("%Y-%m-%d   %A   %H: %M: %S"))
        fm0.after(1000, gettime)

    var = StringVar()
    label4 = Label(fm0, text="当前时间", font=("微软雅黑", 10))
    label4.grid(row=1, column=1)
    label5 = Label(fm0, textvariable=var, fg="blue", bg="white", font=("微软雅黑", 10), padx=8)
    label5.grid(row=1, column=2, columnspan=3, padx=4)
    fm0.grid(row=0)

    fm1 = Frame(root)
    l1 = Label(fm1, text="车次       出发站名      到达站名      出发时间       到达时间        历时      一等座      二等座"
                         "      硬卧      软卧     硬座   "
                         "   软座      无座", fg="red", font=("微软雅黑", 10))
    l1.grid(pady=10, sticky=W + S)
    fm1.grid(row=1, padx=44, sticky=W + S)

    fm2 = Frame(root)
    s1 = Scrollbar(fm2)
    s1.grid(row=0, column=1, sticky=N + S)
    text1 = Text(fm2, width=114, padx=20, yscrollcommand=s1.set)
    text1.grid(row=0, column=0)
    s1.config(command=text1.yview)
    fm2.grid(row=2, padx=10)

    fm3 = Frame(root)
    label6 = Label(fm3, text="车次", font=("微软雅黑", 10))
    label6.grid(row=0, column=0)
    entry4 = Entry(fm3, width=15)
    entry4.grid(row=0, column=1, padx=15)

    label7 = Label(fm3, text="座位类型", font=("微软雅黑", 10))
    label7.grid(row=0, column=2)
    entry5 = Entry(fm3, width=15)
    entry5.grid(row=0, column=3, padx=15)

    label8 = Label(fm3, text="价格", font=("微软雅黑", 10))
    label8.grid(row=0, column=4)
    text2 = Entry(fm3, width=15, fg="blue")
    text2.grid(row=0, column=5, padx=15)

    button1 = Button(fm3, text="票价查询", width=10, fg="green", command=piaojia).grid(row=0, column=6, padx=10)
    button2 = Button(fm3, text="开始订票", width=10, bg="skyblue",command=dingpiao).grid(row=0, column=7, padx=10)
    button3 = Button(fm3, text="取消订单", width=10, fg="red", bg="skyblue",command=cancelcheck).grid(row=0, column=8, padx=10)
    fm3.grid(row=3, padx=10, pady=10)

    fm4 = Frame(root)
    s2 = Scrollbar(fm4)
    s2.grid(row=0, column=1, sticky=N + S)
    text3 = Text(fm4, width=114, height=10, padx=10,pady=5, yscrollcommand=s2.set)
    text3.grid(row=0, column=0)
    s2.config(command=text3.yview)
    fm4.grid(row=4, padx=10)

    gettime()
    root.mainloop()

def startmain():
    global answer,label,label1,label2,entry1,entry2,button
    answer = ""
    root2 = Tk()
    title=root2.title("12306用户验证")
    root2.geometry("300x360+500+200")
    label1=Label(root2,text="用户名:")
    label1.grid(row=0,column=2,pady=5)
    entry1 = Entry(root2, width=20)
    entry1.grid(row=0, column=3)
    label2=Label(root2,text="密码:")
    label2.grid(row=1,column=2)
    entry2 = Entry(root2, width=20,show="*")
    entry2.grid(row=1, column=3)
    label = Label(root2, text="")
    label.grid(row=5, column=0,columnspan=5)
    button = Button(root2, text="")
    button.grid(row=4, column=1, columnspan=5)
    def main():
        global image
        global im
        global button
        label.grid_remove()
        button.grid_remove()
        cv = Canvas(root2, bg='white', height=190, width=293)
        yzmurl = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&"
        response = session.get(url=yzmurl, headers=headers)
        with open("img.jpg", 'wb') as f:
            f.write(response.content)
        image = Image.open('img.jpg')
        im = ImageTk.PhotoImage(image)
        cv.create_image(2, 2, anchor='nw', image=im)
        cv.grid(row=2,column=1,columnspan=5,sticky='ns',pady=5,padx=2)

        def _paint(event):
            # event.x 鼠标左键的横坐标
            # event.y 鼠标左键的纵坐标
            cv.create_oval(event.x - 15, event.y - 15, event.x + 15, event.y + 15, fill="red")
            cv.create_oval(event.x-7,event.y-7,event.x-4,event.y-4,fill="black")
            cv.create_oval(event.x+7, event.y - 7, event.x+4, event.y - 4, fill="black")
            cv.create_arc(event.x - 7.5, event.y - 7.5, event.x + 7.5, event.y + 7.5,start=0,extent=-180,fill="yellow")
            global answer
            answer=answer+str(event.x)+","+str(event.y-30)+","

        def yz():
            global answer
            answer=answer[:-1]
            yzdata = {
                'answer': answer,
                'login_site': 'E',
                'rand': 'sjrand',
            }
            yzurl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
            res = session.post(url=yzurl, headers=headers, data=yzdata, verify=False)
            dic = res.content.decode('utf-8')
            dic = eval(dic)
            resultCode = dic["result_code"]
            global label
            global button
            if resultCode == "4":
                answer=""
                cv.bind("<Button-1>",NONE)
                loginurl = "https://kyfw.12306.cn/passport/web/login"
                logindata = {'username': entry1.get(),
                             'password': entry2.get(),
                             'appid': 'otn'}
                res1 = session.post(url=loginurl, headers=headers, data=logindata, verify=False)
                dic1 = res1.content.decode('utf-8')
                dic1 = eval(dic1)
                if dic1['result_message'] == "登录成功":
                    root2.destroy()
                    chaxun()
                else:
                    label.grid_remove()
                    label = Label(root2, text=dic1['result_message'], fg="red",wraplength = 280,justify = 'left')
                    label.grid(row=3, column=1, columnspan=5)
                    if "密码输入错误" in dic1['result_message']:
                        entry2.delete(0, END)
                    else:
                        entry1.delete(0, END)
                        entry2.delete(0, END)
                    button.grid_remove()
                    button = Button(root2, text="重试", width=10, bg="skyblue", command=main)
                    button.grid(row=4, column=1, columnspan=5)
            else:
                answer=""
                label = Label(root2, text=dic['result_message'], fg="red")
                label.grid(row=3, column=1,columnspan=5)
                button.grid_remove()
                button = Button(root2, text="重试", width=10,bg="skyblue",command=main)
                button.grid(row=4, column=1,columnspan=5)

        button = Button(root2, text="登录", width=20, bg="skyblue", command=yz)
        button.grid(row=4, column=1, columnspan=5)
        cv.bind("<Button-1>", _paint)
    main()
    fm=Frame(root2)
    image1=Image.open("刷新.png")
    img1 = ImageTk.PhotoImage(image1)
    button1 = Button(fm, text="刷新", image=img1, bg="green", command=main)
    button1.grid(row=0, column=4, sticky="ne")
    label3 = Label(fm, text="刷新", font=("微软雅黑", 12))
    label3.grid(row=0, column=5, sticky="ne")
    fm.grid(row=1,column=5)
    root2.iconbitmap('火车.ico')
    root2.mainloop()
startmain()