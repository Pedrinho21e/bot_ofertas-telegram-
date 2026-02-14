FROM python:3.10-slim

# Define a pasta onde o bot vai ficar no servidor
WORKDIR /app

# Copia o arquivo de dependências (o requirements.txt)
COPY requirements.txt .

# Instala o que seu bot precisa (biblioteca do Telegram, etc)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o seu código para dentro do servidor
COPY . .

# COMANDO PARA LIGAR: 
# IMPORTANTE: Se o seu arquivo principal NÃO se chamar 'main.py', 
# troque o nome abaixo pelo nome do seu arquivo (ex: bot.py)
CMD ["python", "main.py"]
