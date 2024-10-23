from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from .LLM import get_llm_response
from vectorize_query import query_modules
import json
from .history import (
    save_message_to_text,
    read_chat_history_from_text,
    save_course_details,
    read_course_details,
    clear_chat_history,
)

app = FastAPI()


@app.post("/clear")
async def clear_chat():
    clear_chat_history()
    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    chat_history = read_chat_history_from_text()
    with open("app/templates/index.html") as f:
        template = Template(f.read())
    return template.render(chat_history=chat_history)

@app.post("/query", response_class=HTMLResponse)
async def handle_query(request: Request, query: str = Form(...)):

    chat_history = read_chat_history_from_text()

    courses_results = query_modules(query)

    if courses_results.empty:
        new_course_details = "[]"
    else:
        courses_list = courses_results.to_dict(orient='records')
        new_course_details = json.dumps(courses_list, indent=4)

    previous_course_details = read_course_details()

    updated_course_details = new_course_details + "\n" + previous_course_details

    try:
        llm_response = get_llm_response(query, chat_history, updated_course_details)
    except Exception as e:
        llm_response = f"Error occurred: {e}"

    save_message_to_text("user", query)
    save_message_to_text("assistant", llm_response)

    save_course_details(new_course_details, llm_response)

    chat_history = read_chat_history_from_text()

    with open("app/templates/index.html") as f:
        template = Template(f.read())
    return template.render(
        chat_history=chat_history,
        query=query,
        courses_results=courses_results.to_html(classes="table table-striped"),
        llm_response=llm_response,
    )