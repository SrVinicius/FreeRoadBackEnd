#!/usr/bin/env python3
"""
Script de diagnóstico para verificar a conexão com o banco de dados Neon.
Execute este script no ambiente Render para depurar problemas de conexão.

Uso: python debug_db_connection.py
"""

import os
import sys
from urllib.parse import urlparse, parse_qs
import asyncio
import asyncpg

async def test_direct_connection():
    """Testa a conexão direta com o banco de dados usando asyncpg."""
    try:
        # Obter a URL do banco de dados
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            print("ERRO: Variável DATABASE_URL não encontrada!")
            return False
            
        # Ocultar credenciais para o log
        if '@' in database_url:
            scheme = database_url.split('@')[0].split('://')[0]
            remainder = database_url.split('@')[1]
            print(f"Tentando conectar a: {scheme}://*****@{remainder}")
        
        # Analisar a URL
        parsed = urlparse(database_url)
        query_dict = parse_qs(parsed.query)
        
        # Verificar se é PostgreSQL
        if not parsed.scheme.startswith('postgresql'):
            print(f"ERRO: Esquema não suportado: {parsed.scheme}")
            return False
            
        # Extrair os componentes da URL
        user_pass = parsed.netloc.split('@')[0]
        host_port = parsed.netloc.split('@')[1]
        
        username = user_pass.split(':')[0]
        password = user_pass.split(':')[1] if ':' in user_pass else ''
        
        host = host_port.split(':')[0]
        port = int(host_port.split(':')[1]) if ':' in host_port else 5432
        
        database = parsed.path.lstrip('/')
        
        # Configuração SSL para Neon
        ssl = "sslmode" in query_dict and query_dict["sslmode"][0] == "require"
        
        print(f"Tentando conectar a: {host}:{port}/{database} (SSL: {ssl})")
        
        # Tentar conexão
        conn = await asyncpg.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=database,
            ssl=ssl
        )
        
        print("Conexão bem-sucedida!")
        
        # Testar consulta simples
        version = await conn.fetchval("SELECT version()")
        print(f"Versão do PostgreSQL: {version}")
        
        # Fechar conexão
        await conn.close()
        return True
    
    except Exception as e:
        print(f"ERRO na conexão: {str(e)}")
        return False

async def test_sqlalchemy_connection():
    """Testa a conexão usando SQLAlchemy."""
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        
        # Obter a URL do banco de dados
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            print("ERRO: Variável DATABASE_URL não encontrada!")
            return False
            
        print("Testando conexão via SQLAlchemy...")
        
        # Configuração SSL
        connect_args = {}
        if "neon.tech" in database_url:
            connect_args["ssl"] = True
        
        # Criar engine
        engine = create_async_engine(
            database_url,
            echo=True,
            connect_args=connect_args
        )
        
        # Testar conexão
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            print(f"Consulta de teste: {await result.fetchone()}")
            
        print("Conexão SQLAlchemy bem-sucedida!")
        return True
        
    except Exception as e:
        print(f"ERRO na conexão SQLAlchemy: {str(e)}")
        return False

async def main():
    """Função principal."""
    print("=== DIAGNÓSTICO DE CONEXÃO COM BANCO DE DADOS ===")
    print(f"Python version: {sys.version}")
    print(f"Sistema operacional: {os.name}")
    print(f"DATABASE_URL definida: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
    
    print("\n=== TESTE DIRETO COM ASYNCPG ===")
    direct_ok = await test_direct_connection()
    
    print("\n=== TESTE COM SQLALCHEMY ===")
    sqlalchemy_ok = await test_sqlalchemy_connection()
    
    print("\n=== RESULTADO FINAL ===")
    if direct_ok and sqlalchemy_ok:
        print("✅ Ambas as conexões foram bem-sucedidas!")
    elif direct_ok:
        print("⚠️ Apenas a conexão direta foi bem-sucedida. Problema na configuração do SQLAlchemy.")
    elif sqlalchemy_ok:
        print("⚠️ Apenas a conexão SQLAlchemy foi bem-sucedida. Estranho!")
    else:
        print("❌ Ambas as conexões falharam. Verifique a configuração do banco de dados.")

if __name__ == "__main__":
    asyncio.run(main())
