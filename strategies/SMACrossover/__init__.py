from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class SMACrossover(Strategy):
    @property
    def slow_sma(self): return ta.sma(self.candles,200)
    @property
    def fast_sma(self): return ta.sma(self.candles,50)
    def should_long(self): return self.fast_sma>self.slow_sma
    def should_short(self): return self.fast_sma<self.slow_sma
    def should_cancel_entry(self): return False
    def go_long(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.buy=qty,self.price
    def go_short(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.sell=qty,self.price
    def update_position(self):
        if self.is_long and self.fast_sma<self.slow_sma: self.liquidate()
        if self.is_short and self.fast_sma>self.slow_sma: self.liquidate()
