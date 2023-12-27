""""
Consider that you have been hired by a Multiplex management organization to extract the information of the top 50 movies with the best average rating.
The information required is Average Rank, Film, and Year.
You are required to write a Python script webscraping_movies.py that extracts the information and saves it to a CSV file top_50_films.csv. You are also required to save the same information to a database Movies.db under the table name Top_50.
"""

# 1. Importing libraries required for the assignment
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

# 2. Initialization of known entities

# Web to extract the data
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
cvs_path = '/home/aben/Documents/IBM/Course3/W2/top_50.csv'

# Information required
#df = pd.DataFrame(columns=["Average Rank", "Film", "Year", "Roten Tomatoes' Top 100"])
df = pd.DataFrame(columns=["Film", "Year", "Roten Tomatoes' Top 100"])

# Loop counter to iterate over the 50 top results
count = 0 

# 3. Loading the webpage for webscraping
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# 4. Scraping the web
# The variable tables gets the body of all the tables in the web page and the variable rows gets all the rows of the first table.
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count < 50:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {
                #"Average Rank": col[0].contents[0],
                "Film": col[1].contents[0],
                "Year": col[2].contents[0],
                "Roten Tomatoes' Top 100": col[3].contents[0]
            }
            df1 = pd.DataFrame(data_dict, index = [0])
            df = pd.concat([df, df1], ignore_index = True)
            count += 1
    else:
        break

#print(df)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df2 = df[df['Year'].between(2000, 2009)]
print(df2)

# 5. Storing the data
df.to_csv(cvs_path)
# To store the required data in a database, you first need to initialize a connection to the database, save the dataframe as a table, and then close the connection.
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()

