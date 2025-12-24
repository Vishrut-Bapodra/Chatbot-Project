import os, requests, re, json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

# --------------------------------------------------------------
# MODEL NAME (easy to change)
# --------------------------------------------------------------
MODEL_NAME = "openai/gpt-oss-120b"
# --------------------------------------------------------------


# --------------------------------------------------------------
# LIST OF MODELS THAT SUPPORT TOOLS
# --------------------------------------------------------------
TOOL_MODELS = {
    "openai/gpt-oss-120b",
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "openai/gpt-4.1",
    "openai/gpt-4.1-mini",
    "anthropic/claude-3",
    "anthropic/claude-3.5",
}

def model_supports_tools(model: str) -> bool:
    model = model.lower()
    for m in TOOL_MODELS:
        if m in model:
            return True
    return False


# --------------------------------------------------------------
# CLEAN MODEL OUTPUT
# --------------------------------------------------------------
def clean_model_output(text):
    patterns = [
        r"<s>", r"</s>",
        r"\[OUT\]", r"\[/OUT\]",
        r"\[INST\]", r"\[/INST\]",
        r"^\s*[\[\<].*function.*\].*$",
    ]
    out = text
    for p in patterns:
        out = re.sub(p, "", out, flags=re.DOTALL | re.IGNORECASE)
    return out.strip()


# --------------------------------------------------------------
# WEB SEARCH
# --------------------------------------------------------------
def web_search(query: str):
    if not SERPER_KEY:
        return {"summary": "Web search unavailable."}

    try:
        r = requests.post(
            "https://google.serper.dev/search",
            json={"q": query},
            headers={"X-API-KEY": SERPER_KEY},
            timeout=15
        )
        data = r.json()
    except Exception as e:
        return {"summary": f"Search error: {str(e)}"}

    organic = data.get("organic", [])
    summary = ""

    for item in organic[:3]:
        summary += f"• {item.get('title','')}\n  {item.get('snippet','')}\n\n"

    if not summary.strip():
        summary = "No results found."

    return {"summary": summary}

# --------------------------------------------------------------
# SAFE JSON LOAD
# --------------------------------------------------------------
def safe_json_loads(text):
    try:
        return json.loads(text)
    except:
        try:
            cleaned = re.sub(r"(\w+):", r'"\1":', text)
            cleaned = cleaned.replace("'", '"')
            return json.loads(cleaned)
        except:
            return {"query": text}


# --------------------------------------------------------------
# OPENROUTER CALL
# --------------------------------------------------------------
def call_openrouter(messages, model, tools=None, tool_choice=None):
    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
    }

    if tools:
        payload["tools"] = tools
    if tool_choice:
        payload["tool_choice"] = tool_choice

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    try:
        return response.json()
    except:
        return {}


# --------------------------------------------------------------
# MAIN CHATBOT LOGIC (AUTO-TOOL DETECTION)
# --------------------------------------------------------------
def get_chatbot_response(messages, model=MODEL_NAME):

    if not API_KEY:
        return "Missing API key."

    # -------- AUTO-TOOL DETECTION --------
    supports_tools = model_supports_tools(model)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web.",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"]
                }
            }
        }
    ] if supports_tools else None

    tool_choice = "auto" if supports_tools else None
    # -------------------------------------

    # FIRST CALL
    initial = call_openrouter(messages, model, tools=tools, tool_choice=tool_choice)

    if "choices" not in initial or len(initial["choices"]) == 0:
        return "Unable to respond."

    msg = initial["choices"][0]["message"]

    # TOOL CALL LOGIC (ONLY IF SUPPORTED)
    if supports_tools and msg.get("tool_calls"):
        tool_call = msg["tool_calls"][0]
        fn_name = tool_call["function"]["name"]
        raw_args = tool_call["function"]["arguments"]

        args = safe_json_loads(raw_args)

        if fn_name == "web_search":
            findings = web_search(args.get("query", ""))

            follow_messages = messages + [
                msg,
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": findings["summary"],
                }
            ]

            final = call_openrouter(follow_messages, model)
            return clean_model_output(final["choices"][0]["message"]["content"])

    # --------------------------------------------------------------

    # NORMAL OUTPUT
    if "content" in msg:
        return clean_model_output(msg["content"])

    return "I'm having trouble responding."
