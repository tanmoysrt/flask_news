from flask import Flask,render_template,request,redirect
import feedparser
import json
import urllib
app=Flask(__name__)

RSS_FEEDS={
    'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn':'http://rss.cnn.com/rss/edition.rss',
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search',methods=['POST','GET'])
def search():
    query=request.args.get('publication')
    try:
        x=query.lower()
    except AttributeError:
        x='bbc'
    if  x  in RSS_FEEDS:
        publication=x
    else:
        publication='bbc'
    feed=feedparser.parse(RSS_FEEDS[publication])
    articles=feed['entries']
    return render_template('search.html',publication=publication.upper(),articles=articles,title=publication.upper())

@app.route('/<publication>')
def get_feed(publication):
    feed=feedparser.parse(RSS_FEEDS[publication])
    articles=feed['entries']
    return render_template("rss.html",publication=publication.upper(),articles=articles,title=publication.upper())

@app.route('/weather/',methods=['GET','POST'])
def get_weather():
    query=request.args.get('query')
    if query is None:
        query='Birnagar'
    else:
        pass
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c43d2a316df28b935cd6ed2a47cb3bfb"
    x=urllib.request.urlopen(api_url.format(query))
    parsed=json.loads(x.read())
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"feels_like":parsed["main"]["feels_like"],"city":parsed["name"]
 }
    city=request.args.get('city')
    if not city:
        city='Birnagar'
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = 'USD'
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = 'INR'
    rate = get_rate(currency_from, currency_to)

    return render_template('weather.html',weather=weather,currency_from=currency_from,currency_to=currency_to,rate=rate)

def get_rate(frm,to):
    api_url='https://openexchangerates.org/api/latest.json?app_id=da54feb1d0fe4186857c79b06b22f265'
    x=urllib.request.urlopen(api_url)
    parsed = json.loads(x.read()).get('rates')
    frm_rate=parsed.get(frm.upper())
    to_rate=parsed.get(to.upper())
    return to_rate/frm_rate
if __name__=='__main__':
    app.run(debug=True)

## Sandip Mar khaoar list
## 10+10