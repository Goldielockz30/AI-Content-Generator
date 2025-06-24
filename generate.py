
# generate.py

import json
import pandas as pd
from llm_setup import chain

def clean_hashtags(posts):
    for post in posts:
        if not isinstance(post, dict):
            print(f"⚠️ Skipping invalid post (not a dict): {post} (type={type(post)})")
            continue
        hashtags = post.get("hashtags", "")
        if isinstance(hashtags, str):
            tags_list = hashtags.split()
        elif isinstance(hashtags, list):
            tags_list = hashtags
        else:
            tags_list = []

        post['hashtags'] = [tag.replace(" ", "") for tag in tags_list if tag.strip()]
    return posts

def generate_posts(niche, count=5):
    result = chain.invoke({"niche": niche, "count": count})
    print(f"DEBUG: Raw result from chain.invoke:\n{result}\n")
    try:
        posts = json.loads(result)
        print(f"DEBUG: Type of posts after JSON load: {type(posts)}")

        if isinstance(posts, dict):
            # If posts is a dict, convert to list by sorted keys
            posts_list = [posts[k] for k in sorted(posts.keys())]
            posts = posts_list

        # Flatten any nested lists inside posts (if any post is itself a list)
        fixed_posts = []
        for post in posts:
            if isinstance(post, list):
                print(f"DEBUG: Flattening nested list post: {post}")
                fixed_posts.extend(post)
            else:
                fixed_posts.append(post)
        posts = fixed_posts

        if not isinstance(posts, list):
            print("⚠️ Expected a list of posts but got:", type(posts))
            return []

        return posts[:count]
    except json.JSONDecodeError:
        print("⚠️ Failed to decode JSON. Raw output:", result)
        return []

def get_post_strings(posts):
    lines = []
    for p in posts:
        if not isinstance(p, dict):
            print(f"⚠️ Skipping invalid post in get_post_strings: {p} (type={type(p)})")
            continue
        text = p.get('text', '').strip()
        hashtags = p.get('hashtags', [])
        clean_tags = [tag.strip().replace(" ", "") for tag in hashtags if tag.strip()]
        line = text # Hashtags already included in 'text'
        lines.append(line)
    return lines

def save_to_files(posts, filename_prefix="posts"):
    if not posts:
        print("⚠️ No posts to save.")
        return

    with open(f"{filename_prefix}.txt", "w", encoding="utf8") as f:
        for p in posts:
            f.write(f"{p['text']}\n\n")

    print(f"✅ Posts saved to {filename_prefix}.txt")

    # Save only 'text' column to CSV, since it has hashtags inside
    df = pd.DataFrame(posts)
    df = df[['text']]  # keep only text column
    df.to_csv(f"{filename_prefix}.csv", index=False)
    print(f"✅ Posts saved to {filename_prefix}.csv")

if __name__ == "__main__":
    niche = input("Enter niche: ")
    count = int(input("Number of posts: "))
    posts = generate_posts(niche, count)
    posts = clean_hashtags(posts)

    post_list = get_post_strings(posts)

    print("\nHere is the list of posts with hashtags (copy and paste as needed):\n")
    print(post_list)

    print("\n--- Posts preview ---")
    for post in post_list:
        print(post)
        print()
    print("---------------------\n")

    save_to_files(posts, niche.replace(" ", "_"))

