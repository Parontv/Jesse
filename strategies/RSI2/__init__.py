from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class RSI2(Strategy):
    def __init__(self):
        super().__init__(); self.vars['fast_sma_period']=5; self.vars['slow_sma_period']=200; self.vars['rsi_period']=2; self.vars['rsi_ob_threshold']=90; self.vars['rsi_os_threshold']=10
    @property
    def fast_sma(self): return ta.sma(self.candles,self.vars['fast_sma_period'])
    @property
    def slow_sma(self): return ta.sma(self.candles,self.vars['slow_sma_period'])
    @property
    def rsi(self): return ta.rsi(self.candles,self.vars['rsi_period'])
    def should_long(self): return self.price>self.slow_sma and self.rsi<=self.vars['rsi_os_threshold']
    def should_short(self): return self.price<self.slow_sma and self.rsi>=self.vars['rsi_ob_threshold']
    def should_cancel_entry(self): return False
    def go_long(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.buy=qty,self.price
    def go_short(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.sell=qty,self.price
    def update_position(self):
        if self.is_long and self.price>self.fast_sma: self.liquidate()
        if self.is_short and self.price<self.fast_sma: self.liquidate()
