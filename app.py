import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Scrape me!")

query = st.text_input("Search for an item:")

@st.cache_data(show_spinner=False)
def fetch_sold_items(search_query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&LH_Sold=1&LH_Complete=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')

def parse_items(soup, max_results=5):
    items = soup.select("li.s-item")
    results = []
    for item in items:
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        img_tag = item.select_one(".s-item__image-img")

        if title_tag and price_tag and img_tag:
            results.append({
                "title": title_tag.get_text(),
                "price": price_tag.get_text(),
                "img_url": img_tag.get("src")
            })
            if len(results) >= max_results:
                break
    return results

if query:
    search_query = query.replace(' ', '+')
    soup = fetch_sold_items(search_query)
    results = parse_items(soup)

    if results:
        for item in results:
            st.image(item["img_url"], width=150)
            st.write(f"**{item['title']}**")
            st.write(f"Price: {item['price']}")
            st.markdown("---")
    else:
        st.write("No sold items found. Try another search.")
