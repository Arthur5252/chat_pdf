import random
import py_eureka_client.eureka_client as eureka_client

def init_eureka():
    # Gera uma porta aleatória entre 1024 e 65535
    random_port = random.randint(1024, 65535)

    # Inicialize o cliente Eureka com as configurações especificadas
    eureka_client.init(
        eureka_server="http://eureka.octopustax.com.br/eureka",
        app_name="chat-bot-service",  # Substitua pelo nome do seu serviço
        instance_id=f"chat-bot-service:{random_port}",  # Substitua pelo ID da instância
        instance_host="eureka.octopustax.com.br",
        instance_port=random_port,  # Usa a porta aleatória gerada
        renewal_interval_in_secs=10,
        duration_in_secs=30,
        should_register=True
    )

    return random_port