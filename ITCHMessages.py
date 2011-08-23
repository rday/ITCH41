import struct

'''
This is a quick implementation of ITCH 4.1 according to
http://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTV-ITCH-V4_1.pdf

Ryan Day
ryanday2@gmail.com
'''

class ITCHMessage(object):
    sysEventCodes = {
                        'O':'Start of Messages',
                        'S':'Start of System Hours',
                        'Q':'Start of Market Hours',
                        'M':'End of Market Hours',
                        'E':'End of System Hours',
                        'C':'End of Messages',
                        'A':'EMC Halt',
                        'R':'EMC Quote Only',
                        'B':'EMV Resumption'
                    }
    exchanges = {
                        'N':'NYSE',
                        'A':'AMEX',
                        'P':'Arca',
                        'Q':'NASDAQ Global Select',
                        'G':'NASDAQ Global Market',
                        'S':'NASDAQ Capital Market'
                    }
    finStatusIndicators = {
                        'D':'Deficient',
                        'E':'Deliquent',
                        'Q':'Bankrupt',
                        'S':'Suspended',
                        'G':'Deficient and Bankrupt',
                        'H':'Deficient and Deliquent',
                        'J':'Delinquent and Bankrput',
                        'K':'Deficient, Delinquent and Bankrupt',
                        'Y':'Bad Financial Status',
                        ' ':'Compliant'
                    }
    tradingStates = {
                        'H':'All Markets Halted',
                        'V':'NASDAQ Halted',
                        'Q':'Quote Only XSRO',
                        'R':'Quote only NASDAQ',
                        'T':'Trading on NASDAQ'
                    }
    marketMakerModes = {
                        'N':'Normal',
                        'P':'Passive',
                        'S':'Syndicate',
                        'R':'Pre-syndicate',
                        'L':'Penalty'
                    }
    marketParticipantStates = {
                        'A':'Active',
                        'E':'Excused',
                        'W':'Withdrawn',
                        'S':'Suspended',
                        'D':'Deleted'
                    }

class TimestampMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'T'
        self.description = 'Timestamp Message'
        self.timestamp = struct.unpack("!I", message[1:5])[0]
                
class SystemEventMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'S'
        self.description = "System Event Message"
        (self.timestamp, self.code) = struct.unpack("!Ic", message[1:])

class StockDirectoryMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'R'
        self.description = "Stock Directory Message"
        (self.timestamp, self.ticker, self.category,
            self.status, self.lotsize, self.lotsonly) = struct.unpack("!I8sccIc", message[1:])

class StockTradingActionMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'H'
        self.description = "Stock Trading Message"
        (self.timestamp, self.ticker, self.state,
            self.reserved, self.reason)  = struct.unpack("!I8scc4s", message[1:])

class RegSHOMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'Y'
        self.description = "Reg SHO Short Sale Message"
        (self.timestamp, self.ticker, self.action) = struct.unpack("!I8sc", message[1:])

class MarketParticipantPositionMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'T'
        self.description = "Market Participant Message"
        (self.timestamp, self.mpid, self.ticker, self.primaryMarketMaker,
            self.mode, self.state) = struct.unpack("!I4s8sccc", message[1:])

class AddOrderMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Add Order Message"
        (self.timestamp, self.orderRefNum, self.indicator, self.shares,
            self.ticker, self.price) = struct.unpack("!IQcI8sI", message[1:])

class AddOrderMPIDMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Add Order w/ MPID Message"
        (self.timestamp, self.orderRefNum, self.indicator, self.shares,
            self.ticker, self.price, self.attribution)  = struct.unpack("!IQcI8sI4s", message[1:])

class OrderExecutedMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Executed Message"
        (self.timestamp, self.orderRefNum, self.shares, self.match) = struct.unpack("!IQIQ", message[1:])

class OrderExecutedPriceMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Executed w/ Price Message"
        (self.timestamp, self.orderRefNum, self.shares, self.match,
            self.printable, self.price) = struct.unpack("!IQIQcI", message[1:])

class OrderCancelMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Cancel Message"
        (self.timestamp, self.orderRefNum, self.shares) = struct.unpack("!IQI", message[1:])

class OrderDeleteMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Delete Message"
        (self.timestamp, self.orderRefNum) = struct.unpack("!IQ", message[1:])

class OrderReplaceMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Replaced Message"
        (self.timestamp, self.origOrderRefNum, self.newOrderRefNum,
            self.shares, self.price) = struct.unpack("!IQQII", message[1:])

class TradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Trade Message"
        (self.timestamp, self.origOrderRefNum, self.indicator, self.shares,
            self.ticker, self.price, self.match) = struct.unpack("!IQcI8sIQ", message[1:])

class CrossTradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Cross Trade Message"
        (self.timestamp, self.shares, self.ticker, self.price, self.match,
            self.crossType) = struct.unpack("!IQ8sIQc", message[1:])

class BrokenTradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Broken Trade Message"
        (self.timestamp, self.match) = struct.unpack("!IQ", message[1:])

class NoiiMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "NOII Message"
        (self.timestamp, self.pairedShares, self.imbalance, self.imbalanceDirection,
            self.ticker, self.farPrice, self.nearPrice, self.currentRefPrice,
            self.crossType, self.priceVariationIndicator) = struct.unpack("!IQQc8sIIIcc", message[1:])
