from transformers import pipeline
import pandas as pd
from reviewCrawler import Scraper

X=Scraper("https://www.jumia.co.ke/mens-casual-breathable-canvas-sneakers-black-fashion-mpg230688.html")
df=pd.DataFrame(X.rev_list)

nlp_sent=pipeline(
    "sentiment-analysis"
)
nlp_sent("Before he makes any purchases, Billy likes to do his research; he's so cheap")



def get_sentiment(text):    
    resp=nlp_sent(text)
    if resp['label']=='NEGATIVE':
        score=-1*resp['score']
    else:
        score=resp['score']
    return score

df["h_sent"]=[get_sentiment(x) for x in df.Heading]
df["r_sent"]=[get_sentiment(x) for x in df.Review]

get_sentiment("Before he makes any purchases, Billy likes to do his research; he's so cheap")
import matplotlib.pyplot as plt

plt.matshow(df[["h_sent","r_sent"]].corr())
plt.show()
