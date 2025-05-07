import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(page_title="Kaiser File Extractor", layout="wide")
st.title("📂 Kaiser Permanente File Extractor")

url = st.text_input("🔗 Enter a Kaiser Permanente Transparency URL")

if st.button("Get Downloadable Files") and url:
    try:
        st.info("🔄 Scraping... Please wait.")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")

        links = soup.find_all("a", href=True)
        download_links = []

        for a in links:
            if 'download' in a.text.lower() or any(a['href'].endswith(ext) for ext in ['.zip', '.json']):
                full_url = urljoin(url, a['href'])
                label = a.text.strip() or full_url.split("/")[-1]
                download_links.append((label, full_url))

        if download_links:
            st.success(f"✅ Found {len(download_links)} downloadable files:")
            for label, link in download_links:
                st.markdown(f"[📥 {label}]({link})")
        else:
            st.warning("⚠️ No downloadable .zip or .json files found.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

