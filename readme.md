# ABACI
This is the repository of `SuisCorn`'s project for Chengdu80. Our work is `ABACI` (e ba qi), which aims to offer
the clients A Better Capital. We try to offers robotic advisory to serve investors to make a better interpretable investment.

## Introduction

#### Screening based on ESG score
We believe companies with better performance in ESG score could show more promising return in the stocks.
So we choose the top 50 companies in S&P 500 in terms of ESG score as the investment company pool.

#### Weighting based on smart-beta factors
We choose three smart-beta factors:  `RoE`(Return on Equity), `PE`(Price-to-Earning Ratio),
`Proyoy`(Net Profit year over year) to calculate the weight. We first detect the abnormality for the features
and fill in the missing ones with the average values. Next, we map the features to \[0,1\]. Finally,
we can choose to calculate the weight with softmax function or with simple linear weighting.

#### ZigZag to determine better action time
Instead of buy and hold strategy, we can be more active in investing by selling and buying for multiple
times. ZigZag function can detect the up and down trend and can provide insights for the action.

#### Compare with S&P 500.
We implement the first two steps and choose buy and hold strategy. We then compare the performance of our
strategy with buy and hold S&P in terms of `Return`, `Votality`, `Max Drawdown` and `Sharpe ratio`.


## Install
run `pip install -r requirements.txt` to install the required packages.

#### Get Backtest result
run `python -m get_backtest.py --factors $factor1 $factor2 --stra $stra` to get the related `.npy` file in the `\result` directory.
$factor should be chosen from (roe, mv, pe, proyoy), $stra from (simple, softmax).

#### Get News mapping
run `python news4company.py` to get the related the recognized entities from the news. Need to change
the file path in the `news4company.py`.

## Notice
Due to limited time, we have some ideas that are not achieved so far. We believe
they can work and that would be our work focus in the future.

#### ESG scores and financial news
Theoretically, we should compute the ESG score from scratch based on
the financial news. That is, 1) tokenize and parse the news. 2) detect
entity and relevant ESG events. 3) evaluate the effect level of those events on entities. 4) calculate the ESG score.

However, considering the limited time, we decide to take
advantage of the ESG scores given by other institutions, which might be
more persuasive and accurate than ours since they are more professional.

For the financial news, we manage to detect the main entities in each news.

#### ZigZag
In our plan, zigzag should help us in determining the action time point.
However, the experiment result turns out to be bad so we do not integrate this
in the final result.






