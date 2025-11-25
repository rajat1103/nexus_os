import os
from groq import Groq

def get_llm_response(query, context):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    system_prompt = f"""
    You are NEXUS, an advanced personal intelligence OS.
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say you don't know.
    
    Context:
    {context}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content