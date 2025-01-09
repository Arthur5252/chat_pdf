from app import app
from eureka_setup import init_eureka

if __name__ == "__main__":
    port = init_eureka()
    app.run(host='0.0.0.0', port=port)
    print(f"Serviço registrado no Eureka na porta {port}!")
