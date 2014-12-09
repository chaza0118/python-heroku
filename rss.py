import feedparser
from future import Future
#"http://phys.org/rss-feed/"

def
rss_feed = "http://feeds.bbci.co.uk/news/rss.xml"
rss_list = ["http://feeds.bbci.co.uk/news/rss.xml","http://phys.org/rss-feed/"]
#feed = feedparser.parse(rss_feed)
future_calls = [Future(feedparser.parse,rss_url) for rss_url in rss_list]
feeds = [future_obj() for future_obj in future_calls]
for feed in feeds:
    for entry in feed.entries:
        print entry.title

#for entry in feed.entries:
 #   print entry.title
    


