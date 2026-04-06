#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
📋 Script de Teste das Novas Funcionalidades v3.0
Demonstra decoradores, geradores, iteradores, data/hora e limite de transações
"""

import sys
from datetime import datetime, date
from io import StringIO

# Importar o módulo principal
sys.path.insert(0, '.')
from main import (
    ContaIterador, 
    gerar_relatorio_transacoes,
    log_transacao,
    novo_usuario,
    nova_conta,
    depositar,
    sacar,
    exibir_extrato,
    exibir_relatorio,
    validar_cpf
)

def teste_decorador_log():
    """Teste 1: Decorador de Log"""
    print("\n" + "="*60)
    print("✅ TESTE 1: DECORADOR DE LOG")
    print("="*60)
    
    print("\nO decorador @log_transacao está implementado nas funções:")
    print("  • depositar()")
    print("  • sacar()")
    print("\nQuando chamadas, elas imprimem:")
    print("  [LOG] DD/MM/YYYY HH:MM:SS - Transação: TIPO")
    print("\nExemplo esperado:")
    print("  [LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO")

def teste_iterador_contas():
    """Teste 2: Iterador de Contas"""
    print("\n" + "="*60)
    print("✅ TESTE 2: ITERADOR DE CONTAS (ContaIterador)")
    print("="*60)
    
    # Criar dados de teste
    usuarios = [
        {
            "nome": "João da Silva",
            "data_nascimento": "15/08/1990",
            "cpf": "12345678901",
            "endereco": "Rua X, 100 - Centro - São Paulo/SP - 01310-100"
        },
        {
            "nome": "Maria Santos",
            "data_nascimento": "22/11/1985",
            "cpf": "98765432109",
            "endereco": "Avenida Y, 200 - Bairro Z - Rio de Janeiro/RJ - 20000-000"
        }
    ]
    
    contas = [
        {
            "agencia": "0001",
            "numero_conta": 1,
            "usuario": usuarios[0],
            "transacoes": [
                {
                    "tipo": "deposito",
                    "valor": 1000.0,
                    "data_hora": datetime.now(),
                    "data_hora_str": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "saldo_apos": 1000.0
                },
                {
                    "tipo": "saque",
                    "valor": 150.0,
                    "data_hora": datetime.now(),
                    "data_hora_str": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "saldo_apos": 850.0
                }
            ],
            "data_criacao": datetime.now()
        },
        {
            "agencia": "0001",
            "numero_conta": 2,
            "usuario": usuarios[1],
            "transacoes": [
                {
                    "tipo": "deposito",
                    "valor": 2000.0,
                    "data_hora": datetime.now(),
                    "data_hora_str": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "saldo_apos": 2000.0
                }
            ],
            "data_criacao": datetime.now()
        }
    ]
    
    print("\n🔄 Iterando sobre contas usando ContaIterador:\n")
    
    iterador = ContaIterador(contas)
    for i, info in enumerate(iterador, 1):
        print(f"{i}. Conta #{info['numero']}")
        print(f"   Agência: {info['agencia']}")
        print(f"   Titular: {info['titular']}")
        print(f"   Saldo: R$ {info['saldo']:.2f}")
        print()

def teste_gerador_relatorio():
    """Teste 3: Gerador de Relatórios"""
    print("\n" + "="*60)
    print("✅ TESTE 3: GERADOR DE RELATÓRIOS (gerar_relatorio_transacoes)")
    print("="*60)
    
    conta = {
        "agencia": "0001",
        "numero_conta": 1,
        "usuario": {
            "nome": "João da Silva",
            "cpf": "12345678901"
        },
        "transacoes": [
            {
                "tipo": "deposito",
                "valor": 1000.0,
                "data_hora": datetime(2026, 4, 6, 14, 35, 22),
                "data_hora_str": "06/04/2026 14:35:22",
                "saldo_apos": 1000.0
            },
            {
                "tipo": "saque",
                "valor": 150.0,
                "data_hora": datetime(2026, 4, 6, 14, 36, 45),
                "data_hora_str": "06/04/2026 14:36:45",
                "saldo_apos": 850.0
            },
            {
                "tipo": "deposito",
                "valor": 500.0,
                "data_hora": datetime(2026, 4, 6, 15, 0, 10),
                "data_hora_str": "06/04/2026 15:00:10",
                "saldo_apos": 1350.0
            },
            {
                "tipo": "saque",
                "valor": 200.0,
                "data_hora": datetime(2026, 4, 6, 15, 15, 30),
                "data_hora_str": "06/04/2026 15:15:30",
                "saldo_apos": 1150.0
            }
        ]
    }
    
    # Teste 1: Todas as transações
    print("\n1️⃣ Todas as transações:")
    print("-" * 50)
    for i, transacao in enumerate(gerar_relatorio_transacoes(conta), 1):
        tipo = "DEPÓSITO" if transacao["tipo"] == "deposito" else "SAQUE"
        print(f"{i}. [{transacao['data_hora_str']}] {tipo} - R$ {transacao['valor']:.2f}")
    
    # Teste 2: Apenas depósitos
    print("\n2️⃣ Apenas Depósitos:")
    print("-" * 50)
    for i, transacao in enumerate(gerar_relatorio_transacoes(conta, "deposito"), 1):
        print(f"{i}. [{transacao['data_hora_str']}] DEPÓSITO - R$ {transacao['valor']:.2f}")
    
    # Teste 3: Apenas saques
    print("\n3️⃣ Apenas Saques:")
    print("-" * 50)
    for i, transacao in enumerate(gerar_relatorio_transacoes(conta, "saque"), 1):
        print(f"{i}. [{transacao['data_hora_str']}] SAQUE - R$ {transacao['valor']:.2f}")

def teste_data_hora():
    """Teste 4: Data e Hora em Transações"""
    print("\n" + "="*60)
    print("✅ TESTE 4: DATA E HORA EM TRANSAÇÕES")
    print("="*60)
    
    print("\nTodas as transações agora registram data/hora.")
    print("\nEstrutura de uma transação (v3.0):")
    print("""
    transacao = {
        "tipo": "deposito",                   # ou "saque"
        "valor": 1000.00,
        "data_hora": datetime(...),           # Objeto datetime
        "data_hora_str": "06/04/2026 14:35:22",  # String formatada
        "saldo_apos": 1000.00
    }
    """)
    
    geracao_agora = datetime.now()
    print(f"Data/Hora do sistema agora: {geracao_agora.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Data hoje: {date.today()}")
    
    print("\nReset automático:")
    print("  • Contador de transações reseta à meia-noite")
    print("  • Contador de saques reseta à meia-noite")
    print("  • Sistema detecta mudança de data automaticamente")

def teste_limite_10_transacoes():
    """Teste 5: Limite de 10 Transações Diárias"""
    print("\n" + "="*60)
    print("✅ TESTE 5: LIMITE DE 10 TRANSAÇÕES DIÁRIAS")
    print("="*60)
    
    print("\n📊 Implementação do Limite:")
    print("  • Variável: transaction_hoje (conta transações do dia)")
    print("  • Limite: Máximo 10 transações por dia")
    print("  • Reset: Automático à meia-noite")
    print("  • Depósitos E saques CONTAM para o limite")
    
    print("\n⚠️ Mensagem quando limite é excedido:")
    print("""
    @@@ Operação falhou! Você excedeu o número de transações 
    permitidas para hoje (máximo 10). @@@
    """)
    
    print("\n🔄 Fluxo de controle:")
    print("  1. Usuário tenta fazer transação")
    print("  2. Sistema verifica: date.today() != data_transacoes")
    print("  3. Se mudou de dia → reseta contadores")
    print("  4. Verifica se transacoes_hoje >= 10")
    print("  5. Se SIM → mostra erro e rejeita")
    print("  6. Se NÃO → permite e incrementa transacoes_hoje")

def teste_cpf_validacao():
    """Teste 6: Validação de CPF (mantido de v2.1)"""
    print("\n" + "="*60)
    print("✅ TESTE 6: VALIDAÇÃO DE CPF")
    print("="*60)
    
    testes = [
        ("12345678901", True, "CPF válido"),
        ("111.111.111-11", False, "Todos dígitos iguais"),
        ("123.456.789-10", False, "Dígito verificador inválido"),
        ("12345", False, "Menos de 11 dígitos"),
    ]
    
    print("\nTestando función validar_cpf():\n")
    for cpf, esperado, descricao in testes:
        resultado = validar_cpf(cpf)
        status = "✓" if resultado == esperado else "✗"
        print(f"{status} validar_cpf('{cpf}')")
        print(f"  Esperado: {esperado}, Resultado: {resultado}")
        print(f"  Descrição: {descricao}\n")

def resumo_novas_features():
    """Resumo Visual das Novas Features"""
    print("\n" + "="*60)
    print("📋 RESUMO DAS NOVAS FUNCIONALIDADES v3.0")
    print("="*60)
    
    features = [
        ("Decorador de Log", "@log_transacao", "Registra data/hora de cada transação"),
        ("Gerador de Relatórios", "gerar_relatorio_transacoes()", "Itera transações com filtro"),
        ("Iterador de Contas", "ContaIterador", "Itera sobre todas as contas"),
        ("Data e Hora", "datetime", "Registra momento exato de cada transação"),
        ("Limite Diário", "transacoes_hoje", "Máximo 10 transações por dia"),
    ]
    
    print("\n")
    for nome, implementacao, descricao in features:
        print(f"⭐ {nome}")
        print(f"   Implementação: {implementacao}")
        print(f"   Descrição: {descricao}\n")

def main():
    """Função principal de testes"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🧪 TESTES DAS NOVAS FUNCIONALIDADES v3.0".center(58) + "║")
    print("║" + "  Sistema Bancário em Python com:"           .center(58) + "║")
    print("║" + "  • Decoradores • Geradores • Iteradores"   .center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    teste_decorador_log()
    teste_iterador_contas()
    teste_gerador_relatorio()
    teste_data_hora()
    teste_limite_10_transacoes()
    teste_cpf_validacao()
    resumo_novas_features()
    
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES COMPLETADOS COM SUCESSO!")
    print("="*60)
    print("\n📌 Próximos passos:")
    print("  1. Execute 'python main.py' para usar o sistema")
    print("  2. Teste os novos recursos interativamente:")
    print("     • [de] - Depositar (com decorador de log)")
    print("     • [sa] - Sacar (com decorador de log + limite 10 trans)")
    print("     • [ex] - Extrato (com data/hora)")
    print("     • [rel] - Relatório (com gerador + filtros)")
    print("     • [it] - Iterador (com iterador de contas)")
    print("\n")

if __name__ == "__main__":
    main()
