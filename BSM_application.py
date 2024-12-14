import numpy as np
from Equity_Option_Data import EquityOption
from BSM import Equity, Option, BlackScholesMerton
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action = 'ignore')

e0 = EquityOption('COST')
exp_date, trade_date, strike_list, volatility_list, put_call, bid, ask = e0.get_option_data('2025-03-21', 'call')

all_n = np.arange(0,len(trade_date))
rate = 0.001
bsm = BlackScholesMerton(eq, op, rate)
predic = []
avg = []
errors = []
for n in all_n:
    op = Option(exp_date, trade_date[n], strike_list[n], volatility_list[n], put_call)

    spot_price = e0.get_equity_data(trade_date[n])[-2][-1]
    dividend_yield = e0.get_equity_data(trade_date[n])[-1]
    eq = Equity(spot_price, dividend_yield)

    bsm = BlackScholesMerton(eq, op, rate)
    predicted_price = bsm.bsm_pricer(eq,op,rate)
    predic.append(predicted_price)
    avg_price = (bid[n] + ask[n])/2
    avg.append(avg_price)
    err = predicted_price - avg_price
    errors.append(err)


plt.plot(errors)
plt.grid()
plt.axhline(0,c = 'black')
plt.show()

plt.plot(predic, label = 'prediced price')
plt.plot(avg, label = 'avg of bid&ask')
plt.grid()
plt.axhline(0,c = 'black')
plt.legend(loc ='best')
plt.show()