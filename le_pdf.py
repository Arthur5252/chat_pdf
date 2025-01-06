import PyPDF2

def ler_pdf(caminho_pdf):
    texto = ""
    with open(caminho_pdf, "rb") as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        for pagina in leitor_pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto