"""
Name: Kailee Hollister
CS230: Anqi Xu
Data: Fast Food Restaurants
URL: Link to your web application online

Description:
This program summarizes the top fast food restaurants by state through an interactive pie chart.
It also gives the top cities and states (user choice) with the most Burger king locations.
The app contains a multiselect button for the fast food restaurants, which it then adds to a total bar chart by state.
It shows a folium map of all fast food restaurants in Massachussetts (based on the data).
"""
import csv
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

st.title("Wesbite on Fast Food in America")
st.write("Welcome to this website on the analytics behind the most popular fast food restaurants in the US")
df = pd.read_csv("Fast_Food_Restaurants_8000_sample.csv")
from PIL import Image
image = Image.open('ffood.webp')
st.image(image, caption='')

state = st.sidebar.text_input("Enter a state abbreviation", "MA")
df["name"] = df["name"].str.capitalize()

#Pie chart for top 10 fast food restaurants in a selected state
def get_pie_chart(s):
    listName = []
    listCount = []
    name_by_state = df.loc[(df["province"] == s.upper()), ["province", "name"]]
    name_by_state = name_by_state.groupby(by="name").count()
    name_by_state = name_by_state.reset_index()
    name_by_state = name_by_state.sort_values(["province"], ascending=False)
    if len(name_by_state) >= 10:
        name_by_state = name_by_state[0:10]
    for i in range(len(name_by_state)):
        listName.append(name_by_state.iloc[i, 0])
        listCount.append(name_by_state.iloc[i, 1])
    return listName, listCount

def make_chart():
    a, b = get_pie_chart(state)
    st.header(f"Top {len(a)} Fast Food Restaurants in {state}")
    fig, ax = plt.subplots()
    ax.pie(b, labels=a, autopct='%.2f%%')
    st.pyplot(fig)
make_chart()

def make_bar1():
    restaurant = df.loc[(df["province"] == "MA"), ["name", "province"]]
    restaurant = restaurant.groupby(by="name").count()
    restaurant = restaurant.reset_index()
    restaurant = restaurant.sort_values(["province"], ascending = False)
    if len(restaurant) >= 10:
        restaurant = restaurant[0:10]
    area = []
    count = []
    for i in range(len(restaurant)):
        area.append(restaurant.iloc[i,0])
        count.append(restaurant.iloc[i,1])
    area.reverse()
    count.reverse()
    st.header(f"The Top {len(area)} Most Frequent Restaurant Locations in Massachussetts")
    fig, ax = plt.subplots()
    ax.bar(area, count)
    plt.xlabel("Restaurant")
    plt.ylabel("Frequency")
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
make_bar1()

state_or_city = st.selectbox("Please select a state or city analysis", ("city", "province"))

def get_bar_chart2(b):
    if b == "city":
        name_by_area = df.loc[(df["name"] == "Burger king"), ["city", "name"]]
    else:
        name_by_area = df.loc[(df["name"] == "Burger king"), ["province", "name"]]
    name_by_area = name_by_area.groupby(by=b).count()
    name_by_area = name_by_area.reset_index()
    name_by_area = name_by_area.sort_values(["name"], ascending = False)
    if len(name_by_area) >= 10:
        name_by_area = name_by_area[0:10]
    area = []
    count = []
    for i in range(len(name_by_area)):
        area.append(name_by_area.iloc[i,0])
        count.append(name_by_area.iloc[i,1])
    return area, count

def make_bar2():
    a, b = get_bar_chart2(state_or_city)
    a.reverse()
    b.reverse()
    if state_or_city == "city":
        st.header(f"The Top {len(a)} Cities With the Most Burger King Locations")
    else:
        st.header(f"The Top {len(a)} States With the Most Burger King Locations")
    fig, ax = plt.subplots()
    ax.bar(a,b, width = .75, color="r")
    plt.xlabel(state_or_city)
    plt.ylabel("Frequency")
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
make_bar2()

plt.style.use('seaborn-whitegrid')

def restaurant_type():
    #number og restertants in each states
    st.title('States vs. Number of Fast Food Restaurants in the state')
    df = pd.read_csv("Fast_Food_Restaurants_8000_sample.csv")
    df = df.sort_values(by=["name"])
    restaurant_options= df["name"].unique()
    rest_values = df['name'].values.tolist()
    restaurant= []
    restaurant.append(rest_values)
    selected_condition = st.multiselect('What restaurant do you want to view', restaurant_options)
    df= df[df["name"].isin(selected_condition)]
    counts = df["province"].value_counts()
    y = counts
    x = y.index
    plt.bar(x, y)
    fig, chart= plt.subplots()
    chart.bar(x,y)
    chart.xaxis.set_label_text("State")
    plt.xticks(rotation='vertical')
    chart.yaxis.set_label_text("Number of Restaurants")
    chart.set_facecolor("white")
    fig.suptitle("Total Number of Selected Restaurants in Each State")
    st.pyplot(fig)
restaurant_type()


from streamlit_folium import folium_static
import folium
df.head()
center = [0,0]
st.header("Map of Fast Food Restaurants in Massachusetts")
fastfood = folium.Map(location = [42, -72], zoom_start = 8)
for i,j in df.iterrows():
    location = [j["latitude"], j["longitude"]]
    if j['province'] == "MA":
        folium.Marker(location, popup=f"Name:{j['name']}\nState:{j['province']}\nCity:{j['city']}").add_to(fastfood)
folium_static(fastfood)


if st.button("Click here for a surprise"):
    st.balloons()
