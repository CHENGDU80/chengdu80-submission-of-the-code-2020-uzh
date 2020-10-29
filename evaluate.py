# this script is to evaluate the performance of index/investment strategy
import numpy as np

# use 250 as the year interval
year_period = 251
safe_aror = 0.02  # average yearly return of US treasury bond from 2012 to 2016

def get_ARoR(price_list):
    """ Get Annualized Return of Rate"""
    ror_list = []
    for i in range(len(price_list)-year_period):
        ror_list.append((price_list[i+year_period]-price_list[i])/price_list[i])
    return ror_list


def get_avg_ARoR_per_year(price_list):
    """ compute the average ARoR per year (2012-2016)"""
    aror_list = get_ARoR(price_list)
    num_year = int(len(aror_list)/year_period)
    avg_aror = []
    for i in range(num_year):
        avg_aror.append(np.mean(aror_list[i*year_period:(i+1)*year_period]))
    return avg_aror


def get_variance(price_list):
    """Get Variance of RoR"""
    ARoRList = get_ARoR(price_list)
    std = np.std(ARoRList)
    return std


def get_sharpe_ratio(price_list):
    """Get the Sharpe ratio"""
    aror_list = get_ARoR(price_list)
    avg_aror = np.mean(aror_list)
    std_aror = np.std(aror_list)
    sharpe_ratio = (avg_aror-safe_aror)/std_aror
    return sharpe_ratio


def get_max_Drawdown(price_list):
    """Get Maximum drawdown of specific strategy"""
    max_drawdown = 0
    if price_list:
        base_price = price_list[0]
        for i in range(1,len(price_list)):
            cur_price = price_list[i]
            ratio = (cur_price-base_price)/base_price
            max_drawdown = min(max_drawdown,ratio)

            if cur_price > base_price:
                base_price = cur_price
    return max_drawdown


def get_alpha():
    pass


def get_beta():
    pass


