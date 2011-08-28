import os
import sys
import struct
import ITCHMessages
from threading import Thread
from multiprocessing import Process, Queue

'''
The ITCH Controller is meant to run as a separate process to increase
speed. Again, this is most likely too slow for a production system. But
it is pretty quick for setting up tests against hostorical data.

Ryan Day
ryanday2@gmail.com
'''

class ITCHController(Process):
    def __init__(self, queueSize=2048000):
        self.handlers = {}
        self.messageQueue = Queue(queueSize)

    def ItchFactory(self, message):
        '''
            Pass this factory an entire bytearray and you will be
            given the appropriate ITCH message
        '''
        msgtype = message[0]
        if msgtype == 'T': return ITCHMessages.TimestampMessage(message)
        elif msgtype == 'S': return ITCHMessages.SystemEventMessage(message)
        elif msgtype == 'R': return ITCHMessages.StockDirectoryMessage(message)
        elif msgtype == 'H': return ITCHMessages.StockTradingActionMessage(message)
        elif msgtype == 'Y': return ITCHMessages.RegSHOMessage(message)
        elif msgtype == 'L': return ITCHMessages.MarketParticipantPositionMessage(message)
        elif msgtype == 'A': return ITCHMessages.AddOrderMessage(message)
        elif msgtype == 'F': return ITCHMessages.AddOrderMPIDMessage(message)
        elif msgtype == 'E': return ITCHMessages.OrderExecutedMessage(message)
        elif msgtype == 'C': return ITCHMessages.OrderExecutedPriceMessage(message)
        elif msgtype == 'X': return ITCHMessages.OrderCancelMessage(message)
        elif msgtype == 'D': return ITCHMessages.OrderDeleteMessage(message)
        elif msgtype == 'U': return ITCHMessages.OrderReplaceMessage(message)
        elif msgtype == 'P': return ITCHMessages.TradeMessage(message)
        elif msgtype == 'Q': return ITCHMessages.CrossTradeMessage(message)
        elif msgtype == 'B': return ITCHMessages.BrokenTradeMessage(message)
        elif msgtype == 'I': return ITCHMessages.NoiiMessage(message)
        return None

    def AddHandler(self, messageType, handler):
        '''
            Everytime a message is received, the controller searches
            for a handler for that message type. Use this method
            to add a handler to specific message types
         '''
        self.handlers[messageType] = handler

    def run(self):
        '''
            Our run method wait for a message to hit the queue. We
            grab the object for that message andf search for any
            handlers that should be run.
        '''
        while True:
            messageData = self.messageQueue.get()
            itch = self.ItchFactory(messageData)
            if type(itch) in self.handlers:
                self.handlers[type(itch)](itch)
