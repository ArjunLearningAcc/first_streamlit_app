import streamlit
import pandas 
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My Parents healthy dinner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry oat meal')
streamlit.text('kale, spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])


# selecting the  records which are picked in the above code
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# working code properly -- testing done 

streamlit.header("Fruityvice Fruit Advice!")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# writes the user entered text in a text box
fruit_choice = streamlit.text_input('What fruit would you like information about?','Watermelon')
streamlit.write('The user entered ', fruit_choice)


# takes the json version and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# creates a dataframe over the normalized data 
streamlit.dataframe(fruityvice_normalized)

# completed and working code till data loading from various sources

streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


# added a new text box
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('test')")


