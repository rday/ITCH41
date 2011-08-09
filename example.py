from ITCHController import ITCHController
import ITCHMessages
from multiprocessing import Process, Queue

'''
This is a example of how to use the ITCHController and ITCHMessages classes.

Ryan Day
ryanday2@gmail.com

'''
The next few procedures are example handlers. They will be registered
with the ITCH Controller and called whenever an appropriate message
is received
'''
def handleTime(msg):
    '''
        This would be a good place to keep time state. ITCH says that
        timestamp messages will be delivered offset from midnight. But
        each other message will have a nanosecond offset from the
        previous timestamp message.
    '''
    print "Seconds: %d" % msg.timestamp

def handleEvents(msg):
    ''' Handle system event messages '''
    if msg.code == 'O': print "Start of messages!"
    elif msg.code == 'S': print "Market open!"
    elif msg.code == 'E': print "Marker closed!"
    elif msg.code == 'C': print "End of messages!"

refNums = []

def handleOrders(msg):
    '''
        Lets keep track of order related to Apple
    '''
    if isinstance(msg, ITCHMessages.AddOrderMessage):
        if msg.ticker == b'AAPL    ':
            print "%c Order %d (%d@%d)" % (msg.indicator,msg.orderRefNum,msg.shares,msg.price)
            refNums.append(msg.orderRefNum)
    elif isinstance(msg, ITCHMessages.OrderCancelMessage):
        if msg.orderRefNum in refNums:
            print "Order %d Canceled (%d)" % (msg.orderRefNum,msg.shares)
            refNums.remove(msg.orderRefNum)
    elif isinstance(msg, ITCHMessages.OrderExecutedPriceMessage):
        if msg.orderRefNum in refNums:
            print "Order %d Executed (%d@%d)" % (msg.orderRefNum,msg.shares,msg.price)
            refNums.remove(msg.orderRefNum)


'''
Now we can instantiate our ITCH Controller, and
register our handlers
'''
itch = ITCHController()
itch.AddHandler(ITCHMessages.TimestampMessage, handleTime)
itch.AddHandler(ITCHMessages.SystemEventMessage, handleEvents)
itch.AddHandler(ITCHMessages.AddOrderMessage, handleOrders)
itch.AddHandler(ITCHMessages.OrderCancelMessage, handleOrders)
itch.AddHandler(ITCHMessages.OrderExecutedMessage, handleOrders)
p = Process(target=itch.run)
p.start()


'''
Our controller is now waiting for messages. So we can read
a data file (ftp://emi.nasdaq.com/ITCH/) and start processing
messages.
'''
cachesize = 16384000*4
data = file("DATAFILE", "rb")
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

