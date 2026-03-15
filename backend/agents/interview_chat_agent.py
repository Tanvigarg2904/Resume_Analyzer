from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def interview_chat_agent(role, skills, resume_text, chat_history, message):

    system_prompt = f"""
You are a professional technical interviewer.

Target Role: {role}

Candidate Skills:
{skills}

Candidate Resume:
{resume_text}

Your behavior:
- Conduct a realistic technical interview
- Ask thoughtful interview questions
- Evaluate candidate answers briefly
- Ask follow-up questions
- If candidate asks something, answer it
- Keep conversation natural like ChatGPT
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    for msg in chat_history:
        messages.append(msg)

    messages.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content