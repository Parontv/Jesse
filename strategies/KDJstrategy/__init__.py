from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class KDJstrategy(Strategy):
    @property
    def KDJIndicator(self): return ta.kdj(self.candles)
    @property
    def LastKDJ(self): return ta.kdj(self.candles[:-1])
    @property
    def atr(self): return ta.atr(self.candles, period=14)
    def should_long(self) -> bool: return self.KDJIndicator[2] > (self.KDJIndicator[0] and self.KDJIndicator[1])
    def should_short(self) -> bool: return False
    def should_cancel(self) -> bool: return True
    def go_long(self):
        risk_perc=5; entry=self.price; stop=entry-2*self.atr; qty=utils.risk_to_qty(self.capital,risk_perc,entry,stop); self.buy=qty,self.price; self.stop_loss=qty,stop
    def go_short(self): return False
    def update_position(self):
        if self.is_long and self.position.pnl_percentage>0 and self.LastKDJ[2]>self.KDJIndicator[2]: self.liquidate()
        elif self.is_long and self.KDJIndicator[2] < (self.KDJIndicator[0] and self.KDJIndicator[1]): self.liquidate()
