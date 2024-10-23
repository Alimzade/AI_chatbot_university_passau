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
        "Your responses must be concise, polite, correct, and informative, addressing the needs of students. "
        "If the user greets you (e.g., 'hi', 'hello'), respond politely with a greeting and ask how you can assist them today. "
        "If the user thanks you or expresses gratitude, acknowledge it politely and offer further assistance if needed. "
        "If users ask questions unrelated to your main tasks, kindly let them know that you are not able to assist with that but can help with module catalog-related questions. "
        "Ensure that your answers are factually correct and directly address the questions asked. Use a step-by-step approach to provide accurate information."
    ),
}

    messages = []
    messages.append(system_prompt)

    for entry in chat_history:
        messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": "gpt-4-turbo",
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
        .replace("\n", "<br>")  # Handle line breaks
        .replace("\*\*(.*?)\*\*", r"<strong>\1</strong>")
    )