from flask import Flask, request, render_template, session
from flask_session import Session
from datetime import timedelta
from openai import OpenAI
from le_pdf import *
import PyPDF2
import time
import os

# O Codigo recebe um arquivo PDF do usuário, extrai todo o texto e guarda em uma variável, esta variável será utilizada como contexto para as respostas do Chatbot. 
# Para que o usuário consiga fazer diversas perguntas ao mesmo PDF estou utilizando o modulo Session do Flask, desta forma eu consigo gerenciar quanto tempo vamos # armazenar o contexto do PDF atual.
# Para realizar outras perguntas a outros arquivos PDF o usuário pode simplesmente fazer o upload de um novo arquivo pdf, desta forma nos subescrevemos o contexto # antigo e substituimos pelo contexto novo do novo pdf.

app = Flask(__name__)
app.secret_key = 'octopus'
app.config['SESSION_TYPE'] = 'filesystem' # Define o tipo de armazenamento da sessão, pode ser alterado para escalar a aplicação
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) # Define o tempo de duração da sessão
Session(app) # inicia a sessão

#cliente=OpenAI(api_key= "Chave API aqui")
modelo = "gpt-4o-mini"

def perguntar_ao_chatbot(pergunta,contexto):
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

@app.route("/", methods=["GET", "POST"])
def index():
    resposta_chatbot = ""
    nome_arquivo_pdf = ""

    # Primeiro, verifica se um PDF foi carregado
    if request.method == "POST":
        print("PDF foi carregado.")
        if 'pdf_file' in request.files:  # Verifica se um arquivo PDF foi enviado
            print("PDF foi enviado.")
            arquivo = request.files["pdf_file"]
            print(arquivo)
            if arquivo and arquivo.filename.endswith('.pdf'):
                caminho_pdf = f"./uploads/{arquivo.filename}"
                arquivo.save(caminho_pdf)

                # Lê o PDF e armazena o texto na sessão
                contexto = ler_pdf(caminho_pdf)
                session['contexto'] = contexto  # Armazena o novo contexto na sessão
                session['nome_arquivo'] = arquivo.filename  # Atualiza o nome do arquivo na sessão
                #os.remove(caminho_pdf)
                resposta_chatbot = "PDF carregado com sucesso! Você pode fazer suas perguntas."

        elif request.form.get("pergunta"):  # Se uma pergunta foi feita
            pergunta = request.form.get("pergunta")  # Recebe a pergunta do usuário
            
           
            # Verifica se já temos um contexto e uma pergunta para fazer
            if "contexto" in session and pergunta:
                resposta_chatbot = perguntar_ao_chatbot(pergunta, session['contexto'])  # Obtém a resposta

    # Verifica se o nome do arquivo está na sessão
    if "nome_arquivo" in session:
        nome_arquivo_pdf = session['nome_arquivo']
    return render_template("index.html", resposta=resposta_chatbot, nome_arquivo=nome_arquivo_pdf)

