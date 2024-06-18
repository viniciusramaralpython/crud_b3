''''
Essa função AWS Lambda recebe arquivos via Request(POST) e salva os arquivos em um repositório FTP.
Este repositório serve para alimentar a consulta do sistema principal.
Para fazer o envio basta fazer um request como post com os seguintes dados

url: https://ys32el2xcqzuke7rhtyiknaota0qqvhf.lambda-url.us-east-1.on.aws/

No body, só enviar o seguinte json
{
  "file": "base64 do arquivo"
  "type": "pdf",
  "filename": "arquivo.pdf"
}

Em file, enviar o arquivo como base64
Em type especificar se é pdf ou xml
Em filename, especificar o nome do arquivo com a extensão
O arquivo sempre será salvo no ftp em uma pasta chamada documents

''''









import json, ftplib, os, io
from ftplib import FTP_TLS
from datetime import datetime, timedelta
import base64
import xml.etree.ElementTree as ET
 
#=================================================================
#=================================================================
#Conversor de base64 para XML
#=================================================================
#=================================================================
def base64_to_xml(base64_string):
    # Decodificar a string base64
    decoded_data = base64.b64decode(base64_string)
    
    # Converter os bytes decodificados para uma string
    decoded_string = decoded_data.decode('utf-8')
    
    return 
    
    # Parsear a string XML
    try:
        return decoded_string
    except ET.ParseError as e:
        return f"Erro ao parsear XML: {e}"


#=================================================================
#=================================================================
#Salvar o PDF (base64) para string e salvar em um arquivo
#=================================================================
#=================================================================
def base64_to_pdf(base64_string):
    try:
        # Decodificar a string base64
        return base64.b64decode(base64_string)
    except Exception as e:
        return f"Erro ao converter base64 para PDF: {e}"

        
#=================================================================
#=================================================================
#Upload de arquivos para FTP
#=================================================================
#=================================================================
def upload_file_from_memory_to_ftp(file_content, ftp_directory, ftp_filename, ftp):
    """
    Envia um arquivo diretamente da memória para uma pasta específica no servidor FTP.

    :param file_content: Conteúdo do arquivo em bytes.
    :param ftp_directory: Caminho da pasta no servidor FTP onde o arquivo será salvo.
    :param ftp_filename: Nome com o qual o arquivo será salvo no servidor FTP.
    """
    # Navegar para a pasta desejada no servidor FTP
    try:
        ftp.cwd(ftp_directory)
    except ftplib.error_perm:
        # Se a pasta não existir, cria-la
        ftp.mkd(ftp_directory)
        ftp.cwd(ftp_directory)

    # Usar um objeto BytesIO para o conteúdo do arquivo em memória
    memory_file = io.BytesIO(file_content)

    # Usar STOR para enviar o arquivo ao servidor FTP
    ftp.storbinary(f'STOR {ftp_filename}', memory_file)
    
    print(f"Arquivo {ftp_filename} enviado para {ftp_directory} no servidor FTP.")




#=================================================================
#=================================================================
#Lambda function
#=================================================================
#=================================================================
def lambda_handler(event, context):
    
    
    myFile = event["file"]
    myType = event["type"]
    myFileName = event["filename"]
    
    if myType == "xml":
        myFile = base64_to_xml(myFile)
    else:
        myFile = base64_to_pdf(myFile)
    
   
    # Configurações do servidor FTP
    ftp_server = 'seu_endereco_ftp'  # Substitua pelo endereço do seu servidor FTP
    ftp_username = '_seu_username'    # Substitua pelo seu nome de usuário FTP
    ftp_password = 'sua_senha'      # Substitua pela sua senha FTP
    
 
    # Conectando-se ao servidor FTP
    ftp = ftplib.FTP(ftp_server)
    ftp.login(user=ftp_username, passwd=ftp_password)


    # Conteúdo do arquivo em memória (pode ser texto ou dados binários)
    file_content = bytes(myFile, encoding='utf-8')
    
    # Diretório no servidor FTP (você pode definir dinamicamente)
    ftp_directory = '/documents/'
    
    # Nome do arquivo no servidor FTP
    ftp_filename = myFileName
    
    # Enviar o arquivo em memória para o servidor FTP
    upload_file_from_memory_to_ftp(file_content, ftp_directory, ftp_filename, ftp)
    
    # Fechar a conexão com o servidor FTP
    ftp.quit()
    
        

    return {
        'statusCode': 200,
        'body': {
            "status": "Arquivo enviado com sucesso",
            "file_name": f"{ftp_filename}",
            "datetime": str(datetime.now()),
            "event": str(event)
        }
        
    }


