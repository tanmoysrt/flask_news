from flask import Flask,render_template
import feedparser
app=Flask(__name__)

RSS_FEEDS={
    'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn':'http://rss.cnn.com/rss/edition.rss',
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<publication>')
def get_feed(publication):
    feed=feedparser.parse(RSS_FEEDS[publication])
    articles=feed['entries']
    return render_template("rss.html",publication=publication.upper(),articles=articles,title=publication.upper())

if __name__=='__main__':
    app.run(debug=True)

## Sandip Mar khaoar list
## 10