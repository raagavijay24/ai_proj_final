# 🤖 Agentic AI System  
### Strategic Planning & Tool-Using Autonomous Agent
A real-world **ReAct-style autonomous AI agent** built using **Hugging Face LLM (Llama 3.1 8B Instruct)**.

This system is not a basic chatbot — it is a **goal-driven reasoning agent** capable of planning, tool usage, structured decision-making, and persistent memory.

---

## ✨ Core Capabilities

- 🧠 **Mission Planning** – Generates a structured 5-step execution plan  
- 🔎 **Web Search** – Fetches real-time information using DuckDuckGo  
- 🧮 **Mathematical Computation** – Safely evaluates expressions  
- 💾 **Persistent Memory** – Stores and recalls past goals and outputs  
- 🔁 **Multi-Step Reasoning** – Implements a strict ReAct execution loop  

---

## 🧩 Strategic Supervisor Architecture

The system follows a structured orchestration workflow:

1. Plan the mission  
2. Select the appropriate tool  
3. Execute reasoning steps  
4. Observe tool results  
5. Produce a clean final answer  
6. Store the result in memory  

---

# 🚀 Demo Capabilities

## 1️⃣ General Knowledge & Web Intelligence

Uses the **SEARCH** tool to retrieve live information.

### Workflow
User Query → Planning → Tool Selection → Web Search → Reasoning → Final Answer
## 2️⃣ Mathematical Reasoning

Uses a secure math evaluation engine.

### Workflow
User Query → Planning → Tool Selection → MATH → Observation → Final Answer

## 🏗️ Architecture Overview

User Input
↓
Planning Module
↓
Tool Selection Module
↓
ReAct Agent Loop (Max 6 Steps)
↓
Tool Execution
↓
Memory Logging
↓
Clean Final Output

# 📂 Project Structure

📦 Agentic-System
├── agent.py # Main autonomous agent loop
├── smtg.env # Environment file (API key)
├── agent_memory.txt # Persistent memory log
├── requirements.txt
└── README.md

# ⚙️ Setup Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
## 2️⃣ Install Dependencies
```bash
pip install huggingface_hub python-dotenv ddgs
```
## 3️⃣ Configure Environment

Create a file named:

```bash
smtg.env
```
Add your Hugging Face API key:

```bash
HF_API_KEY=your_huggingface_api_key_here
```
## 4️⃣ Run the System

```bash
python agent.py
```

**🛠️ Tech Stack**

Python 3.9+

Hugging Face Inference API

Llama 3.1 8B Instruct

DDGS (DuckDuckGo Search)

python-dotenv

Regex-based action parsing
