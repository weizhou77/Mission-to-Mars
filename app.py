


from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
app=Flask(__name__)

#1st says that we will use Flask to render a template, redirecting to another url and creating a URL
#2nd we will use PyMongo to interact with our Mongo database
#3rd use the scraping.py code, we will convert from Jupyter to python




# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# 1st line above tells python that our app will connect to Mongo using a URI, a uniform resource identifier similar to URL
# then we will be using to connect our app to Mongo. this URI says that the app can reach Mongo through our  localhost server
# using port 27017 using a database named mars_app




# first we define the rout for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars) # put the index.html in a file call template
# '@app.route("/")' tells flask what to display when we are looking at the home page.
# within the def index(): function, 
# 'mars = mongo.db.mars.find_one()' uses PyMongo to find the mars collection in our database which we will create when we convert our jupyter scraping code to python script
# 'return render_template("index.html", mars=mars)' tells flask to return an HRML template using an index.html file. we will create this file after we build the flask routes
# 'mars=mars' tells python to use the mars collection in MongoDB





# the next function will set up our scraping route. this route will be the button of the web application, the one will scrape updated data when we tell it to from the homepage of our web app
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
# '@app.route("/scrape")' defines the route that flask will be using. '/scrape'
# the next lines allow us to access the database, scrape new data using our scraping.py, update database and return a message when successful
# first we define def scrape()
# then we assign a new variable that points our Mongo databse mars = mongo.db.mars
# then we create a new variable to hold the newly scraped data mars_data = scraping.scrape_all().
# in mars_data line, we reference the scrape_all function in the scraping.py
# now we gathered new data, we need to update the database using .update_one(). upsert=True means ask Mongo to create a new document if one doesnt exist and new data will always be saved
# last line, this will navigate our page back to / where we can see the updated content




if __name__ == "__main__":
   app.run()






