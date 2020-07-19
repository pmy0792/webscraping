from scraper import *
from save import *
rstrt=extract_rstrts()
print(rstrt)
excel_sheet(rstrt)


from flask import Flask, render_template, request, redirect, send_file
from scraper import extract_locations
extract_locations()
from scraper import location_list, final_list

from analyze import *
show_analyze_result(final_list)



app=Flask("webscrapper3")

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/local_restaurant')
def local_restaurants():
  return render_template("local_restaurant.html",location_list=location_list)


@app.route('/show_local_restaurant')
def show_restaurants():
  location=request.values["location"]
  restaurants_list=[]
  for li in final_list:
    if location==list(li.keys())[0]:
      restaurants_list=list(li.values())[0]
  print("#############", len(restaurants_list))
  return render_template("show_local_restaurant.html",location=location, restaurants_list=restaurants_list,number=len(restaurants_list))


@app.route('/analyze')
def analyze():
  return render_template("analyze.html",location_list=location_list)

app.run(host="0.0.0.0")