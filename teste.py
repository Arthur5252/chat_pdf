json_data = {
                    "filename":"xxxx.pdf",
                    "rootpaste":"C:\\inetpub\\wwwroot\\gpca\\octopus\\arquivos",
                    "clientfolder":"93",
                    "workbook":"ai",
                    "subworkbook":"pdf" 
            }

filename=json_data['filename']
rootpaste=json_data['rootpaste']
clientfolder=json_data['clientfolder']
workbook= json_data['workbook']
subworkbook=json_data['subworkbook']

monta_caminho = f"{rootpaste}\\{clientfolder}\\{workbook}\\{subworkbook}\\{filename}"
print(monta_caminho)