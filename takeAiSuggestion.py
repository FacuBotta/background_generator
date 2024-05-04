import ollama
import random

def give_tip(interests):
    random_topic = random.choice(interests)
    prompt_title = f"Ask me a question to test my knowledge in {random_topic}. Just ask the question, do not add extra text."

    title_response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt_title,
        },
    ])

    
    if title_response['message']['content']:
      prompt_text = f"{title_response['message']['content']}. Your response should be a maximum of 300 characters including spaces."
      text_response = ollama.chat(model='llama3', messages=[
          {
              'role': 'user',
              'content': prompt_text,
              'temperature': 0,
          },
      ])

    if title_response and text_response:
        result = {'title': title_response['message']['content'], 'text': text_response['message']['content'], 'topic': random_topic}
    else:
        result = {'title': 'Ups!', 'text': "Sorry! I can't help you today", 'topic': ''}

    return result
