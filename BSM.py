import numpy as np
from Equity_Option_Data import EquityOption
from dataclasses import dataclass
import scipy.stats as stat
from math import log, sqrt, e

@dataclass
class Equity:
    spot_price: float
    dividend_yield: float

@dataclass
class Option:
    exp_date: float
    trade_date: float
    strike_price: float
    volatility: float
    put_call: float

class BlackScholesMerton():
    def __init__(self, equ, opt, rate):
        
        self.s0 = equ.spot_price
        self.div = equ.dividend_yield
        self.exp_date = opt.exp_date
        self.trade_date = opt.trade_date.to_pydatetime().replace(tzinfo = None)
        self.k = opt.strike_price
        self.v = opt.volatility
        self.put_call = opt.put_call
        self.r = rate
        self.t = (self.exp_date - self.trade_date).total_seconds()/(24*60*60*365)
        
        
    def bsm_pricer(self, eq, op, rate):
        self.put_call = op.put_call

        self.d1 = (log(self.s0/self.k) + (self.r - self.div + 0.5*self.v**2)*self.t)/(self.v*sqrt(self.t))
        self.d2 = self.d1 - self.v*sqrt(self.t)
        
        if self.put_call == 'call':
            self.option_price = self.s0*e**-(self.div*self.t)*stat.norm.cdf(self.d1) - self.k*e**-(self.r*self.t)*stat.norm.cdf(self.d2)
        elif self.put_call == 'put':
            self.option_price = self.k*e**(-self.r*self.t)*stat.norm.cdf(-self.d2) - self.s0*e**(-self.div*self.t)*stat.norm.cdf(-self.d1)

        return self.option_price