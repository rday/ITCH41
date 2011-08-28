from ITCHController import ITCHController
import ITCHMessages
from multiprocessing import Process, Queue


'''
This is a pretty weak example, but I figured it would be very
useful real world. 

I see a lot of requests for the entire list of stock symbols.
Every symbol will generate a Directory Message before the market
opens for the day. This example will grab each of those tickers
and write them to a file, giving you the complete list.

Ryan Day
ryanday2@gmail.com
'''


tickerfile = file("tickerlist","w")

def handleEvents(msg):
    ''' Handle system event messages '''
    if msg.code == 'O':
        print "Start of messages!"
    elif msg.code == 'Q':
        print "Market open, dictionary messages done!"
        tickerfile.close()

def handleDict(msg):
    tickerfile.write(msg.ticker.rstrip() + "\n")

'''
Now we can instantiate our ITCH Controller, and
register our handlers
'''
itch = ITCHController()
itch.AddHandler(ITCHMessages.StockDirectoryMessage, handleDict)
itch.AddHandler(ITCHMessages.SystemEventMessage, handleEvents)
p = Process(target=itch.run)
p.start()

'''
Our controller is now waiting for messages. So we can read
a data file (ftp://emi.nasdaq.com/ITCH/) and start processing
messages.
'''
cachesize = 16384000*4
data = file("partial", "rb")
haveData = True
ptr = buflen = 0
dataBuffer = data.read(cachesize)
buflen = len(dataBuffer)
while haveData is True:
    byte = dataBuffer[ptr:ptr+1]
    ptr = ptr + 1
    if ptr == buflen:
        ''' If we are out of buffer '''
        ptr = 0
        dataBuffer = data.read(cachesize)
        buflen = len(dataBuffer)
    if byte == b'\x00':
        length = ord(dataBuffer[ptr:ptr+1])
        ptr = ptr + 1
        if (ptr+length) > buflen:
            ''' If we don't have the entire message in our buffer '''
            temp = dataBuffer[ptr:buflen]
            dataBuffer = temp + data.read(cachesize)
            buflen = len(dataBuffer)
            ptr = 0
        message = dataBuffer[ptr:ptr+length]
        ptr = ptr + length
        itch.messageQueue.put(message)
        if ptr == buflen:
            ''' Finally, check to see if we hit the end of the buffer '''
            ptr = 0
            dataBuffer = data.read(cachesize)
            buflen = len(dataBuffer)
    else:
        print "Byte was %d" % ord(byte)

