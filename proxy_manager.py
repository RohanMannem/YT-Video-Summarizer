import requests
import random
import streamlit as st

WEBSHARE_PROXY_LIST_URL = st.secrets["WEBSHARE_PROXY_LIST_URL"]

def get_proxy_pool():
    try:
        response = requests.get(WEBSHARE_PROXY_LIST_URL, timeout=10)
        response.raise_for_status()
        raw_proxies = response.text.strip().splitlines()
        return [f"http://{proxy.strip()}" for proxy in raw_proxies if proxy.strip()]
    except Exception as e:
        print(f"Failed to download proxy list: {e}")
        return []

# Randomly select one proxy from the list
def get_random_proxy():
    proxy_pool = get_proxy_pool()
    if not proxy_pool:
        raise Exception("No proxies available from Webshare.")
    return random.choice(proxy_pool)
