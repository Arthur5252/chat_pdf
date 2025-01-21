from flask import Flask, request, jsonify
from le_pdf import *
from bot import *
import logging
import os

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename="app.log",  
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    filemode='w'  # 'w' para sobrescrever o log
)

@app.route("/<int:cod_cliente>/chat/pdf/<nome_arquivo>", methods=["POST"])
def chatbot(cod_cliente, nome_arquivo):
    caminho_base = 'C:/inetpub/wwwroot/gpca/octopus/arquivos'

    # Verifica a URL antes de processá-la
    url_recebida = request.url
    logging.info(f"URL recebida: {url_recebida}")

    logging.info(f"Cliente: {cod_cliente}, Arquivo: {nome_arquivo}")

    # Monta o caminho completo para o arquivo
    caminho_arquivo = os.path.join(caminho_base, str(cod_cliente), 'ai', 'pdf', nome_arquivo)
    logging.info(f'caminho_arquivo: {caminho_arquivo}')

    try:
        logging.info("Recebida requisição para interação com o chatbot.")

        # Verifica se os dados estão no formato JSON (no caso de enviar parâmetros adicionais)
        json_data = request.get_json()
        if json_data and 'msg' not in json_data:
            logging.warning("Campo 'msg' ausente no JSON.")
            return jsonify({"erro": "O campo 'msg' é obrigatório."}), 400

        # Caso o corpo da requisição não seja JSON, verificamos se o campo "msg" está como parâmetro de formulário
        prompt = json_data['msg'] if json_data else request.form.get('msg')
        logging.info(f'msg: {prompt}')

        # Verifica se o caminho do arquivo existe
        if not os.path.exists(caminho_arquivo):
            logging.warning(f"Arquivo não encontrado: {caminho_arquivo}")
            return jsonify({"erro": f"O arquivo '{caminho_arquivo}' não foi encontrado."}), 404

        # Lê o conteúdo do PDF
        contexto = ler_pdf(caminho_arquivo)

        # Valida se o conteúdo do PDF foi extraído
        if not contexto:
            logging.error(f"Falha ao ler o conteúdo do arquivo: {caminho_arquivo}")
            return jsonify({"erro": "Falha ao ler o conteúdo do PDF. Verifique o arquivo."}), 500

        # Pergunta ao chatbot com o contexto extraído
        resposta_chatbot = perguntar_ao_chatbot(prompt, contexto)

        # Retorna a resposta do chatbot
        msg = {
            "msg": resposta_chatbot.replace("\n", "")
        }
        logging.info(f"Resposta do chatbot enviada com sucesso.")
        return jsonify(msg)

    except Exception as e:
        logging.error(f"Erro ao processar interação com o chatbot: {str(e)}", exc_info=True)
        return jsonify({"erro": f"Ocorreu um erro inesperado: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)