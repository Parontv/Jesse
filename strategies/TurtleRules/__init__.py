from jesse.strategies import Strategy
from jesse.indicators import donchian, atr

class TurtleRules(Strategy):
    def __init__(self):
        super().__init__(); self.current_pyramiding_levels=0; self.last_opened_price=0; self.last_was_profitable=False
    def before(self):
        self.vars['unit_risk_percent']=1; self.vars['entry_dc_period']=20; self.vars['exit_dc_period']=10; self.vars['atr_period']=20; self.vars['atr_multiplier']=2; self.vars['maximum_pyramiding_levels']=4; self.vars['pyramiding_threshold']=0.5; self.vars['system_type']='S1'
    @property
    def entry_donchian(self): return donchian(self.candles,self.vars['entry_dc_period'])
    @property
    def exit_donchian(self): return donchian(self.candles,self.vars['exit_dc_period'])
    @property
    def atr(self): return atr(self.candles,self.vars['atr_period'])
    def unit_qty(self,unit_risk_percent,dollars_per_point=1): return ((unit_risk_percent/100)*self.balance)/(self.atr*dollars_per_point)
    def entry_signal(self):
        if self.high>=self.entry_donchian[0]: return 'entry_long'
        if self.low<=self.entry_donchian[2]: return 'entry_short'
    def exit_signal(self):
        if self.high>=self.exit_donchian[0]: return 'exit_short'
        if self.low<=self.exit_donchian[2]: return 'exit_long'
    def should_long(self): return self.entry_signal()=='entry_long'
    def should_short(self): return self.entry_signal()=='entry_short'
    def should_cancel_entry(self): return False
    def go_long(self):
        qty=self.unit_qty(self.vars['unit_risk_percent']); self.buy=qty,self.price; self.stop_loss=qty,self.price-self.vars['atr_multiplier']*self.atr; self.current_pyramiding_levels+=1; self.last_opened_price=self.price
    def go_short(self):
        qty=self.unit_qty(self.vars['unit_risk_percent']); self.sell=qty,self.price; self.stop_loss=qty,self.price+self.vars['atr_multiplier']*self.atr; self.current_pyramiding_levels+=1; self.last_opened_price=self.price
    def update_position(self):
        if self.current_pyramiding_levels<self.vars['maximum_pyramiding_levels']:
            if self.is_long and self.price>self.last_opened_price+self.vars['pyramiding_threshold']*self.atr: self.buy=self.unit_qty(self.vars['unit_risk_percent']),self.price
            if self.is_short and self.price<self.last_opened_price-self.vars['pyramiding_threshold']*self.atr: self.sell=self.unit_qty(self.vars['unit_risk_percent']),self.price
        if (self.is_long and (self.entry_signal()=='entry_short' or self.exit_signal()=='exit_long')) or (self.is_short and (self.entry_signal()=='entry_long' or self.exit_signal()=='exit_short')): self.liquidate(); self.current_pyramiding_levels=0
    def on_increased_position(self,order):
        if self.is_long: self.stop_loss=abs(self.position.qty),self.price-self.vars['atr_multiplier']*self.atr
        if self.is_short: self.stop_loss=abs(self.position.qty),self.price+self.vars['atr_multiplier']*self.atr
        self.current_pyramiding_levels+=1; self.last_opened_price=self.price
    def on_stop_loss(self,order): self.current_pyramiding_levels=0
    def on_take_profit(self,order): self.last_was_profitable=True; self.current_pyramiding_levels=0
    def filters(self): return [self.S1_filter]
    def S1_filter(self):
        if self.vars['system_type']=='S1' and self.last_was_profitable: self.last_was_profitable=False; return False
        return True
