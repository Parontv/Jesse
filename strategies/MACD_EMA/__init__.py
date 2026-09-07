from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class MACD_EMA(Strategy):
    @property
    def macd(self): return ta.macd(self.candles,self.hp['fastperiod'],self.hp['slowperiod'],self.hp['signalperiod'])
    @property
    def ema(self): return ta.ema(self.candles,self.hp['ema'])
    def should_long(self): return self.close > self.ema and self.macd[0] > self.macd[1]
    def should_short(self): return False
    def should_cancel_entry(self) -> bool: return True
    def go_long(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.buy=qty,self.price
    def go_short(self): pass
    def update_position(self):
        if self.macd[0] < self.macd[1] and self.close < self.ema: self.liquidate()
    def hyperparameters(self):
        return [{'name':'ema','type':int,'min':50,'max':200,'default':100},{'name':'fastperiod','type':int,'min':10,'max':18,'default':12},{'name':'slowperiod','type':int,'min':19,'max':36,'default':26},{'name':'signalperiod','type':int,'min':3,'max':9,'default':9}]
