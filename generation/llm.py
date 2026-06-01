import requests

def build_prompt(question, chunks):
    
    context = ""

    for chunk in chunks:
        context+=chunk["text"] + '\n\n'

    prompt = f"""
You are a helpful model which gives answer based on the provided context

Context: {context}
Question: {question}
"""
        
    return prompt

def generate(question, chunks):

    url = "http://localhost:11434/api/generate"

    prompt = build_prompt(question, chunks)

    response = requests.post(url, json = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    print(response.json()["response"])

    return