from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta # <-- Nova importação para lidar com data e hora

app = Flask(__name__)

# Coloque aqui a URL que o SheetDB gerou para você
SHEETDB_URL = "https://sheetdb.io/api/v1/0pq8m9lx5a0d9"

EVENTOS = {
    "face_a_face": {
        "id": "face_a_face",
        "nome": "Face a Face com Deus 2026",
        "preco_display": "R$ 50,00",
        "banner": "/static/face_a_face.jpeg", 
        "pix_copia_cola": "00020126360014br.gov.bcb.pix011462955505245275520400005303986540550.005802BR5925IGREJA DO EVANGELHO QUADR6008CONTAGEM62070503***6304E139",
        "tem_camisa": True # <--- ATIVAMOS A CAMISA PARA ESTE EVENTO
    },
    "ieq_fit": {
        "id": "ieq_fit",
        "nome": "IEQ Fit",
        "preco_display": "R$ 50,00",
        "banner": "/static/ieq_fit.jpeg",
        "pix_copia_cola": "00020126360014br.gov.bcb.pix011462955505245275520400005303986540550.005802BR5925IGREJA DO EVANGELHO QUADR6008CONTAGEM62070503***6304E139",
        "tem_camisa": False # <--- Desativado
    }
}

@app.route('/')
def index():
    return render_template('index.html', eventos=EVENTOS.values())

@app.route('/inscricao/<id_evento>', methods=['GET', 'POST'])
def inscricao(id_evento):
    evento_escolhido = EVENTOS.get(id_evento)
    if not evento_escolhido:
        return "Evento não encontrado", 404

    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        telefone = request.form.get('telefone')
        
        # Captura o tamanho da camisa. Se o evento não tiver camisa, envia um traço "-"
        tamanho_camisa = request.form.get('tamanho_camisa', '-')

        agora_brasil = datetime.utcnow() - timedelta(hours=3)
        data_hora_formatada = agora_brasil.strftime("%d/%m/%Y %H:%M:%S") 

        payload = {
            "data": {
                "Nome": nome,
                "Sobrenome": sobrenome,
                "Telefone": telefone,
                "Evento": evento_escolhido['nome'],
                "Data_Hora": data_hora_formatada,
                "Tamanho_Camisa": tamanho_camisa # <--- Nova coluna mapeada
            }
        }
        try:
            requests.post(SHEETDB_URL, json=payload)
        except Exception as e:
            print("Erro ao salvar na planilha:", e)

        whatsapp_igreja = "5531991809494" 
        return render_template('evento.html', evento=evento_escolhido, whatsapp=whatsapp_igreja, nome=nome, telefone=telefone)

    return render_template('inscricao.html', evento=evento_escolhido)

if __name__ == '__main__':
    app.run(debug=True)