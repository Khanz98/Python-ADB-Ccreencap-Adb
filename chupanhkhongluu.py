import os,time
try:
 import threading,subprocess,base64,cv2,random,requests
 import numpy as np
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
import threading,subprocess,base64,cv2,random,requests
import numpy as np
from datetime import datetime

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self):
        #os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
    def DumpXML(self):
        name = self.handle
        if ":" in self.handle:
            name = self.handle.replace(":", "").replace(".", "")
        #print(name)
        os.system(f"adb -s {self.handle} shell uiautomator dump && adb -s {self.handle} pull /sdcard/window_dump.xml {name}.xml")
        return name+".xml"
    def find(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        #image = cv2.rectangle(img2, retVal[0],(retVal[0][0]+img.shape[0],retVal[0][1]+img.shape[1]), (0,250,0), 2)
        #cv2.imshow("test",image)
        #cv2.waitKey(0)
        #cv2.destroyWindow("test")
        return retVal
def get_code_hotmail(mail,pwd):
        code = requests.get(f'https://tools.dongvanfb.com/api/get_code?mail={mail}&pass={pwd}&type=instagram').json()["data"]
        return code
def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
GetDevices()
thread_count = len(GetDevices())
tk = open("tk.txt").readlines()

class starts(threading.Thread):
    def __init__(self, nameLD,file, i):
        super().__init__()
        self.nameLD = nameLD
        self.file = file
        self.device = i
    def run(self):
        email = self.file.split("|")[0]
        pwd = self.file.split("|")[1]
        #i = self.index
        device = self.device
        d = Auto(device)
        poin  = d.find('1.png')
        if poin > [(0, 0)] :
                        d.click(poin[0][0],poin[0][1])
                        print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
                        


    

def main(m):
        device = GetDevices()[m]
        for i in range(m, len(tk), thread_count):
                mail = tk[i].strip()
                run = starts(device,mail, device,)
                run.run()

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()