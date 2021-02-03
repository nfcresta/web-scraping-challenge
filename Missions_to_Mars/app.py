from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# @TODO: setup mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# @TODO: connect to mongo db and collection
db = client.Mission_to_Mars
mars_data = db.mars_data

#drop the collection first
mars_data.drop()

# scrape route
@app.route('/scrape')
def scrape():
    import scrape_mars
    data = scrape_mars.scrape_()
    db.mars_data.update({}, data, upsert=True)

# index route
@app.route('/')
def index():
    mars_ = db.mars_data.find()
    return render_template('index.html', mars=mars_)


if __name__=='__main__':
    app.run(debug=True)
