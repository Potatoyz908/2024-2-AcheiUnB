# Use a imagem oficial do Python
FROM python:3.12

# Define o diretório de trabalho
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev && apt-get clean

# Copia os arquivos de dependência
COPY API/requirements.txt /app/

# Atualiza o pip antes de instalar os requisitos
RUN python -m pip install --upgrade pip

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . /app/

# Define a porta padrão
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
