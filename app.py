# Streamlit Interactive Dashboard

import streamlit as st
import pandas as pd
import json
from generate import generate_posts, clean_hashtags, get_post_strings  # reuse your logic

st.title("Social Media Post Generator")

# Ask for email first
email = st.text_input("Enter your email to get started:")

# Validate email (basic check)
def is_valid_email(e):
    return "@" in e and "." in e and len(e) > 5

if email and is_valid_email(email):
    st.success(f"Thanks for subscribing, {email}!")
# User inputs
niche = st.text_input("Enter niche:", placeholder="e.g., nails, fitness, tech gadgets")
count = st.number_input("Number of posts (max 5):", min_value=1, max_value=5, value=1, step=1)

# When user clicks Generate, store posts in session_state
if st.button("Generate Posts"):
    with st.spinner("Generating posts..."):
        posts = generate_posts(niche, count)
        posts = clean_hashtags(posts)
        post_list = get_post_strings(posts)
        st.session_state['posts'] = posts
        st.session_state['post_list'] = post_list
        st.session_state['niche'] = niche

# Display saved posts and download buttons if available
if 'posts' in st.session_state and st.session_state['posts']:
    posts = st.session_state['posts']
    post_list = st.session_state['post_list']
    niche = st.session_state['niche']

    st.success(f"Generated {len(posts)} posts for niche '{niche}':")

    # Display posts with spacing
    for post in post_list:
        st.write(post)
        st.markdown("---")

    # Prepare downloadable files
    txt_content = "\n\n".join([p['text'] for p in posts])
    df = pd.DataFrame(posts)
    df_csv = df[['text']].to_csv(index=False)

    # Download buttons (always visible if posts exist)
    st.download_button(
        label="Download TXT",
        data=txt_content,
        file_name=f"{niche.replace(' ', '_')}.txt",
        mime="text/plain"
    )

    st.download_button(
        label="Download CSV",
        data=df_csv,
        file_name=f"{niche.replace(' ', '_')}.csv",
        mime="text/csv"
    )

