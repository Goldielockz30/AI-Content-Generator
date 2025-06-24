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
