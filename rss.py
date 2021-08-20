import feedparser
import serial
import time

usleep = lambda x: time.sleep(x/1000.0)

ser = serial.Serial('COM4')  # open serial port
print(ser.is_open)

for adr in [ 0x01, 0x02, 0x03, 0x04 ]:
    time.sleep(1)
    print(adr)
    packet = bytearray()
    packet.append(adr)

    ser.write(packet)
    msg = b"__________\n"
    ser.write(serial.to_bytes(msg))
    
time.sleep(1)

def printDate(date):
    if ser.is_open:
        packet = bytearray()
        packet.append(0x01)
        ser.write(packet)
        msg = (date+"\n").encode()
        ser.write(serial.to_bytes(msg))
        print(msg)

def printName():
    if ser.is_open:
        packet = bytearray()
        packet.append(0x01)
        ser.write(packet)
        msg = ("    The NEWS"+"\n").encode()
        ser.write(serial.to_bytes(msg))
        


def printNews(news):
    news = "______________"  + news + "______________"
    for i in range(len(news)-14):
        if ser.is_open:
            packet = bytearray()
            packet.append(0x03)
            ser.write(packet)
            msg = (news[i:i+13]+"\n").encode()
            ser.write(serial.to_bytes(msg))
            print(msg)
            packet = bytearray()
            packet.append(0x04)
            ser.write(packet)
            msg = b"                             \n"
            usleep(200)
    

def displayCovid():
    NewsFeed = feedparser.parse("https://www.thenews.com.pk/rss/1/12")
    
    for feed in NewsFeed.entries:
        if feed['title'].find("Pakistan") > 0:
            if feed['title'].find("COVID") > 0:
                printNews (feed['title'])
                time.sleep(1)
                
def displayNews():
    NewsFeed = feedparser.parse("https://www.thenews.com.pk/rss/1/1")    
    i = 0
    for feed in NewsFeed.entries:
        printNews (feed['title'])
        i = i+1
        if i > 5:
            break
       
while 0==0:
    if not ser.is_open:
        ser.open()
        time.sleep(1)
    printName()
    print("working")
    displayNews()
    time.sleep(2)
    displayCovid()
    time.sleep(2)

ser.close()
