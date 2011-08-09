import struct

'''
This is a quick implementation of ITCH 4.1 according to
http://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTV-ITCH-V4_1.pdf

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
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.code = message[5]

class StockDirectoryMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'R'
        self.description = "Stock Directory Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.ticker = message[5:13]
        self.category = message[13]
        self.status = message[14]
        self.lotsize = struct.unpack("!I", message[15:19])[0]
        self.lotsonly = message[19]

class StockTradingActionMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'H'
        self.description = "Stock Trading Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.ticker = message[5:13]
        self.state = message[13]
        self.reserved = message[14]
        self.reason = message[15:19]

class RegSHOMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'Y'
        self.description = "Reg SHO Short Sale Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.ticker = message[5:13]
        self.action = message[13]

class MarketParticipantPositionMessage(ITCHMessage):
    def __init__(self, message):
        self.type = 'T'
        self.description = "Market Participant Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.mpid = message[5:9]
        self.ticker = message[9:17]
        self.primaryMarketMaker = message[17]
        self.mode = message[18]
        self.state = message[19]

class AddOrderMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Add Order Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.indicator = message[13]
        self.shares = struct.unpack("!I", message[14:18])[0]
        self.ticker = message[18:26]
        self.price = struct.unpack("!I", message[26:30])[0]

class AddOrderMPIDMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Add Order w/ MPID Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.indicator = message[13]
        self.shares = struct.unpack("!I", message[14:18])[0]
        self.ticker = message[18:26]
        self.price = struct.unpack("!I", message[26:30])[0]
        self.attribution = message[30:34]

class OrderExecutedMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Executed Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.shares = struct.unpack("!I", message[13:17])[0]
        self.match = struct.unpack("!Q", message[17:25])[0]

class OrderExecutedPriceMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Executed w/ Price Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.shares = struct.unpack("!I", message[13:17])[0]
        self.match = struct.unpack("!Q", message[17:25])[0]
        self.printable = message[25]
        self.price = struct.unpack("!I", message[26:30])[0]

class OrderCancelMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Cancel Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.shares = struct.unpack("!I", message[13:17])[0]

class OrderDeleteMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Delete Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.orderRefNum = struct.unpack("!Q", message[5:13])[0]

class OrderReplaceMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Order Replaced Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.origOrderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.newOrderRefNum = struct.unpack("!Q", message[13:21])[0]
        self.shares = struct.unpack("!I", message[21:25])[0]
        self.price = struct.unpack("!I", message[25:29])[0]

class TradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Trade Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.origOrderRefNum = struct.unpack("!Q", message[5:13])[0]
        self.indicator = message[13]
        self.shares = struct.unpack("!I", message[14:18])[0]
        self.ticker = message[18:26]
        self.price = struct.unpack("!I", message[26:30])[0]
        self.match = struct.unpack("!Q", message[30:38])[0]

class CrossTradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Cross Trade Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.shares = struct.unpack("!Q", message[5:13])[0]
        self.ticker = message[13:21]
        self.price = struct.unpack("!I", message[21:25])[0]
        self.match = struct.unpack("!Q", message[25:33])[0]
        self.crossType = message[33]

class BrokenTradeMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "Broken Trade Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.match = struct.unpack("!Q", message[5:13])[0]

class NoiiMessage(ITCHMessage):
    def __init__(self, message):
        self.description = "NOII Message"
        self.timestamp = struct.unpack("!I", message[1:5])[0]
        self.pairedShares = struct.unpack("!Q", message[5:13])[0]
        self.imbalance = struct.unpack("!Q", message[13:21])[0]
        self.imbalanceDirection = message[21]
        self.ticker = message[22:30]
        self.farPrice = struct.unpack("!I", message[30:34])[0]
        self.nearPrice = struct.unpack("!I", message[34:38])[0]
        self.currentRefPrice = struct.unpack("!I", message[38:42])[0]
        self.crossType = message[42]
        self.priceVariationIndicator = message[43]
