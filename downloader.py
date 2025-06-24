import streamlit as st
import csv
import os
import requests
import tempfile


def save_img(url, path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            return f"✅ Downloaded: {os.path.basename(path)}"
        else:
            return f"❌ Failed: {url} (Status {response.status_code})"
    except Exception as e:
        return f"⚠️ Error downloading {url}: {e}"


def download_images(csv_path, keyword, folder_name):
    results = []
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_id = row.get('image_id', '')
            if keyword in image_id:
                image_url = f"https://iscan.britanniaiscan.com/input_file/{image_id}"
                filepath = os.path.join(folder_name, f"{image_id}.jpg")
                result = save_img(image_url, filepath)
                results.append(result)
    return results


st.title("🖼️ Britannia Image Downloader")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=['csv'])

category = st.selectbox(" Select a category to download", [
    'WAF', 'CAK', 'CHE', 'RUS', 'BIS', 'GHE', 'DAI', 'CRO'
])

download_button = st.button("📥 Download Images")

if uploaded_file and download_button:
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    folder_name = f"{category.lower()}_images"
    with st.spinner("Downloading..."):
        output = download_images(tmp_path, category, folder_name)

    st.success("Download complete!")
    for msg in output:
        st.write(msg)

    st.info(f"Images saved in: `{folder_name}/`")
