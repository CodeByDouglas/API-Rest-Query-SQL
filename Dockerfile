# Usando a imagem oficial do Python como base
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /diretorioDocker

# Copiar os arquivos de dependências para o container
COPY requirements.txt /diretorioDocker/requirements.txt

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt


# Expor a porta usada pela aplicação Flask
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "run.py"]