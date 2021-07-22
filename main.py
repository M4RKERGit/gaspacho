import time, subprocess, platform, ctypes, datetime, random
import json, httplib2
import requests
import math

def getDayTime(t, response):
    sunrise = math.ceil(datetime.datetime.fromtimestamp((json.loads(response.text)["sys"]["sunrise"])).hour)
    sunset = math.ceil(datetime.datetime.fromtimestamp((json.loads(response.text)["sys"]["sunset"])).hour)
    if t.tm_hour >= sunrise and time.localtime().tm_hour <= sunrise + 6: return 'morning'
    if t.tm_hour >= sunrise + 6 and time.localtime().tm_hour <= sunrise + 12: return 'day'
    if t.tm_hour >= sunrise + 12 and time.localtime().tm_hour <= sunset: return 'evening'
    return 'night'

def parsePic(dayTime, weather):
    try:
        request = requests.get(f"https://pixabay.com/api/?key=20129846-7b8836a9a63b2f2b6fa405f5f&q={dayTime}+{weather}&image_type=photo&pretty=true")
        data = json.loads(request.text)
        hit = data["hits"][random.randint(0, len(data["hits"]))]
        picUrl = hit["fullHDURL"]
        h = httplib2.Http('.cache')
        response, content = h.request(picUrl)
        out = open("/home/opezdal/Pictures/wallpapers/img.jpg", "wb")
        out.write(content)
        out.close()
        return 1
    except:
        return 0

def setLocal(dayTime, weather):
    runningSys = platform.system()
    path = f"/home/opezdal/Pictures/wallpapers/{weather}"
    if runningSys == "Linux":
        process = subprocess.Popen(["feh", "--bg-fill", f"{path}/{dayTime}.jpg"])
        process.wait()
        if process.returncode != 0: 
            print("Краш процесса")
            return
    if runningSys == "win32": ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{dayTime}.jpg", 3)

def setPixabay():
    runningSys = platform.system()
    if runningSys == "Linux":
        process = subprocess.Popen(["feh", "--bg-fill", "/home/opezdal/Pictures/wallpapers/img.jpg"])
        process.wait()
        if process.returncode != 0: 
            print("Краш процесса")
            return
    if runningSys == "win32": ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{dayTime}.jpg", 3)

while(True):
    try:
        gpsRes = requests.get("https://ipinfo.io/loc")
        lat = gpsRes.text.split(',')[0]
        lon = gpsRes.text.split(',')[1][:-1]
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=06d0d10ec4b1f25282e0ea1f8788bcb2")
        weather = json.loads(response.text)["weather"][0]["main"].lower()
    except:
        weather = "clear"

    t = time.localtime()
    dayTime = getDayTime(t, response)

    if (parsePic(dayTime, weather)):
        setPixabay()
    else:
        setLocal(dayTime, weather)

    print(f"{t.tm_hour}:{t.tm_min}, установил {weather} {dayTime} обои")

    file = open("log.txt", "a")
    file.write(f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}, установил {weather} {dayTime} обои\n")
    file.close()
    time.sleep(300)