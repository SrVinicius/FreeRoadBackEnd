#!/bin/bash
# Script de inicialização para o Render

echo "=== INICIANDO APLICAÇÃO NO RENDER ==="
echo "Verificando ambiente..."

# Verifica se a variável DATABASE_URL está definida
if [ -z "$DATABASE_URL" ]; then
    echo "AVISO: DATABASE_URL não está definida!"
else
    echo "DATABASE_URL encontrada (ocultando por segurança)"
fi

# Adiciona prefixo à DATABASE_URL se necessário
if [[ "$DATABASE_URL" == *"postgresql://"* ]] && [[ "$DATABASE_URL" != *"postgresql+asyncpg://"* ]]; then
    echo "Convertendo DATABASE_URL para formato asyncpg..."
    export DATABASE_URL=${DATABASE_URL/postgresql:\/\//postgresql+asyncpg:\/\/}
    echo "Formato corrigido!"
fi

# Instala dependências
echo "Instalando dependências..."
pip install -U pip
pip install -r requirements.txt

# Executa migrações do banco de dados
echo "Executando migrações do banco de dados..."
if command -v alembic &> /dev/null; then
    alembic upgrade head
else
    echo "AVISO: Alembic não encontrado, pulando migrações."
fi

# Inicia a aplicação
echo "Iniciando aplicação..."
echo "Comando: uvicorn freeroad.api.main:app --host 0.0.0.0 --port $PORT"
exec uvicorn freeroad.api.main:app --host 0.0.0.0 --port $PORT
