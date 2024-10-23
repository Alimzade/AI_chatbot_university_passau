import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_url = os.getenv("API_URL")
api_key = os.getenv("API_KEY")


def get_llm_response(query: str, chat_history: list, courses_details: str) -> list:

    temperature = 0.3

    if not courses_details:
        user_prompt = (
            f"Now user wants to know: {query}"
            "Provide a concise and relevant response. Answer ONLY based on the context of history."
            "If you think that previous discussions are IRRELEVENT to users new question, ask user to be more precise or ask another question"
            "Ensure that your response is well-structured, factual, and directly addresses the user's needs."
            "Please use step by step approach to answer it accurately."
        )
        #temperature = 0
    else:
        user_prompt = (
            f"Now user wants to know: {query}"
            f"If user's question is not related to his previous questions, then use these details to answer the question:{courses_details}"
            "Provide a concise and relevant response to the user's new question. Otherwise answer based on context of chat history."
            "Ensure that your response is well-structured, factual, and directly addresses the user's needs."
            "Please use step by step approach to answer it accurately."
        )
        #temperature = 0.25

    system_prompt = {
        "role": "system",
        "content": (
            "You are a chatbot designed to assist students with questions related to the module catalogues of the AI Engineering and Informatics Master's Programs at the University of Passau. "
            "Your responses must be concise, correct, and informative enough to the needs of students."
            "Ensure that your answers are factually correct and directly address the questions asked. Use step-by-step approach to provide accurate information."
        ),
    }
    messages = []
    messages.append(system_prompt)

    for entry in chat_history:
        messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": "Mixtral-8x7B-Instruct-v0.1",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 1500,
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return (
        response.json()
        .get("choices")[0]
        .get("message")
        .get("content")
        .replace("\n", "<br>")
    )
