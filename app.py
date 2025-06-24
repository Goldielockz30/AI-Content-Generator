# Streamlit Interactive Dashboard

import streamlit as st
import pandas as pd
from generate import generate_posts, clean_hashtags, get_post_strings

st.title("Social Media Post Generator")

# Ask for email first
email = st.text_input("Enter your email to get started:")

# Email validator
def is_valid_email(e):
    return "@" in e and "." in e and len(e) > 5

# Only show the rest of the UI if email is valid
if email and is_valid_email(email):
    st.success(f"Thanks for subscribing, {email}!")

    # User inputs
    niche = st.text_input("Enter niche:", placeholder="e.g., nails, fitness, tech gadgets")
    count = st.number_input("Number of posts (max 5):", min_value=1, max_value=5, value=1, step=1)

    # Generate posts
    if st.button("Generate Posts"):
        with st.spinner("Generating posts..."):
            posts = generate_posts(niche, count)
            posts = clean_hashtags(posts)
            post_list = get_post_strings(posts)
            st.session_state['posts'] = posts
            st.session_state['post_list'] = post_list
            st.session_state['niche'] = niche

    # Display & download if posts exist
    if 'posts' in st.session_state and st.session_state['posts']:
        posts = st.session_state['posts']
        post_list = st.session_state['post_list']
        niche = st.session_state['niche']

        st.success(f"Generated {len(posts)} posts for niche '{niche}':")

        for post in post_list:
            st.write(post)
            st.markdown("---")

        txt_content = "\n\n".join([p['text'] for p in posts])
        df = pd.DataFrame(posts)
        df_csv = df[['text']].to_csv(index=False)

        st.download_button("Download TXT", txt_content, f"{niche}.txt", mime="text/plain")
        st.download_button("Download CSV", df_csv, f"{niche}.csv", mime="text/csv")

# If email entered but invalid
elif email:
    st.error("Please enter a valid email to continue.")
