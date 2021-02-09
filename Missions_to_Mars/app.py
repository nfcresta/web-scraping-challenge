from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.Mission_to_Mars
mars_data = db.mars_data

# index route
@app.route('/')
def index():
    mars = db.mars_data.find_one()
    return render_template('index.html', mars=mars)

# drop the collection first
mars_data.drop()

# scrape route
@app.route('/scrape')
def scrape():
    data = scrape_mars.scrape_()
    db.mars_data.update({}, data, upsert=True)
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)
