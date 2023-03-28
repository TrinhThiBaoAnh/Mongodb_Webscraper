from flask import Flask, render_template
from collections import Counter
import datetime

app = Flask(__name__)
import json
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import pickle
def preprocess(text):
    text = text.lower().strip()
# counts word frequency using
# Counter from collections
def count_words_fast(text):	
	text = text.lower()
	skips = [".", ", ", ":", ";", "'", '"']
	for ch in skips:
		text = text.replace(ch, "")
	word_counts = Counter(text.split(" "))
	return word_counts
# word_counts = count_words_fast(text)
def word_stats(word_counts):	
	num_unique = len(word_counts)
	counts = word_counts.values()
	return (num_unique, counts)

def processing_author(author_lst, author_file, author_stat_file, save_fig_path):
    set_author = set(author_lst)
    print(set_author)
    with open(f'{author_file}.txt', 'w') as f:
        for item in set_author:
            f.write("%s\n" % item)

    stat_author = Counter(author_lst)
    my_dict = dict(stat_author)

    # Save dictionary to JSON file
    with open(f'{author_stat_file}.json', 'w', encoding='utf-8') as f:
        json.dump(my_dict, f)
    f.close()
    import numpy as np

    names = list(stat_author.keys())
    values = list(stat_author.values())
    
    for i in range(len(names)):
        if names[i] is None:
              names[i] = "unknown"
    print(names)
    plt.bar(names, values, width=0.2)
    plt.xlabel('Author Name')
    plt.ylabel('Num of articles')
    plt.title('Number of articles per author')
    plt.savefig(f"static/{save_fig_path}")
    return set_author
def processing_date(data,line_chart_name, name):
     # Extract data for x and y axis
    x = list(data.keys())
    y = list(data.values())

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the data as a line chart
    ax.plot(x, y)

    # Set the chart title and axis labels
    ax.set_title(name)
    ax.set_xlabel('Time')
    ax.set_ylabel('Num of articles')

    # Save the chart to a file
    plt.savefig(f'static/{line_chart_name}')

def process_content(content):
    content = preprocess(content)
    num_words = count_words_fast(content)

import pymongo
from pymongo import MongoClient
# Replace the following with your MongoDB Atlas connection string
uri = "mongodb+srv://laptrinhmang:EKolZui6ZVocPcqR@cluster0.jxtulcr.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient to connect to MongoDB Atlas
client = MongoClient(uri)

db = client.reactionary
dkn = db.articles
viettan = db.viettan
author_lst = []
date_lst = []
date_format = "%d/%m/%y, %H:%M"
items =[]
with open('/home/baoanh/Desktop/Ky2Nam5/Lập trình mạng/code/mongodb_webscraper/mongodb_webscraper/spiders/links.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

tmp = [obj["link"] for obj in data]
start_urls = [name for name in tmp if name.startswith("https://")]

##########################################
##              DAI KY NGUYEN           ##
##########################################
articles_dkn = {}
i = 0
for item in dkn.find():
    # items.append(item)
    i = i + 1
    if (i<= 10):
        articles_dkn[item["title"][0]] = item["content"][:200]
    author = item["author"]
    date= item["date"]
    author_lst.append(author)
    datetime_obj = datetime.datetime.strptime(date, date_format)
    date_lst.append(datetime_obj)
# print(articles_dkn)
set_authors = processing_author(author_lst, "set_author_dkn", "stat_author_dkn", "dkn_author_stat.png")

# group the dates by month
dates_by_month = {}
date_lst = sorted(date_lst)
for item in date_lst:
    month = item.strftime('%m/%Y')
    if month not in dates_by_month:
        dates_by_month[month] = []
    dates_by_month[month].append(item)
updated_dates = {}
for month, dates in dates_by_month.items():
    updated_dates[month] = len(dates)
# print(updated_dates)
# processing_date(updated_dates,"dkn_line_chart.png","DKN.tv")


##########################################
##                VIET TAN              ##
##########################################
num_articles_vt = 0
date_format2 = "%d/%m/%Y"
author_lst2 = []
date_lst2 = []
items2 =[]
articles_vt = {}
#viettan statistics
i = 0
for item in viettan.find():
    # items.append(item)
    i = i + 1
    if (i<= 10):
        articles_vt[item["Title"]] = item["Content"][:200]
    num_articles_vt = num_articles_vt + 1
    title = item["Title"]
    content = item["Content"]
    author = item["Author"]
    date= item["Date"]
    author_lst2.append(author)
    datetime_obj = datetime.datetime.strptime(date, date_format2)
    date_lst2.append(datetime_obj)
set_authors2 = processing_author(author_lst2, "set_author_vt", "stat_author_vt", "vt_author_stat.png")

# group the dates by month
dates_by_year = {}
date_lst2 = sorted(date_lst2)
for item in date_lst2:
    year = item.strftime('%Y')
    if year not in dates_by_year:
        dates_by_year[year] = []
    dates_by_year[year].append(item)
updated_dates21 = {}
updated_dates22 = {}
count = 0
for year, dates in dates_by_year.items():
    count = count + 1
    
    if (count >10):
         updated_dates22[year] = len(dates)
    else:
         updated_dates21[year] = len(dates)
# processing_date(updated_dates2,"vt_line_chart.png","Viettan.org")

@app.route('/')
def index():
    return render_template('index.html', 
                           authors= set_authors, 
                           num_author_dkn = len(set_authors),
                           num_articles_dkn = len(start_urls),
                           urls = start_urls,
                           num_articles_vt = num_articles_vt,
                           num_author_vt = len(set_authors2),
                           dates_by_month=updated_dates,
                           dates_by_month21=updated_dates21,
                           dates_by_month22=updated_dates22,
                           articles_dkn = articles_dkn,
                           articles_vt = articles_vt)
