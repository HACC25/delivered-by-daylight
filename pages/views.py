# pages/views.py

from django.shortcuts import render
import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from google import genai
import json

def home(request):
    return render(request, "pages/home.html")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# initialize Gemini
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash-lite"

# load csv only once
CSV_PATH = "manoa_courses.csv"
df = pd.read_csv(CSV_PATH)

# build the major-to-prefix map dynamically
unique_majors = df["dept_name"].unique()
major_prefix_map = {}

for major in unique_majors:
    prefix = major.split()[0].upper()
    major_prefix_map[major.lower()] = prefix


def build_context_for_major(major):
    # normalize user input
    major = major.lower()
    prefix_match = None

    # find matching major prefix
    for key, prefix in major_prefix_map.items():
        if key in major:
            prefix_match = prefix
            break

    if prefix_match is None:
        return ""

    # filter rows by prefix
    matches = df[df["Course ID"].str.startswith(prefix_match, na=False)]

    course_lines = []
    for _, row in matches.iterrows():

        course_id = row.get("Course ID", "")
        name = row.get("Course Name", "")
        desc = row.get("Description", "")
        prereq = row.get("Prerequisites", "")

        # protect against NaN
        desc = "" if pd.isna(desc) else desc
        prereq = "" if pd.isna(prereq) else prereq

        line = f"{course_id} - {name}. Description: {desc}"

        if prereq.strip():
            line += f" Prerequisites: {prereq}"

        course_lines.append(line)

    return "\n".join(course_lines)


def build_prompt(user_input, conversation_state, detected_major=None):
    # system instructions + restrictions
    base_rules = """
    You are an AI academic advisor for UH Mānoa.
    You must follow these rules:

    1. Do NOT use Markdown.
    2. Do NOT use bullet points or numbered lists.
    3. Only recommend UH Mānoa courses found in the dataset.
    4. For each course you recommend, include a one-sentence explanation.
    5. Keep everything in plain text.
    6. Do not ask for concentrations. If the user states a general field, proceed normally.
    """

    # handle state-based prompting
    if conversation_state == "intro":
        return "Hello! I'm an AI academic advisor for UH Mānoa. Do you already know what major you want to pursue?"

    if conversation_state == "awaiting_major":
        return "Great. What major are you thinking about?"

    if conversation_state == "awaiting_interests":
        return "No problem. What are your current interests? I can help match them to a UH Mānoa major."

    # normal advising mode
    context = ""
    if detected_major:
        context = build_context_for_major(detected_major)

    full_prompt = f"""
    {base_rules}

    User input:
    {user_input}

    Relevant UH Mānoa courses:
    {context}

    Provide a four-year course plan using as many relevant major courses as possible.
    Respond in plain text.
    """
    return full_prompt


import json

@csrf_exempt
def gemini_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user_input = data.get("prompt", "")  # match the key your JS uses

    # initialize session state if needed
    if "conversation_state" not in request.session:
        request.session["conversation_state"] = "intro"

    state = request.session["conversation_state"]
    detected_major = request.session.get("detected_major", None)

    # --- STATE MACHINE LOGIC ---

    if state == "intro":
        if user_input.strip() == "":
            response_text = build_prompt("", "intro")
            return JsonResponse({"response": response_text})

        user_lower = user_input.lower()
        if "yes" in user_lower:
            request.session["conversation_state"] = "awaiting_major"
            return JsonResponse({"response": build_prompt("", "awaiting_major")})

        if "no" in user_lower:
            request.session["conversation_state"] = "awaiting_interests"
            return JsonResponse({"response": build_prompt("", "awaiting_interests")})

        return JsonResponse({"response": "Hello! I am an AI academic advisor for UH Manoa. Before we get started, do you already know what you want to major in?"})

    if state == "awaiting_major":
        detected_major = user_input
        request.session["detected_major"] = detected_major
        request.session["conversation_state"] = "normal"

    if state == "awaiting_interests":
        interests = user_input.lower()
        matched_major = None
        for key in major_prefix_map.keys():
            if any(word in key for word in interests.split()):
                matched_major = key
                break

        if matched_major is None:
            return JsonResponse({"response": "Thanks. Can you describe your interests in a bit more detail so I can match them to a major?"})

        detected_major = matched_major
        request.session["detected_major"] = detected_major
        request.session["conversation_state"] = "normal"

    # normal state
    prompt = build_prompt(user_input, "normal", detected_major)
    result = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    response_text = result.text

    return JsonResponse({"response": response_text})



    return JsonResponse({"response": response_text})
