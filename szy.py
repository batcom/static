#!/bin/python
# coding=utf-8

import httpx
import asyncio
import schedule
import time
import sys
import datetime

headers = {
    'host': 'vip1.witontek.com',
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://vip1.witontek.com',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045317 Mobile Safari/537.36 MMWEBID/6538 MicroMessenger/7.0.17.1720(0x27001137) Process/tools WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
    'sec-fetch-mode': 'cors',
    'content-type': 'application/json;charset=UTF-8',
    'x-requested-with': 'com.tencent.mm',
    'sec-fetch-site': 'same-origin',
    'referer': 'https://vip1.witontek.com/ehospital3web/web/subscription-search-result-subscription-and-registration',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'connection': 'close',
}


def get_days_before_today(n=0):
    '''''
    date format = "YYYY-MM-DD HH:MM:SS"
    '''
    now = datetime.datetime.now()
    '''if(n < 0):
        return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    else:'''
    n_days_before = now - datetime.timedelta(days=n)
    return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day)


requestToken = "85efbb5efb544186868d0b0e952eeb78"
doctor_id = "eb3818b4e0b14f52924dfb5000532a43"
department_id = "e63b0bea20db4fd4b404857332d212c4"
'''
5ee6607f335749d582cb6907919789b8 : 张浪手机
f54a9990d46b4236b220966ad52ca976 : 徐恒手机

梅国强:
doctor_id: 9feaeadd408c40f896a5bd70dc7f3d37
department_id: 4fd8d55014564972a134ad4bb468732e

'''
# patient_id = "5ee6607f335749d582cb6907919789b8"
hospital_area_id = "c4e1fb9eab54497192280960e5f5ab2d"


async def subscription(schedule_id, patient_id):
    # client = httpx.Client()
    client = httpx.AsyncClient()
    data = {
        "requestToken": requestToken, "requestData": {"hospital_id": "hbszyyadmin", "doctor_id": doctor_id, "patient_id": patient_id, "his_no": "42900619870901935X", "registration_type": "clinic_specialist", "resource_id": "", "schedule_id": schedule_id, "visit_time": "", "hospital_area_id": hospital_area_id}, "pageSize": "0", "pageNumber": "0"

    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://vip1.witontek.com/eHospital2/subscription/addSubscription?v=0.6251178489752278', headers=headers, json=data, timeout=10.0
            )
            print(response.json())
    except:
        pass

async def main():
    curdate = time.strftime("%Y-%m-%d", time.localtime())
    scandate = get_days_before_today(-8).strftime("%Y-%m-%d")
    client = httpx.Client()

    # params = {'v', '0.18932269629832654'}
    data = {"requestToken": requestToken,
            "requestData": {"hospital_id": "hbszyyadmin", "department_id": department_id, "doctor_id": doctor_id, "clinic_date": scandate, "type": "3", "hospital_area_id": hospital_area_id}, "pageSize": "999", "pageNumber": "1"}
    try:
        response = client.post(
            'https://vip1.witontek.com/eHospital2/schedule/qrySchedule?v=0.18932269629832654', headers=headers, json=data, timeout=10.0)
    except:
        return
        pass
    # print(response.json())
    scheduleData = response.json()['responseData']
    doctorList = scheduleData['doctorList']
    taskList = []
    # print(len(doctorList), doctorList)
    if(len(doctorList) > 0):
        doctor = doctorList[0]
        specialScheduleList = doctor['specialScheduleList']
        for schedule in specialScheduleList:
            print("%s:%s,%s %s,,剩余号:%s,scheId:%s," % (doctor['doctor_name'], schedule['clinic_week'], schedule['clinic_date'], schedule['clinic_time_quantum'],
                                                      schedule['clinic_distribution_no'], schedule['schedule_id']))

            sub = subscription(schedule['schedule_id'],
                               "f54a9990d46b4236b220966ad52ca976")
            task = asyncio.create_task(sub)
            taskList.append(task)
        await asyncio.gather(*taskList)
    else:
        print("%s 没有排班,扫描%s" % (curdate, scandate))
    # print(doctorList[1])


def runTaskList():
    major = sys.version_info.major
    minor = sys.version_info.minor
    if(major > 2):
        if(minor > 6):
            asyncio.run(main())
        else:
            asyncio.get_event_loop().run_until_complete(main())
    else:
        print("2.7系统不支持异步任务")


schedule.every(1).seconds.do(runTaskList)
while True:
    schedule.run_pending()
    time.sleep(1)
# while(True):
