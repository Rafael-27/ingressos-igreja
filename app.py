from flask import Flask, render_template

app = Flask(__name__)

# Nosso "Banco de Dados" em memória. 
# IMPORTANTE: Gere os códigos PIX Copia e Cola no app do seu banco com os valores exatos e substitua abaixo.
EVENTOS = {
    "face_a_face": {
        "id": "face_a_face",
        "nome": "Face a Face com Deus",
        "preco_display": "R$ 50,00",
        "banner": "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=500", # Troque pela URL da arte do evento
        "pix_copia_cola": "00020126580014br.gov.bcb.pix01360543c85d-5d00-4244-ba94-e2c0cf8feea2520400005303986540550.005802BR5925RAFAEL DOUGLAS FERNANDES 6014BELO HORIZONTE62070503***630462CF"
    },
    "casais": {
        "id": "casais",
        "nome": "Encontro de Casais",
        "preco_display": "R$ 50,00",
        "banner": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=500",
        "pix_copia_cola": "COLE_AQUI_O_PIX_ESTATICO_DE_50_REAIS"
    },
    "ieq_fit": {
        "id": "ieq_fit",
        "nome": "IEQ Fit",
        "preco_display": "R$ 50,00",
        "banner": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=500",
        "pix_copia_cola": "COLE_AQUI_O_PIX_ESTATICO_DE_50_REAIS"
    }
}

# Rota Principal: Lista os eventos
@app.route('/')
def index():
    return render_template('index.html', eventos=EVENTOS.values())

# Rota de Pagamento: Mostra o PIX específico do evento escolhido
@app.route('/evento/<id_evento>')
def evento(id_evento):
    evento_escolhido = EVENTOS.get(id_evento)
    if not evento_escolhido:
        return "Evento não encontrado", 404
    
    # Número do WhatsApp da igreja (apenas números, com código do país 55)
    whatsapp_igreja = "5511999999999" 
    
    return render_template('evento.html', evento=evento_escolhido, whatsapp=whatsapp_igreja)

if __name__ == '__main__':
    app.run(debug=True)