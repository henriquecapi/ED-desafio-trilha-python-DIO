"""
Módulo de gerenciamento de persistência de dados em CSV para o Sistema Bancário v4.0
Responsável por: criação, leitura e escrita de arquivos CSV
"""

import csv
import os
import re
from datetime import datetime

from pathlib import Path
from models import PessoaFisica, ContaCorrente

# ================== CAMINHOS DOS ARQUIVOS CSV ==================
# Garante que os arquivos CSV fiquem sempre na mesma pasta que os scripts
BASE_DIR = Path(__file__).resolve().parent
CSV_USUARIOS = BASE_DIR / "usuarios.csv"
CSV_CONTAS = BASE_DIR / "contas.csv"
CSV_TRANSACOES = BASE_DIR / "transacoes.csv"


# ================== INICIALIZAÇÃO DOS ARQUIVOS CSV ==================
def inicializar_csvs():
    """
    Inicializa os arquivos CSV na primeira execução.
    Se não existirem, cria com headers vasios.
    """
    # Criar arquivo usuarios.csv
    if not os.path.exists(CSV_USUARIOS):
        with open(CSV_USUARIOS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["cpf", "nome", "data_nascimento", "endereco"])
        print(f"[INFO] Arquivo {CSV_USUARIOS} criado.")

    # Criar arquivo contas.csv
    if not os.path.exists(CSV_CONTAS):
        with open(CSV_CONTAS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["cpf", "agencia", "numero_conta", "data_criacao", "saldo"])
        print(f"[INFO] Arquivo {CSV_CONTAS} criado.")

    # Criar arquivo transacoes.csv
    if not os.path.exists(CSV_TRANSACOES):
        with open(CSV_TRANSACOES, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["cpf", "numero_conta", "tipo", "valor", "data_hora", "saldo_apos"]
            )
        print(f"[INFO] Arquivo {CSV_TRANSACOES} criado.")


# ================== OPERAÇÕES COM USUÁRIOS ==================
def adicionar_usuario_csv(cpf, nome, data_nascimento, endereco):
    """Adiciona um novo usuário ao arquivo CSV."""
    try:
        with open(CSV_USUARIOS, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([cpf, nome, data_nascimento, endereco])
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao adicionar usuário: {e}")
        return False


def carregar_usuarios():
    """Carrega todos os usuários do arquivo CSV."""
    usuarios = []
    try:
        if os.path.exists(CSV_USUARIOS):
            with open(CSV_USUARIOS, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader is not None:
                    for row in reader:
                        if row["cpf"]:  # Ignorar linhas vazias
                            usuarios.append(
                                {
                                    "cpf": row["cpf"],
                                    "nome": row["nome"],
                                    "data_nascimento": row["data_nascimento"],
                                    "endereco": row["endereco"],
                                }
                            )
    except Exception as e:
        print(f"[ERRO] Erro ao carregar usuários: {e}")

    return usuarios


def carregar_usuarios_objetos():
    """Carrega todos os usuários do arquivo CSV como objetos PessoaFisica."""
    usuarios = []
    try:
        if os.path.exists(CSV_USUARIOS):
            with open(CSV_USUARIOS, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["cpf"]:
                        usuarios.append(
                            PessoaFisica(
                                nome=row["nome"],
                                data_nascimento=row["data_nascimento"],
                                cpf=row["cpf"],
                                endereco=row["endereco"],
                            )
                        )
    except Exception as e:
        print(f"[ERRO] Erro ao carregar usuários: {e}")
    return usuarios


def usuario_existe(cpf):
    """Verifica se um usuário com o CPF informado já existe."""
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False


def obter_usuario(cpf):
    """Obtém um usuário específico pelo CPF."""
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


# ================== OPERAÇÕES COM CONTAS ==================
def adicionar_conta_csv(cpf, agencia, numero_conta, data_criacao, saldo=0):
    """Adiciona uma nova conta ao arquivo CSV."""
    try:
        with open(CSV_CONTAS, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([cpf, agencia, numero_conta, data_criacao, saldo])
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao adicionar conta: {e}")
        return False


def carregar_contas():
    """Carrega todas as contas do arquivo CSV."""
    contas = []
    try:
        if os.path.exists(CSV_CONTAS):
            with open(CSV_CONTAS, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader is not None:
                    for row in reader:
                        if row["cpf"]:  # Ignorar linhas vazias
                            contas.append(
                                {
                                    "cpf": row["cpf"],
                                    "agencia": row["agencia"],
                                    "numero_conta": str(
                                        row["numero_conta"]
                                    ),  # Converter para string
                                    "data_criacao": row["data_criacao"],
                                    "saldo": float(row["saldo"]),
                                }
                            )
    except Exception as e:
        print(f"[ERRO] Erro ao carregar contas: {e}")

    return contas


def carregar_transacoes_objetos():
    """Carrega as transações do CSV."""
    transacoes = []
    try:
        if os.path.exists(CSV_TRANSACOES):
            with open(CSV_TRANSACOES, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["cpf"]:
                        transacoes.append(row)
    except Exception as e:
        print(f"[ERRO] Erro ao carregar transações: {e}")
    return transacoes


def carregar_contas_objetos(usuarios):
    """
    Carrega todas as contas do arquivo CSV como objetos ContaCorrente.
    Vincula cada conta ao seu respectivo usuário e carrega o histórico.
    """
    contas = []
    transacoes_csv = carregar_transacoes_objetos()
    try:
        if os.path.exists(CSV_CONTAS):
            with open(CSV_CONTAS, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["cpf"]:
                        usuario = next(
                            (u for u in usuarios if u.cpf == row["cpf"]), None
                        )
                        if usuario:
                            conta = ContaCorrente(
                                numero=int(row["numero_conta"]),
                                cliente=usuario,
                                limite=500,
                                limite_saques=3,
                            )
                            # Calcular saldo real a partir do histórico de transações
                            saldo_calculado = 0.0
                            for t in transacoes_csv:
                                if (
                                    t["cpf"] == row["cpf"]
                                    and t["numero_conta"] == row["numero_conta"]
                                ):
                                    tipo = t["tipo"].lower()
                                    valor = float(t["valor"])
                                    
                                    if tipo == "deposito":
                                        saldo_calculado += valor
                                    elif tipo == "saque":
                                        saldo_calculado -= valor

                                    # Adicionar ao histórico do objeto
                                    conta.historico.transacoes.append(
                                        {
                                            "tipo": t["tipo"].capitalize(),
                                            "valor": valor,
                                            "data": t["data_hora"],
                                        }
                                    )
                            
                            # Definir o saldo calculado como o saldo inicial do objeto
                            conta._saldo = saldo_calculado

                            contas.append(conta)
                            usuario.adicionar_conta(conta)
    except Exception as e:
        print(f"[ERRO] Erro ao carregar contas: {e}")
    return contas


def obter_contas_do_usuario(cpf):
    """Obtém todas as contas de um usuário específico."""
    contas = carregar_contas()
    contas_usuario = [conta for conta in contas if conta["cpf"] == cpf]
    return contas_usuario


def atualizar_saldo_conta(cpf, numero_conta, novo_saldo):
    """Atualiza o saldo de uma conta específica."""
    try:
        contas = carregar_contas()

        # Encontrar e atualizar a conta
        atualizado = False
        for conta in contas:
            if conta["cpf"] == cpf and conta["numero_conta"] == numero_conta:
                conta["saldo"] = novo_saldo
                atualizado = True
                break

        if not atualizado:
            return False

        # Reescrever o arquivo
        with open(CSV_CONTAS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["cpf", "agencia", "numero_conta", "data_criacao", "saldo"])
            for conta in contas:
                writer.writerow(
                    [
                        conta["cpf"],
                        conta["agencia"],
                        conta["numero_conta"],
                        conta["data_criacao"],
                        conta["saldo"],
                    ]
                )
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao atualizar saldo: {e}")
        return False


# ================== OPERAÇÕES COM TRANSAÇÕES ==================
def adicionar_transacao_csv(cpf, numero_conta, tipo, valor, data_hora, saldo_apos):
    """Adiciona uma nova transação ao arquivo CSV."""
    try:
        with open(CSV_TRANSACOES, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([cpf, numero_conta, tipo, valor, data_hora, saldo_apos])
        return True
    except Exception as e:
        print(f"[ERRO] Erro ao adicionar transação: {e}")
        return False


def carregar_transacoes():
    """Carrega todas as transações do arquivo CSV."""
    transacoes = []
    try:
        if os.path.exists(CSV_TRANSACOES):
            with open(CSV_TRANSACOES, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader is not None:
                    for row in reader:
                        if row["cpf"]:  # Ignorar linhas vazias
                            transacoes.append(
                                {
                                    "cpf": row["cpf"],
                                    "numero_conta": row["numero_conta"],
                                    "tipo": row["tipo"],
                                    "valor": float(row["valor"]),
                                    "data_hora": row["data_hora"],
                                    "saldo_apos": float(row["saldo_apos"]),
                                }
                            )
    except Exception as e:
        print(f"[ERRO] Erro ao carregar transações: {e}")

    return transacoes


def obter_transacoes_conta(cpf, numero_conta):
    """Obtém todas as transações de uma conta específica."""
    transacoes = carregar_transacoes()
    numero_conta_str = str(numero_conta)  # Converter para string
    transacoes_conta = [
        t
        for t in transacoes
        if t["cpf"] == cpf and str(t["numero_conta"]) == numero_conta_str
    ]
    return transacoes_conta


def obter_saldo_conta(cpf, numero_conta):
    """Calcula o saldo atual de uma conta baseado nas transações."""
    transacoes = obter_transacoes_conta(cpf, numero_conta)

    saldo = 0
    for transacao in transacoes:
        if transacao["tipo"] == "deposito":
            saldo += transacao["valor"]
        elif transacao["tipo"] == "saque":
            saldo -= transacao["valor"]

    return saldo


# ================== UTILITÁRIOS ==================
def dados_existem():
    """Verifica se existe algum dado persistido (primeira ou segunda execução)."""
    usuarios = carregar_usuarios()
    return len(usuarios) > 0


def contas_existem():
    """Verifica se existe alguma conta criada."""
    contas = carregar_contas()
    return len(contas) > 0
