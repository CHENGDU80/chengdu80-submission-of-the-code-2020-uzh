import numpy as np
import pandas as pd
import datetime
from pandas_datareader import get_data_yahoo
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# load result
port_price_list_mv, sp500_price_list, all_company_list = np.load('result/mv_simple.npy', allow_pickle=True)
port_price_list_pe, sp500_price_list, all_company_list = np.load('result/pe_simple.npy', allow_pickle=True)
port_price_list_roe, sp500_price_list, all_company_list = np.load('result/roe_simple.npy', allow_pickle=True)
port_price_list_proyoy, sp500_price_list, all_company_list = np.load('result/proyoy_simple.npy', allow_pickle=True)
port_price_list_mv_roe,_,_ = np.load('result/mv_roe_simple.npy', allow_pickle=True)

# output to excel
start_date = datetime.datetime(2012, 1, 1)
end_date = datetime.datetime(2018, 1, 1)
sp_price = get_data_yahoo('^GSPC', start=start_date, end=end_date)
result_output = pd.DataFrame(index=sp_price.index)
result_output['mv_portfolio'] = port_price_list_mv
result_output['pe_portfolio'] = port_price_list_pe
result_output['roe_portfolio'] = port_price_list_roe
result_output['proyoy_portfolio'] = port_price_list_proyoy
result_output['mv_roe_portfolio'] = port_price_list_mv_roe
result_output['sp500bench'] = sp500_price_list
result_output.to_excel('result/backtest_result.xlsx')

df = pd.DataFrame(all_company_list[-1], columns=['Ticker', 'Name', 'esg score', 'weight'])
df.to_excel('company_info.xlsx')


# calculate performance
from evaluate import get_ARoR,get_variance,get_sharpe_ratio,get_max_Drawdown
port_price = port_price_list_mv
aror_mv_roe, aror_sp = get_ARoR(port_price), get_ARoR(sp500_price_list)
std_mv_roe, std_sp = get_variance(port_price), get_variance(sp500_price_list)
sr_mv_roe, sr_sp = get_sharpe_ratio(port_price), get_sharpe_ratio(sp500_price_list)
dd_mv_roe, dd_sp = get_max_Drawdown(port_price), get_max_Drawdown(sp500_price_list)

print("return-> port: {}, sp500: {}".format(np.mean(aror_mv_roe),np.mean(aror_sp)))
print("votality-> port: {}, sp500: {}".format(std_mv_roe, std_sp))
print("sharpe-> port: {}, sp500: {}".format(sr_mv_roe, sr_sp))
print("drawdown-> port: {}, sp500: {}".format(dd_mv_roe, dd_sp))


# have nice plot
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(1, month=1, day=1))
plt.plot(sp_price.index, port_price_list_pe)
plt.plot(sp_price.index, port_price_list_roe)
plt.plot(sp_price.index, port_price_list_proyoy)
plt.plot(sp_price.index, port_price_list_mv_roe)
plt.plot(sp_price.index, port_price_list_mv)
plt.plot(sp_price.index, sp500_price_list)
plt.gcf().autofmt_xdate()
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend(['pe', 'roe', 'proyoy', 'mv_roe','mv','sp500'])
plt.show()

