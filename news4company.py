# Suiscorn --> find entity names in the financial news

from collections import Counter
import en_core_web_sm
import pandas as pd
from fuzzywuzzy import fuzz


def news4company(news_path):
    with open(news_path,'r',encoding='utf8') as f:
        txt = f.read()
    txt = txt.replace('\n', '')
    nlp = en_core_web_sm.load()
    doc = nlp(txt)

    # find the tokens that belongs to 'ORG'
    text = []
    label = []
    for X in doc.ents:
        text.append(X.text)
        label.append(X.label_)

    index_org = [i for i, x in enumerate(label) if x == 'ORG']
    text_org = [text[i] for i in index_org]

    # count the frequency
    freq = Counter(text_org).most_common()

    # choose the s&p500 companies out of the 10 most common ORGs
    spname = pd.read_csv("data/SPX_names_cleaned.csv")
    spname = spname['Names'].tolist()
    company = []
    for (org, frequency) in freq:
        for names in spname:
            match_score = fuzz.ratio(names, org)
            if (match_score > 60):
                # print(org)
                # print(names)
                # print(match_score)
                company.append((org, frequency))
    return (company)


news_path = 'chengdu80/dataset/2012_financial_news/2012-01-01/-ghost-protocol-leads-last-weekend-of-11'
print(news4company(news_path))







