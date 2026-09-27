import qrcode

# Cole a URL do seu site no Render aqui
url_do_site = "https://ingressos-igreja.onrender.com" 

# Cria o QR Code
img = qrcode.make(url_do_site)

# Salva como imagem
img.save("meu_qrcode.png")
print("QR Code gerado com sucesso!")