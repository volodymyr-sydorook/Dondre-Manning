class MetaTradeMain:
    def __init__(self, mt5):
        self.mt5 = mt5  # class mt5

        # other params for create order
        self.symbol = None
        self.symbol_info = None
        self.lot = None
        self.point = None
        self.price = None
        self.sl = None
        self.tp = None
        self.type_action = None
        self.deviation = None
        self.request = None
        self.result = None

    async def mt_initialize(self):
        """establish connection to the MetaTrader 5 terminal"""
        if not self.mt5.initialize():
            print("initialize() failed, error code =", self.mt5.last_error())
            quit()

    async def create_symbol_and_info(self, message_lst):
        """prepare the buy request structure"""
        self.symbol = message_lst[0].split()[0]
        self.symbol_info = self.mt5.symbol_info(self.symbol)
        print(self.symbol, self.symbol_info)
        if self.symbol_info is None:
            print(self.symbol, "not found, can not call order_check()")
            self.mt5.shutdown()
            quit()

    async def check_open_symbol(self):
        """if the symbol is unavailable in MarketWatch, add it"""
        if not self.symbol_info.visible:
            print(self.symbol, "is not visible, trying to switch on")
            if not self.mt5.symbol_select(self.symbol, True):
                print("symbol_select({}}) failed, exit", self.symbol)
                self.mt5.shutdown()
                quit()

    async def create_other_params(self, message_lst, message):
        self.lot = 0.1
        self.point = self.mt5.symbol_info(self.symbol).point
        self.price = float(message_lst[0].split()[-1])
        self.sl = float(message_lst[2].split()[-1][1:])
        self.tp = float(message_lst[4].split()[2].split('(')[0])
        self.deviation = 20

        #  choice type_action buy
        if 'buy' in message and 'now' in message:
            self.type_action = self.mt5.ORDER_TYPE_BUY
        elif 'buy' in message and 'limit' in message:
            self.type_action = self.mt5.ORDER_TYPE_BUY_LIMIT

        #  choice type_action sell
        elif 'sell' in message and 'now' in message:
            self.type_action = self.mt5.ORDER_TYPE_SELL
        elif 'sell' in message and 'limit' in message:
            self.type_action = self.mt5.ORDER_TYPE_SELL_LIMIT

    async def generate_json(self):
        """generate json for sending offer"""
        self.request = {
            "action": self.mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": self.type_action,
            "price": self.price,
            "sl": self.sl,
            "tp": self.tp,
            "deviation": self.deviation,
            "magic": 234000,
            "comment": "python script open",
            "type_time": self.mt5.ORDER_TIME_GTC,
            "type_filling": self.mt5.ORDER_FILLING_RETURN,
        }

    async def send_json_trading(self):
        """send a trading request"""
        self.result = self.mt5.order_send(self.request)

    async def check_result_offer(self):
        print(f"1. order_send(): by {self.symbol} {self.lot} lots at {self.price} with deviation={self.deviation} points")

        if self.result.retcode != self.mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(self.result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = self.result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            print("shutdown() and quit")
            self.mt5.shutdown()
            quit()
