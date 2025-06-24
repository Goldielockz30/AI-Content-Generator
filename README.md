# Create an AI Content Generator - Step by Step Guide

Build your own AI-powered content generator using fully local tools (no OpenAI). 

This generator will let users input a niche and get multiple posts with emojis and hashtags—outputting .txt or .csv formats.

## Tool kit

- Python - It's where all your code, logic and LLM interaction, lives.

- VS Code + Python extension - The easiest, free, professional coding editor. You will run your python and streamlit apps from here.

- Ollama - This runs your Large Language Model we are using Mistral.

- Streamlit (clean dashboard UI) - turns your python into a web app with zero front end coding.

- Your own machine - Local Hosting (no internet needed after setup)

# 🧩 Step 1 – Environment Setup

### Download Python


- Windows: Download and install from [python.org](https://www.python.org/) or via the Microsoft Store. Be sure to check “Add Python to PATH” in the installer .

- MacOS/Linux: Usually comes pre-installed, or install via:

```bash
brew install python  # macOS (Homebrew)
sudo apt-get install python3  # Ubuntu/Debian

```

### Im using VS Code with python extension

- If you dont already have it download VSCode from https://code.visualstudio.com/ and install the python extension

- To check if you have python installed locally in vs code

```bash 
Python --version

```

- You will see this if python exists

```bash
Python 3.12.1
```
### Create your project folder

- Click on File > Open Folder (or Open on Mac).

- Create a new folder for your project if needed, then select/open it.

Optionally you could 

- Use VS Code command line to create folder

```bash
mkdir my-project # To create a new folder

cd my-project # Navigate into the folder to start working

```
- Then go to file > Open Folder (or Open on Mac) and open the folder you just created

### Create a virtual environment

```bash
python -m venv venv

venv\Scripts\activate      # Windows
```
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
```

### Install dependencies

```bash 
pip install langchain langchain-ollama ollama pandas streamlit
```

Upgrade pip if it suggests just copy and paste

```bash
python.exe -m pip install --upgrade pip
```

### Install Ollama for local LLM hosting

- https://ollama.com/download

You may need to close and re open VS code to recognise the path 

- Navigate back to your working folder and open command line check if Ollama is there

```bash 
ollama --version
```
- Re activate your virtual environment 

```bash 
.\venv\Scripts\Activate.ps1
```
### Download a model, e.g. Mistral 7B

```bash
ollama pull mistral
```

# ⚙️ Step 2 – Connect the Model Locally

### Create a new file named llm_setup.py

```bash
New-Item -Path . -Name "llm_setup.py" -ItemType "File"
```

- Paste this code inside the llm_setup.py file

```bash 
# llm_setup.py
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM

prompt = PromptTemplate(
    input_variables=["niche", "count"],
    template=(
        "You are a helpful social media assistant.\n"
        "Generate {count} engaging social media posts about \"{niche}\".\n"
        "Include emojis and relevant hashtags.\n"
        "Output JSON array of objects with keys: text, hashtags.\n"
    )
)

llm = OllamaLLM(
    model="mistral",
    format="json"  # Valid formats are "" or "json"
)

chain = prompt | llm
```
- This leverages LangChain with Ollama locally

# 📝 Step 3 – Generate and Export Content

- Create a file named generate.py

```bash
New-Item -Path . -Name "generate.py" -ItemType "File"
```
- Paste this code inside the generate.py file

```bash
# generate.py

import json
import pandas as pd
from llm_setup import chain

def clean_hashtags(posts):
    for post in posts:
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
    try:
        posts = json.loads(result)
        
        # If posts is a dict with keys like Post1, Post2, convert to list:
        if isinstance(posts, dict):
            # Extract values (post dicts) and sort by key to keep order if needed
            posts_list = [posts[k] for k in sorted(posts.keys())]
            posts = posts_list
        
        if not isinstance(posts, list):
            print("⚠️ Expected list, got:", type(posts))
            return []
        
        return posts[:count]
    except json.JSONDecodeError:
        print("⚠️ Failed to decode JSON. Raw output:", result)
        return []

def get_post_strings(posts):
    lines = []
    for p in posts:
        text = p.get('text', '').strip()
        hashtags = p.get('hashtags', [])
        clean_tags = [tag.strip().replace(" ", "") for tag in hashtags if tag.strip()]
        line = f"{text} {' '.join(clean_tags)}"
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

    # Get list of strings ready for copy-paste
    post_list = get_post_strings(posts)

    print("\nHere is the list of posts with hashtags (copy and paste as needed):\n")
    print(post_list)  # prints the Python list syntax

    # Optional: print each post on its own line for easy reading
    print("\n--- Posts preview ---")
    for post in post_list:
        print(post)
        print()  # <-- this adds a blank line between posts
    print("---------------------\n")

    # Save files as before
    save_to_files(posts, niche.replace(" ", "_"))

```
# ✅ Reinstall and Test
```bash 
pip install -U langchain-ollama
```

- Run the script and examine the output.

```bash
python generate.py
```

Optional

- Create an examples folder once you happy with your outputs

```bash
mkdir examples
```
- Move your output files  into that folder eg.

```bash
move hair.csv examples\ 
move hair.txt examples\ 
```

# Create a requirements.txt file

```bash
pip freeze > requirements.txt

```
- Replace the long list in the requirements.txt file with this

```bash
pandas>=2.0.0
langchain-core>=0.3.66
langchain-ollama>=0.3.3
streamlit>=1.46.0
altair>=5.5.0
```

- Now you can run this code to install requirements

```bash
pip install -r requirements.txt

```

# Bonus! Create a Dashboard - with downloadable outputs

- A dashboard serves as a centralized, interactive interface to make your data or app more accessible, user-friendly, and actionable.

- Create a file named app.py

```bash
New-Item -Path . -Name "app.py" -ItemType "File"
```
- Paste this code inside the app.py file


```bash
# Streamlit Interactive Dashboard

import streamlit as st
import pandas as pd
import json
from generate import generate_posts, clean_hashtags, get_post_strings  # reuse your logic

st.title("Social Media Post Generator")

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
```
# Run your interactive streamlit dashboard and test it out

```bash
streamlit run app.py
```


# Extras

### You can easily add more features over time:

- Analytics and charts (e.g., hashtag frequency)

- Integration with social media APIs for direct posting

- Customization options for post tone, length, or format

- Multi-niche comparisons or history of generated posts

- Create a file named generate.py

# 🧠  Refine Your Prompts

- If formatting or tone needs adjustment, tweak the PromptTemplate.


## Example improvements:

- Force uppercase hashtags: #Hashtag

- Add length constraints or tone: “Upbeat and friendly.”

- Prompt engineering is essential for reliable social content—LocalAI provides only core building blocks


# Next Steps
- Improve prompts (tone, length, niche specificity)

- Add customization options: emoji style, formatting

- Package your tool (pip installable CLI or web app)

- Sell as digital product: host on GitHub or Gumroad