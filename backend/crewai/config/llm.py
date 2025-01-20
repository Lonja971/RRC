from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
	max_tokens= 5000
)