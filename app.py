from flask import Flask, render_template, request
import requests # Nova biblioteca para enviar dados para a planilha

app = Flask(__name__)

# Coloque aqui a URL que o SheetDB gerou para você
SHEETDB_URL = "https://sheetdb.io/api/v1/0pq8m9lx5a0d9"

EVENTOS = {
    "face_a_face": {
        "id": "face_a_face",
        "nome": "Face a Face com Deus 2026",
        "preco_display": "R$ 50,00",
        "banner": "/static/face_a_face.jpeg", 
        "pix_copia_cola": "00020126360014br.gov.bcb.pix011462955505245275520400005303986540550.005802BR5925IGREJA DO EVANGELHO QUADR6008CONTAGEM62070503***6304E139"
    },
    "ieq_fit": {
        "id": "ieq_fit",
        "nome": "Ieq Fit",
        "preco_display": "R$ 35,00",
        "banner": "/static/ieq_fit.jpeg",
        "pix_copia_cola": "00020126360014br.gov.bcb.pix011462955505245275520400005303986540550.005802BR5925IGREJA DO EVANGELHO QUADR6008CONTAGEM62070503***6304E139"
    }
}

@app.route('/')
def index():
    return render_template('index.html', eventos=EVENTOS.values())

# NOVA ROTA: Formulário de Inscrição
@app.route('/inscricao/<id_evento>', methods=['GET', 'POST'])
def inscricao(id_evento):
    evento_escolhido = EVENTOS.get(id_evento)
    if not evento_escolhido:
        return "Evento não encontrado", 404

    # Se o usuário preencheu e enviou o formulário
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        telefone = request.form.get('telefone')

        # Envia os dados para a planilha do Google via SheetDB
        payload = {
            "data": {
                "Nome": nome,
                "Sobrenome": sobrenome,
                "Telefone": telefone,
                "Evento": evento_escolhido['nome']
            }
        }
        try:
            requests.post(SHEETDB_URL, json=payload)
        except Exception as e:
            print("Erro ao salvar na planilha:", e)
            # Num MVP, não vamos travar o usuário se a planilha falhar. Ele segue pro pagamento.

        # Passamos os dados do usuário para a página de pagamento (para o botão do WhatsApp)
        whatsapp_igreja = "5511999999999" 
        return render_template('evento.html', evento=evento_escolhido, whatsapp=whatsapp_igreja, nome=nome, telefone=telefone)

    # Se for requisição GET (apenas acessando o link), mostra o formulário vazio
    return render_template('inscricao.html', evento=evento_escolhido)

if __name__ == '__main__':
    app.run(debug=True)