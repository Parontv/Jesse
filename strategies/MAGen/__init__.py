import jesse.indicators as ta
from jesse import utils
from jesse.strategies import Strategy

class MAGen(Strategy):
    def should_long(self): return self.longEntry
    def should_short(self): return self.shortEntry
    def go_long(self):
        entry=self.price; stop=entry-self.atr*self.hp['stop_loss_atr_rate']; qty=utils.risk_to_qty(self.balance,3,entry,stop); take_profit=entry+self.atr*self.hp['take_profit_atr_rate']; self.buy=qty,entry; self.stop_loss=qty,stop; self.take_profit=qty,take_profit
    def go_short(self):
        entry=self.price; stop=entry+self.atr*self.hp['stop_loss_atr_rate']; qty=utils.risk_to_qty(self.balance,3,entry,stop); take_profit=entry-self.atr*self.hp['take_profit_atr_rate']; self.sell=qty,entry; self.stop_loss=qty,stop; self.take_profit=qty,take_profit
    def should_cancel_entry(self): return True
    def update_position(self):
        if (self.is_short and self.shortExit) or (self.is_long and self.longExit): self.liquidate()
    @property
    def longEntry(self): return self.trend_direction_change==1 and self.adx>self.hp['adx_entry']
    @property
    def shortEntry(self): return self.trend_direction_change==-1 and self.adx>self.hp['adx_entry']
    @property
    def longExit(self): return self.ma_fast[-1]<self.ma_slow[-1] and self.adx<self.hp['adx_exit']
    @property
    def shortExit(self): return self.ma_fast[-1]>self.ma_slow[-1] and self.adx<self.hp['adx_exit']
    @property
    def adx(self): return ta.adx(self.candles,period=self.hp['adx_period'])
    @property
    def trend_direction_change(self):
        direction=0
        if self.ma_fast[-1]<self.ma_slow[-1] and self.ma_fast[-2]>=self.ma_slow[-2]: direction=-1
        if self.ma_fast[-1]>self.ma_slow[-1] and self.ma_fast[-2]<=self.ma_slow[-2]: direction=1
        return direction
    def _source(self,n): return ['close','high','low','open','hl2','hlc3','ohlc4'][self.hp[n]]
    @property
    def ma_slow(self): return ta.ma(self.candles,matype=self.hp['ma_type_slow'],period=self.hp['ma_period_slow'],source_type=self._source('ma_source_slow'),sequential=True)
    @property
    def ma_fast(self): return ta.ma(self.candles,matype=self.hp['ma_type_fast'],period=self.hp['ma_period_fast'],source_type=self._source('ma_source_fast'),sequential=True)
    @property
    def atr(self): return ta.atr(self.candles,period=self.hp['atr_period'])
    def hyperparameters(self):
        return [{'name':'stop_loss_atr_rate','type':float,'min':1,'max':4,'default':2},{'name':'take_profit_atr_rate','type':float,'min':3,'max':20,'default':5},{'name':'atr_period','type':int,'min':5,'max':40,'default':32},{'name':'ma_period_slow','type':int,'min':3,'max':200,'default':20},{'name':'ma_source_slow','type':int,'min':0,'max':6,'default':0},{'name':'ma_period_fast','type':int,'min':3,'max':100,'default':5},{'name':'ma_source_fast','type':int,'min':0,'max':6,'default':0},{'name':'ma_type_slow','type':int,'min':0,'max':39,'default':11},{'name':'ma_type_fast','type':int,'min':0,'max':39,'default':11},{'name':'adx_period','type':int,'min':3,'max':60,'default':8},{'name':'adx_exit','type':int,'min':3,'max':40,'default':15},{'name':'adx_entry','type':int,'min':3,'max':40,'default':13}]
