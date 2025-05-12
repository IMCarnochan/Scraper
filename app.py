import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("Scrape me!")
query = st.text_input("Search for an item:")

if query:
    search_query = query.replace(' ', '+')
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&LH_Sold=1&LH_Complete=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.select("li.s-item")
    count = 0

    for item in items:
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        img_tag = item.select_one(".s-item__image-img")

        if title_tag and price_tag and img_tag:
            title = title_tag.get_text()
            price = price_tag.get_text()
            img_url = img_tag.get("src")

            st.image(img_url, width=150)
            st.write(f"**{title}**")
            st.write(f"Price: {price}")
            st.markdown("---")

            count += 1
            if count == 5:
                break

    if count == 0:
        st.write("No sold items found. Try another search.")
