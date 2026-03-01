import os
import re
import warnings
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# --- FLEXIBLE IMPORT ---
try:
    from ddgs import DDGS
except ImportError:
    print("❌ Error: Please run 'pip install ddgs'")
    exit()

# ------------------ SETUP ------------------

load_dotenv("smtg.env")
HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    print("❌ ERROR: HF_API_KEY not found in smtg.env")
    exit()

client = InferenceClient(api_key=HF_API_KEY)
MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# ------------------ MEMORY SYSTEM ------------------

MEMORY_FILE = "agent_memory.txt"

# Ensure file exists at startup
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        f.write("=== Agent Memory Log ===\n")

def load_memory(limit=2000):
    if not os.path.exists(MEMORY_FILE):
        return ""
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return content[-limit:]

def save_memory(goal, result):
    full_path = os.path.abspath(MEMORY_FILE)
    print("📂 Saving memory to:", full_path)

    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"\nGoal: {goal}\nResult: {result}\n{'-'*50}\n")

# ------------------ TOOLS ------------------

def web_search(query):
    print(f"  [Tool] Searching: {query}")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No search results found."

        bodies = [r.get('body','') for r in results if isinstance(r, dict)]
        return "\n".join(bodies) if bodies else "No useful results."

    except Exception as e:
        return f"Search Error: {str(e)}"

def math_tool(expression):
    print(f"  [Tool] Calculating: {expression}")
    try:
        clean_expr = expression.replace("x", "*").replace("^", "**")
        return str(eval(clean_expr, {"__builtins__": {}}))
    except Exception as e:
        return f"Math Error: {str(e)}"

# ------------------ LLM CALL ------------------

def call_llm(prompt, system_role):
    try:
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
        response = client.chat_completion(
            model=MODEL,
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"

# ------------------ TOOL SELECTOR ------------------

def select_tool(goal):
    decision_prompt = f"""
Goal: {goal}

Available Tools:
- SEARCH
- MATH
- NONE

Respond with ONLY one word.
"""
    decision = call_llm(decision_prompt, "You are a Tool Selector.")
    return decision.strip().upper()

# ------------------ PLANNING ------------------

def run_planning_workflow(goal):
    print("  [System] Planning...")
    plan = call_llm(f"Plan 5 steps for: {goal}", "You are a Planner.")
    return plan

# ------------------ MAIN AGENT LOOP ------------------

def agent_loop(user_input):

    print("\n[Phase 1] Planning...")
    mission_plan = run_planning_workflow(user_input)

    print("\n[Phase 2] Tool Selection...")
    selected_tool = select_tool(user_input)
    print("Selected Tool:", selected_tool)

    past_memory = load_memory()

    system_role = f"""
You are a Strategic AI Agent.
Today is March 1, 2026.

PAST MEMORY:
{past_memory}

MISSION PLAN:
{mission_plan}

STRICT FORMAT:
Thought: reasoning
Action: TOOL_NAME(input)

Available Tools:
SEARCH
MATH
FINAL_ANSWER

You MUST end with:
Action: FINAL_ANSWER(answer)
"""

    context = f"Goal: {user_input}"
    all_observations = []

    for step in range(6):

        response = call_llm(context, system_role)
        print(f"\n--- Step {step+1} ---\n{response}")

        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", response, re.I)

        if not action_match:
            context += "\nObservation: Invalid format. Use Action: TOOL(input)"
            continue

        tool = action_match.group(1).upper()
        value = action_match.group(2)

        # ------------------ FINAL ANSWER (UPDATED CLEAN VERSION) ------------------
        if tool == "FINAL_ANSWER":

            clean_value = value

            # Remove answer= if model adds it
            clean_value = re.sub(r'^answer\s*=\s*', '', clean_value, flags=re.I)

            # Remove surrounding quotes
            clean_value = clean_value.strip()
            if (clean_value.startswith('"') and clean_value.endswith('"')) or \
               (clean_value.startswith("'") and clean_value.endswith("'")):
                clean_value = clean_value[1:-1]

            save_memory(user_input, clean_value)
            return clean_value

        # ------------------ SEARCH TOOL ------------------
        elif tool == "SEARCH":
            observation = web_search(value)

        # ------------------ MATH TOOL ------------------
        elif tool == "MATH":
            observation = math_tool(value)

        else:
            observation = f"Unknown tool: {tool}"

        print("   [Observation]:", observation[:150])
        all_observations.append(observation)

        context += f"\n{response}\nObservation: {observation}"

    # ------------------ FALLBACK ------------------

    print("\n[Fallback] Generating final answer...")

    final = call_llm(
        f"Answer the goal clearly: {user_input}\nObservations: {all_observations}",
        "You are a final answer generator."
    )

    save_memory(user_input, final)
    return final

# ------------------ MAIN ------------------

if __name__ == "__main__":

    print("\n🚀 Agentic System v5.1 (Clean Output Version)")
    print("="*45)

    while True:
        task = input("\nEnter Goal: ")

        if task.lower() in ["exit", "quit"]:
            break

        if not task.strip():
            continue

        result = agent_loop(task)
        print("\n✅ FINAL RESULT:\n", result)
        print("-"*100)