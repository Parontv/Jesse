from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class Donchian(Strategy):
    @property
    def donchian(self): return ta.donchian(self.candles[:-1])
    @property
    def ma_trend(self): return ta.sma(self.candles, period=200)
    def filter_trend(self): return self.close > self.ma_trend
    def filters(self): return [self.filter_trend]
    def should_long(self) -> bool: return self.close > self.donchian.upperband
    def should_short(self) -> bool: return False
    def should_cancel_entry(self) -> bool: return True
    def go_long(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.buy=qty,self.price
    def go_short(self): pass
    def update_position(self):
        if self.close < self.donchian.lowerband: self.liquidate()
