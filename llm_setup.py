from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def setup_chain(api_key):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",  # ✅ replace the broken model name
        temperature=0.7,
        api_key=api_key
    )

    prompt = PromptTemplate(
        input_variables=["niche", "count"],
        template=(
            "You are a helpful social media assistant.\n"
            "Generate {count} engaging and complete social media posts about \"{niche}\".\n"
            "Each post should be a natural, human-written text including emojis.\n"
            "In addition, provide relevant hashtags as a list.\n"
            "Output a JSON array of objects, each with keys:\n"
            " - text: full post content including emojis\n"
            " - hashtags: list of hashtags without spaces\n"
            "Example output:\n"
            '[{{"text": "Love the new trends in {niche}! 😊", "hashtags": ["#fashion", "#style"]}}, ...]\n'
        )
    )

    return prompt | llm

