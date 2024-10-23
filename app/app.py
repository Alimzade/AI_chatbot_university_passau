from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from fastapi.staticfiles import StaticFiles
from .LLM import get_llm_response
from vectorize_query import query_modules
import json
import uuid
from .history import (
    save_message_to_text,
    read_chat_history_from_text,
    save_course_details,
    read_course_details,
    clear_chat_history_for_user,
)

from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Add session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.post("/clear")
async def clear_chat(request: Request):
    session_id = request.session.get("session_id")
    clear_chat_history_for_user(session_id)
    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Generate a session ID if it doesn't exist
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    session_id = request.session["session_id"]
    chat_history = read_chat_history_from_text(session_id)
    
    with open("app/templates/index.html") as f:
        template = Template(f.read())
    return template.render(chat_history=chat_history)


@app.post("/query", response_class=RedirectResponse)
async def handle_query(request: Request, query: str = Form(...)):

    # Ensure user session
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    session_id = request.session["session_id"]

    chat_history = read_chat_history_from_text(session_id)

    # Call query_modules to get the course results
    courses_results = query_modules(query)

    # Limit course details to only relevant courses (and truncate if too long)
    if courses_results is not None and not courses_results.empty:
        # Convert relevant course details to a list of dictionaries
        courses_list = courses_results.to_dict(orient='records')
        
        # Limit the number of courses included in the prompt to 5
        courses_list = courses_list[:5]

        # Format course details as a concise summary
        new_course_details = json.dumps(courses_list, indent=4)
    else:
        new_course_details = "[]"

    previous_course_details = read_course_details(session_id)

    # Only include relevant course details, avoid appending unnecessary history
    updated_course_details = new_course_details + "\n" + previous_course_details

    # Debugging step: check prompt length again
    #prompt_length = len(query) + len(str(chat_history)) + len(str(updated_course_details))
    #print(f"Prompt Length After Update: {prompt_length}")

    try:
        llm_response = get_llm_response(query, chat_history, updated_course_details)
    except Exception as e:
        llm_response = f"Error occurred: {e}"

    # Save chat messages for the user session
    save_message_to_text(session_id, "user", query)
    save_message_to_text(session_id, "assistant", llm_response)

    # Save only relevant course details for the user session
    save_course_details(session_id, new_course_details, llm_response)

    # Redirect to the main page after handling the query
    return RedirectResponse(url="/", status_code=303)

app.mount("/static", StaticFiles(directory="static"), name="static")