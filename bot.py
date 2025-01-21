from openai import OpenAI
from le_pdf import *
import time

def perguntar_ao_chatbot(pergunta,contexto):
    cliente=OpenAI(api_key= "Chave API aqui")
    modelo = "gpt-4o-mini"
    maximo_tentativas = 1
    repeticao = 0
    while True:
        try:
            prompt_do_sistema = f"""
            Você é um assistente que responde perguntas com base em um PDF.
            use o contexto abaixo para responder as perguntas.
            {contexto}
            """
            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": pergunta
                    }
                ],
                temperature= 0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo
            )
            return response.choices[0].message.content
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no GPT: %s" % erro
            time.sleep(1)