import os
import json
import re

history_file_path = "chat_history.txt"
courses_file_path = "courses_history.json"

def save_message_to_text(role: str, content: str):
    with open(history_file_path, "a", encoding="utf-8") as file:
        file.write(f"{role}: {content}\n")

def read_chat_history_from_text() -> list:
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

def save_course_details(new_course_details: str, llm_response: str):

    course_history = []
    if os.path.exists(courses_file_path):
        try:
            with open(courses_file_path, "r", encoding="utf-8") as file:
                course_history = json.load(file)
        except json.JSONDecodeError:
            print("Error: courses_history.json is not valid JSON. Starting with an empty history.")

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
            #print("Comparing:", course_title, "and", llm_response.lower())
            pattern = re.compile(rf"\b{re.escape(course_title)}\b", re.IGNORECASE)

            if pattern.search(llm_response.lower()):
                #print(f"{course_title} is in the response")
                courses_to_save.append(course) 

        except KeyError:
            print("Error: 'Course Title' key not found in a course dictionary")

    if courses_to_save:
        course_history = courses_to_save + course_history

        # Limit history to the last 5 entries
        if len(course_history) > 5:
            course_history = course_history[:5]

        try:
            with open(courses_file_path, "w", encoding="utf-8") as file:
                json.dump(course_history, file)
        except Exception as e:
            print(f"Error saving course history to file: {e}")

def read_course_details() -> str:
    course_history = []

    if os.path.exists(courses_file_path):
        try:
            with open(courses_file_path, "r", encoding="utf-8") as file:
                course_history = json.load(file)
        except json.JSONDecodeError:
            print("Error: courses_history.json is not valid JSON. Returning empty history.")
    
    if course_history:
        course_history_str = "\n".join([json.dumps(course) for course in course_history])
    else:
        course_history_str = ""
    
    return course_history_str

def clear_chat_history():
    if os.path.exists(history_file_path):
        os.remove(history_file_path)
    if os.path.exists(courses_file_path):
        os.remove(courses_file_path)
        