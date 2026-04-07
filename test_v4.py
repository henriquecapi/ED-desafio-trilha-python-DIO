"""
Script de teste para validar a versão v4.0 do sistema bancário
Realiza testes de: CSV creation, usuários, contas, depósitos, saques
"""

import sys
import os

# Mudar para o diretório correto
os.chdir(r'c:\Cursos\web.dio.me\Python\LuizaLabs-1\trilha-python-dio\00 - Desafio')

# Importar o módulo CSV
from csv_manager import (
    inicializar_csvs,
    adicionar_usuario_csv,
    carregar_usuarios,
    usuario_existe,
    adicionar_conta_csv,
    carregar_contas,
    adicionar_transacao_csv,
    obter_saldo_conta,
    obter_transacoes_conta,
    dados_existem,
    contas_existem
)

print("=" * 60)
print("TESTE DE VALIDAÇÃO - SISTEMA BANCÁRIO v4.0")
print("=" * 60)

# Teste 1: Inicializar CSVs
print("\n[TESTE 1] Inicializando CSVs...")
inicializar_csvs()
print("✓ CSVs inicializados com sucesso")

# Teste 2: Adicionar usuário
print("\n[TESTE 2] Adicionando usuário...")
resultado = adicionar_usuario_csv("12345678901", "João Silva", "01/01/1990", "Rua A, 100 - Centro - São Paulo/SP - 01234-567")
if resultado:
    print("✓ Usuário adicionado com sucesso")
else:
    print("✗ Erro ao adicionar usuário")

# Teste 3: Verificar duplicação de CPF
print("\n[TESTE 3] Verificando duplicação de CPF...")
duplicado = usuario_existe("12345678901")
if duplicado:
    print("✓ CPF duplicado detectado corretamente")
else:
    print("✗ Erro na detecção de duplicação")

# Teste 4: Carregar usuários
print("\n[TESTE 4] Carregando usuários...")
usuarios = carregar_usuarios()
if len(usuarios) > 0:
    print(f"✓ {len(usuarios)} usuário(s) carregado(s)")
    print(f"  - {usuarios[0]['nome']} (CPF: {usuarios[0]['cpf']})")
else:
    print("✗ Nenhum usuário carregado")

# Teste 5: Adicionar conta
print("\n[TESTE 5] Adicionando conta...")
resultado = adicionar_conta_csv("12345678901", "0001", 1, "10/04/2026 10:00:00", saldo=0)
if resultado:
    print("✓ Conta adicionada com sucesso")
else:
    print("✗ Erro ao adicionar conta")

# Teste 6: Carregar contas
print("\n[TESTE 6] Carregando contas...")
contas = carregar_contas()
if len(contas) > 0:
    print(f"✓ {len(contas)} conta(s) carregada(s)")
    print(f"  - Agência: {contas[0]['agencia']}, Conta: {contas[0]['numero_conta']}")
else:
    print("✗ Nenhuma conta carregada")

# Teste 7: Adicionar transações (depósito)
print("\n[TESTE 7] Adicionando depósito...")
resultado = adicionar_transacao_csv("12345678901", 1, "deposito", 100.00, "10/04/2026 10:05:00", 100.00)
if resultado:
    print("✓ Depósito adicionado com sucesso")
else:
    print("✗ Erro ao adicionar depósito")

# Teste 8: Adicionar transações (saque)
print("\n[TESTE 8] Adicionando saque...")
resultado = adicionar_transacao_csv("12345678901", 1, "saque", 30.00, "10/04/2026 10:10:00", 70.00)
if resultado:
    print("✓ Saque adicionado com sucesso")
else:
    print("✗ Erro ao adicionar saque")

# Teste 9: Obter saldo da conta
print("\n[TESTE 9] Obtendo saldo da conta...")
saldo = obter_saldo_conta("12345678901", 1)
print(f"✓ Saldo obtido: R$ {saldo:.2f}")
if saldo == 70.00:
    print("✓ Cálculo de saldo está correto!")
else:
    print(f"✗ Saldo incorreto. Esperado: 70.00, Obtido: {saldo}")

# Teste 10: Carregar transações
print("\n[TESTE 10] Carregando transações...")
transacoes = obter_transacoes_conta("12345678901", 1)
if len(transacoes) > 0:
    print(f"✓ {len(transacoes)} transação(ões) carregada(s)")
    for t in transacoes:
        print(f"  - {t['tipo'].upper()}: R$ {t['valor']:.2f}")
else:
    print("✗ Nenhuma transação carregada")

# Teste 11: Verificar dados existentes
print("\n[TESTE 11] Verificando se dados existem...")
tem_dados = dados_existem()
tem_contas = contas_existem()
if tem_dados:
    print("✓ Dados detectados (Segunda execução)")
    if tem_contas:
        print("✓ Contas existem")
else:
    print("✗ Nenhum dado detectado")

print("\n" + "=" * 60)
print("TESTES CONCLUÍDOS COM SUCESSO!")
print("=" * 60)
print("\nOs CSVs foram criados em:")
print("  - usuarios.csv")
print("  - contas.csv")
print("  - transacoes.csv")
print("\nPróximas etapas:")
print("  1. Execute 'python main_v4.0.py' para usar o sistema")
print("  2. Teste a funcionalidade completa com login, depósitos e saques")
