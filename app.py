from flask import Flask, request, jsonify
from le_pdf import *
from bot import *
import logging
import os


app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename="app.log",  
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    filemode='w'  # 'w' para sobrescrever o log
)


@app.route("/cod_client/chat/pdf/nome_arquivo", methods=["POST"])
def chatbot():
    caminho_base = 'C:\inetpub\wwwroot\gpca\octopus\arquivos\93\ai\pdf'
    cod_cliente = json_data['cod_cliente']
    nome_arquivo = json_data['nome_arquivo']
    try:
        logging.info("Recebida requisição para interação com o chatbot.")

        # Verifica se os dados estão no formato JSON
        json_data = request.get_json()
        if not json_data:
            logging.warning("Requisição inválida: JSON não enviado.")
            return jsonify({"erro": "Requisição inválida. Envie um JSON válido."}), 400

        # Campos obrigatórios para o chatbot
        required_fields = ['caminho', 'msg']
        for field in required_fields:
            if field not in json_data or not json_data[field]:
                logging.warning(f"Campo obrigatório '{field}' ausente ou vazio.")
                return jsonify({"erro": f"O campo '{field}' é obrigatório e não pode estar vazio."}), 400

        # Captura os dados do JSON
        caminho = json_data['caminho']
        prompt = json_data['msg']

        # Verifica se o caminho do arquivo existe
        if not os.path.exists(caminho):
            logging.warning(f"Arquivo não encontrado: {caminho}")
            return jsonify({"erro": f"O arquivo '{caminho}' não foi encontrado."}), 404

        # Lê o conteúdo do PDF
        contexto = ler_pdf(caminho)

        # Valida se o conteúdo do PDF foi extraído
        if not contexto:
            logging.error(f"Falha ao ler o conteúdo do arquivo: {caminho}")
            return jsonify({"erro": "Falha ao ler o conteúdo do PDF. Verifique o arquivo."}), 500

        # Pergunta ao chatbot com o contexto extraído
        resposta_chatbot = perguntar_ao_chatbot(prompt, contexto)

        # Retorna a resposta do chatbot
        response_data = {
            "resposta_gpt": resposta_chatbot.replace("\n", "")
        }
        logging.info(f"Resposta do chatbot enviada com sucesso.")
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"Erro ao processar interação com o chatbot: {str(e)}", exc_info=True)
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
