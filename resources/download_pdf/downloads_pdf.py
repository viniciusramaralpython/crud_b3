import os
import requests
import urllib3
import base64
import xml.etree.ElementTree as ET


#=================================================================
#=================================================================
#Aqui tentamos suprimir os avisos de SSL.
#Por fim, acabamos ignorando o SSL no request mesmo.
#=================================================================
#=================================================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



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
    
    # Parsear a string XML
    try:
        xml_tree = ET.ElementTree(ET.fromstring(decoded_string))
        xml_str = ET.tostring(xml_tree.getroot(), encoding='unicode')
        return xml_str
    except ET.ParseError as e:
        print(f"Erro ao parsear XML: {e}")
        return None
    



#=================================================================
#=================================================================
#Função para baixar os arquivos e retornar o resultado
#=================================================================
#=================================================================

def fetch_example_data(idCategoriaDocumento, idTipoDocumento, idEspecieDocumento, dataInicial, dataFinal, s):
    '''
    idCategoriaDocumento - Informe qual a categoria de documento que deseja baixar, lembrando que aqui é o índice que consta na busca.
    idTipoDocumento - Informe qual a categoria de documento que deseja baixar, lembrando que aqui é o índice que consta na busca.
    idEspecieDocumento - Informe qual a espécie de documento que deseja baixar, lembrando que aqui é o índice que consta na busca.
    dataInicial - dd/mm/aaaa
    dataFinal - dd/mm/aaaa
    s - Significa qual o documento que você quer iniciar a busca. O script sempre pega de 200 em 200.
    '''


    url = "https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados"
    params = {
        'd': 6,
        's': s,
        'l': 200,
        'o[0][dataEntrega]': 'desc',
        'idCategoriaDocumento': idCategoriaDocumento,
        'idTipoDocumento': idTipoDocumento,
        'idEspecieDocumento': idEspecieDocumento,
        'dataInicial': dataInicial,
        'dataFinal': dataFinal
    }
    response = requests.get(url, params=params, verify=False)  # Desabilitar verificação SSL
    response.raise_for_status()  # Levanta um erro se a requisição falhar
    return response.json()



#=================================================================
#=================================================================
#Salvar o XML (base64) para string e salvar em um arquivo
#=================================================================
#=================================================================
def save_xml_string_to_file(xml_string, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xml_string)
        print(f"Arquivo XML salvo em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo XML: {e}")

#=================================================================
#=================================================================
#Salvar o PDF (base64) para string e salvar em um arquivo
#=================================================================
#=================================================================
def base64_to_pdf(base64_string, output_file_path):
    try:
        # Decodificar a string base64
        pdf_data = base64.b64decode(base64_string)
        
        # Escrever os dados decodificados em um arquivo PDF
        with open(output_file_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        
        print(f"PDF salvo em: {output_file_path}")
    except Exception as e:
        print(f"Erro ao converter base64 para PDF: {e}")

#=================================================================
#=================================================================
#Baixar o documento
#=================================================================
#=================================================================

def download_document(doc_id, download_dir):
    download_url = f"https://fnet.bmfbovespa.com.br/fnet/publico/downloadDocumento?id={doc_id}"
    response = requests.get(download_url, verify=False)
    response.raise_for_status()

    # Enviando a solicitação GET
    response = requests.get(download_url, stream=True, verify=False)


    if response.headers.get('Content-Type') == "text/xml":
        myContent = base64_to_xml(response.content)

        file_path = f"documents/{doc_id}.xml"

        save_xml_string_to_file(myContent, file_path)


    else:
      myContent = response.content
      file_path = f"documents/{doc_id}.pdf"
      base64_to_pdf(response.content, file_path)


def main():
    myContinua = True
    myDataInicial = "09/05/2022"
    myDataFinal = "09/05/2022"
    myStartDocument = 0

    while myContinua == True:
      data = fetch_example_data(0, 0, 0, myDataInicial, myDataFinal, myStartDocument)

      if len(data['data']) == 0:
        myContinua = False

      else:
        if 'data' in data:
            results = data['data']
        else:
            results = data  # Adicione toda a resposta se não houver 'data'

        # Diretório para salvar os documentos baixados
        download_dir = "documents"
        os.makedirs(download_dir, exist_ok=True)

        # Fazendo o download dos documentos
        for item in results:
            doc_id = item.get('id')
            if doc_id:
                download_document(doc_id, download_dir)

        myStartDocument += 200

if __name__ == "__main__":
    main()
    
    
    
