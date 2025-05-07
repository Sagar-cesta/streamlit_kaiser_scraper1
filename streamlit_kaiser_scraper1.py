import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

st.set_page_config(page_title="Kaiser File Scraper", layout="wide")
st.title("🗂️ Kaiser Permanente Machine-Readable File Extractor")

# Input form
with st.form("scraper_form"):
    url = st.text_input("🔗 Enter the transparency page URL:", 
                        value="https://healthy.kaiserpermanente.org/northern-california/front-door/machine-readable")
    submit = st.form_submit_button("Get Downloadable Files")

if submit:
    st.info("⏳ Scraping Kaiser page... please wait up to 30 seconds.")

    # Setup Selenium in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)

        # Expand all dropdowns (+)
        expand_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-analytics-label='Expand']")
        for btn in expand_buttons:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)

        # Find all download links
        download_links = driver.find_elements(By.LINK_TEXT, "download")

        files = []
        for link in download_links:
            href = link.get_attribute("href")
            if href and (href.endswith(".zip") or href.endswith(".json")):
                file_name = href.split("/")[-1]
                files.append((file_name, href))

        if files:
            st.success(f"✅ Found {len(files)} downloadable files.")
            for name, link in files:
                st.markdown(f"[📄 {name}]({link})", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No .zip or .json files found.")

    except Exception as e:
        st.error(f"❌ Error occurred: {str(e)}")

    finally:
        driver.quit()
