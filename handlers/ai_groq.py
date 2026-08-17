from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY != "YOUR_GROQ_API_KEY" else None

async def generate_ai_quiz(topic: str, num_questions: int = 5):
    if not client:
        return None
    
    prompt = f"Generate a JSON list of {num_questions} quiz questions on topic '{topic}'. Format: [{{\"question\": \"...\", \"options\": [\"A\", \"B\", \"C\", \"D\"], \"correct_index\": 0}}]"
    
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    
    return completion.choices[0].message.content
  
