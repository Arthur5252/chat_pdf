from flask import Flask, request, render_template, session, jsonify
from le_pdf import *
from bot import *
import os

app = Flask(__name__)

# Variável global para armazenar o último caminho do arquivo processado
ultimo_arquivo = None

@app.route("/montar_caminho", methods=["POST"])
def montar_caminho():
    global ultimo_arquivo  # Para acessar e modificar a variável global
    try:
        # Verifica se os dados estão no formato JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({"erro": "Requisição inválida. Envie um JSON válido."}), 400

        # Campos obrigatórios para montar o caminho
        required_fields = ['filename', 'rootpaste', 'clientefolder', 'workbook', 'subworkbook']
        for field in required_fields:
            if field not in json_data or not json_data[field]:
                return jsonify({"erro": f"O campo '{field}' é obrigatório e não pode estar vazio."}), 400

        # Captura os dados do JSON
        filename = json_data['filename']
        rootpaste = json_data['rootpaste']
        clientfolder = json_data['clientefolder']
        workbook = json_data['workbook']
        subworkbook = json_data['subworkbook']

        # Monta o caminho do novo arquivo
        monta_caminho = os.path.join(rootpaste, clientfolder, workbook, subworkbook, filename)

        # Se houver um arquivo processado anteriormente, apaga-o
        if ultimo_arquivo and os.path.exists(ultimo_arquivo):
            os.remove(ultimo_arquivo)

        # Atualiza o último arquivo processado
        ultimo_arquivo = monta_caminho

        # Retorna o caminho montado
        return jsonify({"caminho": monta_caminho})

    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}), 500


# Endpoint para interação com o chatbot
@app.route("/chatPDF", methods=["POST"])
def chatbot():
    try:
        # Verifica se os dados estão no formato JSON
        json_data = request.get_json()
        if not json_data:
            return jsonify({"erro": "Requisição inválida. Envie um JSON válido."}), 400

        # Campos obrigatórios para o chatbot
        required_fields = ['caminho', 'msg']
        for field in required_fields:
            if field not in json_data or not json_data[field]:
                return jsonify({"erro": f"O campo '{field}' é obrigatório e não pode estar vazio."}), 400

        # Captura os dados do JSON
        caminho = json_data['caminho']
        prompt = json_data['msg']

        # Verifica se o caminho do arquivo existe
        if not os.path.exists(caminho):
            return jsonify({"erro": f"O arquivo '{caminho}' não foi encontrado."}), 404

        # Lê o conteúdo do PDF
        contexto = ler_pdf(caminho)

        # Valida se o conteúdo do PDF foi extraído
        if not contexto:
            return jsonify({"erro": "Falha ao ler o conteúdo do PDF. Verifique o arquivo."}), 500

        # Pergunta ao chatbot com o contexto extraído
        resposta_chatbot = perguntar_ao_chatbot(prompt, contexto)

        # Retorna a resposta do chatbot
        response_data = {
            "resposta_gpt": resposta_chatbot.replace("\n", "")
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}), 500
