import time, subprocess, platform, ctypes, datetime, random, configparser
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

def parsePic(dayTime, weather, pixToken):
    try:
        request = requests.get(f"https://pixabay.com/api/?key={pixToken}&q={dayTime}+{weather}&image_type=photo&pretty=true")
        data = json.loads(request.text)
        hit = data["hits"][random.randint(0, len(data["hits"]))]
        global picUrl 
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





config = configparser.ConfigParser()
config.read('tokens.ini')
pixToken = config.get('tokens', 'pixabay_token')
weatherToken = config.get('tokens', 'openweather_token')
ipinfoToken = config.get('tokens', 'ipinfo_token')
picUrl = "offline"

while(True):
    try:
        gpsRes = requests.get(f"https://ipinfo.io/loc?token={ipinfoToken}")
        lat = gpsRes.text.split(',')[0]
        lon = gpsRes.text.split(',')[1][:-1]
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weatherToken}")
        weather = json.loads(response.text)["weather"][0]["main"].lower()
    except:
        weather = "clear"

    t = time.localtime()
    dayTime = getDayTime(t, response)

    if (parsePic(dayTime, weather, pixToken)):
        setPixabay()
    else:
        setLocal(dayTime, weather)

    print(f"{t.tm_hour}:{t.tm_min}, установил {weather} {dayTime} обои\n{picUrl}")

    file = open("log.txt", "a")
    file.write(f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}, установил {weather} {dayTime} обои\n{picUrl}\n") #спасибо, Лина ♥♥♥
    file.close()
    time.sleep(300)
    