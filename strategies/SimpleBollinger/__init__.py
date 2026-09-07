from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class SimpleBollinger(Strategy):
    @property
    def bb(self): return ta.bollinger_bands(self.candles,source_type='hl2')
    @property
    def ichimoku(self): return ta.ichimoku_cloud(self.candles)
    def filter_trend(self): return self.close>self.ichimoku.span_a and self.close>self.ichimoku.span_b
    def filters(self): return [self.filter_trend]
    def should_long(self): return self.close>self.bb[0]
    def should_short(self): return False
    def should_cancel_entry(self): return True
    def go_long(self):
        qty=utils.size_to_qty(self.balance,self.price,fee_rate=self.fee_rate); self.buy=qty,self.price
    def go_short(self): pass
    def update_position(self):
        if self.close<self.bb[1]: self.liquidate()
