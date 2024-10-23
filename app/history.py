import os
import json
import re

# Directory to store session-specific chat and course histories
history_dir_path = "chat_histories"
course_history_dir_path = "course_histories"

# Helper function to get the session-specific chat history file
def get_history_file_path(session_id: str) -> str:
    return os.path.join(history_dir_path, f"{session_id}_chat_history.txt")

# Helper function to get the session-specific course history file
def get_course_history_file_path(session_id: str) -> str:
    return os.path.join(course_history_dir_path, f"{session_id}_course_history.json")


# Session-specific chat history
def save_message_to_text(session_id: str, role: str, content: str):
    if not os.path.exists(history_dir_path):
        os.makedirs(history_dir_path)

    history_file_path = get_history_file_path(session_id)

    with open(history_file_path, "a", encoding="utf-8") as file:
        file.write(f"{role}: {content}\n")

def read_chat_history_from_text(session_id: str) -> list:
    history_file_path = get_history_file_path(session_id)

    if not os.path.exists(history_file_path):
        return []

    with open(history_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines:
        return []

    chat_history = []
    for line in lines:
        if ": " in line:
            role, content = line.split(": ", 1)
            chat_history.append({"role": role, "content": content.strip()})

    return chat_history

def clear_chat_history_for_user(session_id: str):
    """Clear the chat history for a specific user session."""
    history_file_path = get_history_file_path(session_id)

    if os.path.exists(history_file_path):
        os.remove(history_file_path)


# Session-specific course history
def save_course_details(session_id: str, new_course_details: str, llm_response: str):
    """Save course details for the specific user session."""
    if not os.path.exists(course_history_dir_path):
        os.makedirs(course_history_dir_path)

    course_history_file_path = get_course_history_file_path(session_id)

    course_history = []
    if os.path.exists(course_history_file_path):
        try:
            with open(course_history_file_path, "r", encoding="utf-8") as file:
                course_history = json.load(file)
        except json.JSONDecodeError:
            print("Error: course history file is not valid JSON. Starting with an empty history.")

    try:
        parsed_data = json.loads(new_course_details)

        if isinstance(parsed_data, list):
            new_courses = parsed_data
        elif isinstance(parsed_data, dict):
            new_courses = [parsed_data]
        else:
            print("Error: new_course_details has an unexpected format (not a list or dict)")
            return

    except json.JSONDecodeError as e:
        print(f"Error parsing new_course_details as JSON: {e}")
        return

    if not new_courses:
        print("No new courses to process.")
        return

    courses_to_save = []

    for course in new_courses:
        try:
            course_title = course['Course Title'].lower()
            pattern = re.compile(rf"\b{re.escape(course_title)}\b", re.IGNORECASE)

            if pattern.search(llm_response.lower()):
                courses_to_save.append(course)

        except KeyError:
            print("Error: 'Course Title' key not found in a course dictionary")

    if courses_to_save:
        course_history = courses_to_save + course_history

        # Limit history to the last 5 entries
        if len(course_history) > 5:
            course_history = course_history[:5]

        try:
            with open(course_history_file_path, "w", encoding="utf-8") as file:
                json.dump(course_history, file)
        except Exception as e:
            print(f"Error saving course history to file: {e}")



def read_course_details(session_id: str) -> str:
    """Read course details for the specific user session."""
    course_history_file_path = get_course_history_file_path(session_id)

    course_history = []

    if os.path.exists(course_history_file_path):
        try:
            with open(course_history_file_path, "r", encoding="utf-8") as file:
                course_history = json.load(file)
        except json.JSONDecodeError:
            print("Error: course history file is not valid JSON. Returning empty history.")

    if course_history:
        course_history_str = "\n".join([json.dumps(course) for course in course_history])
    else:
        course_history_str = ""

    return course_history_str


def clear_chat_history():
    """Clear global chat and course history."""
    if os.path.exists(history_dir_path):
        for file in os.listdir(history_dir_path):
            os.remove(os.path.join(history_dir_path, file))

    if os.path.exists(course_history_dir_path):
        for file in os.listdir(course_history_dir_path):
            os.remove(os.path.join(course_history_dir_path, file))
