import streamlit as st
import requests
import pandas as pd
import re
from generate import generate_posts, clean_hashtags, get_post_strings

# 🔐 OpenAI API Key

api_key = st.secrets["openai_api_key"]
# MailerLite API settings

MAILERLITE_API_KEY = st.secrets["mailerlite"]["api_key"]
GROUP_ID = st.secrets["mailerlite"]["group_id"]  # The group ID for your list/group like "All Leads"

# Check if secrets are loaded correctly
st.title("🔐 Secret Key Test")
st.write("🔐 OpenAI Key Loaded:", bool(st.secrets["openai_api_key"]))
st.write("📧 MailerLite API Key Loaded:", bool(st.secrets["mailerlite"]["api_key"]))
st.write("📧 MailerLite Group ID Loaded:", bool(st.secrets["mailerlite"]["group_id"]))



HEADERS = {
    "Content-Type": "application/json",
    "X-MailerLite-ApiKey": MAILERLITE_API_KEY
}

def format_niche_tag(niche):
    tag = re.sub(r'[^\w\s-]', '', niche)  # remove non-word chars
    tag = re.sub(r'\s+', '-', tag)        # replace spaces with dashes
    return tag.lower()

def add_subscriber_to_group(email, niche):
    tag = format_niche_tag(niche)

    url = "https://api.mailerlite.com/api/v2/subscribers"
    data = {
        "email": email,
        "fields": {
            "niche": niche
        },
        "groups": [GROUP_ID],
        "tags": [tag]
    }

    response = requests.post(url, json=data, headers=HEADERS)

    if response.status_code in (200, 201):
        return True
    else:
        st.error(f"MailerLite error ({response.status_code}): {response.text}")
        return False

st.title("✨ Social Media Post Generator")

email = st.text_input("Enter your email to get started:")

def is_valid_email(e):
    return "@" in e and "." in e and len(e) > 5

if email and is_valid_email(email):
    niche = st.text_input("Enter niche:", placeholder="e.g., nails, fitness, tech gadgets")
    count = st.number_input("Number of posts (max 5):", min_value=1, max_value=5, value=1, step=1)

    if niche:
        if st.button("Subscribe & Generate Posts"):
            with st.spinner("Subscribing and generating posts..."):
                subscribed = add_subscriber_to_group(email, niche)
                if subscribed:
                    st.success(f"Thanks for subscribing with niche '{niche}'!")

                    # ✅ Pass API key to generate_posts()
                    posts = generate_posts(niche, count, api_key=api_key)
                    posts = clean_hashtags(posts)
                    post_list = get_post_strings(posts)
                    st.session_state['posts'] = posts
                    st.session_state['post_list'] = post_list
                    st.session_state['niche'] = niche

    if 'posts' in st.session_state and st.session_state['posts']:
        posts = st.session_state['posts']
        post_list = st.session_state['post_list']
        niche = st.session_state['niche']

        st.success(f"Generated {len(posts)} posts for niche '{niche}':")

        for post in post_list:
            st.write(post)
            st.markdown("---")

        txt_content = "\n\n".join([p.get('text', '') for p in posts])
        df = pd.DataFrame(posts)
        df_csv = df[['text']].to_csv(index=False)

        st.download_button("Download TXT", txt_content, f"{niche}.txt", mime="text/plain")
        st.download_button("Download CSV", df_csv, f"{niche}.csv", mime="text/csv")

elif email:
    st.error("Please enter a valid email to continue.")

elif api_key == "":
    st.warning("Please enter your OpenAI API key to use the generator.")
