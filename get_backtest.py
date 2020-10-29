import pandas as pd
import numpy as np
from pandas_datareader import get_data_yahoo
import datetime
from zigzag import *
import os

bad_stock = ['RDC', 'APC', 'AVP', 'BF/B', 'RTN','SCG'] # remove stocks that have little financial information

def filter_us_out(ticker):
    if type(ticker) == str:
        items = ticker.split()
        if items and (items[1] == 'US' or items[1] == 'UW'):
            return True
    return False


def get_simple_ticker(ticker, det=' '):
    if type(ticker) == str:
        items = ticker.split(det)
        if items:
            return items[0]
    return ''

def read_sp(year):
    sp500_bb = pd.read_excel('data/SP_HISTORICAL/SPX_{}.xlsx'.format(year))
    sp500_bb['Ticker'] = sp500_bb['Ticker'].apply(get_simple_ticker)
    return sp500_bb['Ticker'].values

def get_esg_data(year_id):
    esg_data = pd.read_excel('data/ESGdata/ESG{}.xlsx'.format(year_id))
    esg_data['is_us'] = esg_data['Ticker'].apply(filter_us_out)
    esg_data = esg_data[esg_data['is_us']]
    esg_data['Ticker'] = esg_data['Ticker'].apply(get_simple_ticker)
    return esg_data

def softmax(feature):
    exp_fea = np.exp(feature)
    return exp_fea/sum(exp_fea)

def simple_weight(feature):
    feature.fillna(feature.mean())
    return feature/sum(feature)


def outlier_detect(feature):
    q25 = np.nanpercentile(feature,25)
    q75 = np.nanpercentile(feature,75)
    iqr = q75-q25
    max_val = q75+1.5*iqr
    min_val = q25-1.5*iqr
    feature = feature.apply(lambda v: max(min(v,max_val),min_val))
    return feature

def standardization(feature):
    _min = min(feature)
    _max = max(feature)

    # correct extreme value
    feature = outlier_detect(feature)

    # fillin na with mean
    _mean = np.mean(feature)
    feature = feature.fillna(_mean)
    return (feature-_min)/(_max-_min)

def get_weight(feature,strategy='simple'):
    feature = standardization(feature)
    if strategy == 'softmax':
        return softmax(feature)
    if strategy == 'simple':
        return simple_weight(feature)

def remove_bad_stock(df,bad_stock):
    df = df.drop(df[df['Ticker'].isin(bad_stock)].index)
    return df

def fill_na_for_stock_price(stock_mat):
    m,n = stock_mat.shape
    for i in range(n):
        if sum(np.isnan(stock_mat[:,i])) > 0:
            _mean = np.nanmean(stock_mat[:,i])
            tmp = np.nan_to_num(stock_mat[:,i],nan=_mean)
            stock_mat[:, i] = tmp
    return stock_mat


def get_year_result(year,factor,stra='simple',ascending=True):
    start_date = datetime.datetime(year+1,1,1)
    end_date = datetime.datetime(year+2,1,1)
    stock_price = []
    company_list = []
    N = 50

    # get esg data and screen based on esg
    esg_data = get_esg_data(str(year)[2:])
    splist = read_sp(str(year))
    esg_data['is_sp'] = esg_data['Ticker'].isin(splist)
    esg_data = esg_data[esg_data['is_sp']]
    esg_data = remove_bad_stock(esg_data,bad_stock)
    esg_data = esg_data[esg_data['ESG Disc Score:CY'] != ' ']
    esg_data = esg_data.sort_values('ESG Disc Score:CY',ascending=ascending)
    esg_data.set_index('Ticker',inplace=True)
    chosen_tickers = esg_data.index[:N]
    chosen_names = esg_data['Name'][:N]
    esg_score = esg_data['ESG Disc Score:CY'][:N]

    # compute the weight
    spfi['is_sp50'] = spfi.index.isin(chosen_tickers)
    assert sum(spfi['is_sp50']) == N
    sub_spfi = spfi[spfi['is_sp50']]
    if type(factor) == str:
        feature_name = factor+str(year)
        feature = sub_spfi[feature_name]
        weight = get_weight(feature, stra)
    elif type(factor) == list:
        weight_list = None
        for ifactor in factor:
            feature_name = ifactor + str(year)
            feature = sub_spfi[feature_name]
            feature = standardization(feature)
            if weight_list is not None:
                weight_list += feature
            else:
                weight_list = feature
        if stra == 'simple':
            weight = simple_weight(weight_list)
        elif stra == 'softmax':
            weight = softmax(weight_list)
        else:
            print("Bad strategy type. Pls check. Exit")
            exit()
    else:
        print("Bad factor type. PLs check. Exit")
        exit()

    for i,stock in enumerate(feature.index):
        print(stock,chosen_names.loc[stock],esg_score.loc[stock],weight[i])
        company_list.append((stock,chosen_names.loc[stock],esg_score.loc[stock],weight[i]))
        price = get_data_yahoo(stock,start=start_date,end=end_date)
        stock_price.append(price['Close'])
    stock_df = pd.concat(stock_price,axis=1)
    stock_mat = stock_df.to_numpy()
    stock_mat = fill_na_for_stock_price(stock_mat)
    stock_mul = weight.values/stock_mat[0]
    port_price = np.matmul(stock_mat,stock_mul)
    sp500_price = get_data_yahoo('^GSPC', start=start_date, end=end_date)['Close']
    sp500_price = sp500_price / sp500_price[0]
    assert len(port_price) == len(sp500_price)
    return port_price,sp500_price,company_list

def zigzag(price_list,upthre=0.1,downthre=-0.1):
    """use zigzag function to determine whether to buy or not"""
    price_list = np.array(price_list)
    mode_list = []
    money_list = [1]
    share_list = [0]
    share,left_money=0,1
    for i in range(1,len(price_list)):
        pivots = peak_valley_pivots(price_list[:i], upthre, downthre)
        modes = pivots_to_modes(pivots)
        cur_mode = modes[-1]
        if mode_list:
            if cur_mode == 1 and mode_list[-1] == -1:
                share = money_list[-1]/price_list[i]
                left_money = 0
            elif cur_mode == -1 and share > 0:
                left_money = share*price_list[i]
                share = 0
        money = share*price_list[i]+left_money
        money_list.append(money)
        mode_list.append(cur_mode)
        share_list.append(share)
    return money_list

if __name__ == '__main__':

    # load s&p 500 finacial data
    spfi = pd.read_excel('data/sp500_final.xlsx')
    spfi['Ticker'] = spfi['Ticker'].apply(get_simple_ticker, args=('.'))
    spfi = spfi.set_index('Ticker')

    # run the result
    port_price_list = []
    sp500_price_list = []
    all_company_list = []
    year_len = []
    factor = ['mv','roe']
    stra = 'simple'
    if type(factor) == list:
        factor_name = '_'.join(factor)
    else:
        factor_name = factor

    print(">>>> Run Backtest. Weight strategy: {}, factor: {}".format(stra,factor_name))
    for year in range(2011,2017):
        print(year)
        port_price,sp500_price,company_list = get_year_result(year,factor,stra)
        year_len.append(len(port_price))
        if port_price_list and sp500_price_list:
            port_price *= port_price_list[-1]
            sp500_price *= sp500_price_list[-1]
        port_price_list.extend(port_price)
        sp500_price_list.extend(sp500_price)
        all_company_list.append(company_list)

    # save result
    file_name = factor_name+'_'+stra+'.npy'
    file_path = os.path.join('result',file_name)
    np.save(file_path,[port_price_list,sp500_price_list,all_company_list])


