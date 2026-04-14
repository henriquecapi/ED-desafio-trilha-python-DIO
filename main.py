"""
SISTEMA BANCÁRIO PYTHON v4.0 - COM PERSISTÊNCIA DE DADOS EM CSV
Implementa carregamento e salvamento de dados em arquivos CSV
"""

import re
import sys
import textwrap
from abc import ABC, abstractmethod
from datetime import date, datetime
from functools import wraps
from pathlib import Path

from models import (
    Cliente,
    PessoaFisica,
    Conta,
    ContaCorrente,
    Historico,
    Transacao,
    Saque,
    Deposito,
)

# Adiciona o diretório do script ao sys.path para permitir importações locais
# quando o script é executado a partir da raiz do projeto.
file_path = Path(__file__).resolve().parent
if str(file_path) not in sys.path:
    sys.path.append(str(file_path))

from csv_manager import (
    adicionar_conta_csv,
    adicionar_transacao_csv,
    adicionar_usuario_csv,
    atualizar_saldo_conta,
    carregar_contas_objetos,
    carregar_usuarios_objetos,
    inicializar_csvs,
)


# ================== DECORADOR DE LOG ==================
def log_transacao(tipo_transacao):
    """
    Decorador que registra (printa) a data, hora e tipo de transação.
    """

    def decorador(funcao):
        @wraps(funcao)
        def envoltorio(*args, **kwargs):
            agora = datetime.now()
            data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
            print(f"\n[LOG] {data_hora} - Transação: {tipo_transacao}")
            resultado = funcao(*args, **kwargs)

            with open("log_transacoes.txt", "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(
                    f"[{data_hora}] Função '{funcao.__name__}' executada com argumentos {args} e {kwargs}. "
                    f"Retornou {resultado}\n"
                )

            return resultado

        return envoltorio

    return decorador


# ================== ITERADOR DE CONTAS ==================
class ContaIterador:
    """
    Iterador personalizado que permite iterar sobre todas as contas do banco,
    retornando informações básicas de cada conta.
    """

    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self.contas):
            raise StopIteration

        conta = self.contas[self._index]
        self._index += 1

        return {
            "agencia": conta.agencia,
            "numero": conta.numero,
            "titular": conta.cliente.nome,
            "saldo": conta.saldo,
        }


# ================== GERADOR DE RELATÓRIOS ==================
def gerar_relatorio_transacoes(conta, tipo_filtro=None):
    """
    Gerador que permite iterar sobre as transações de uma conta.
    Retorna uma a uma as transações realizadas.
    """
    transacoes = conta.historico.transacoes

    for transacao in transacoes:
        if tipo_filtro is None or transacao["tipo"].lower() == tipo_filtro.lower():
            yield transacao


# ================== VALIDAÇÕES ==================
def validar_cpf(cpf):
    """
    Valida um CPF seguindo as regras brasileiras.
    Verifica se o CPF possui 11 dígitos e valida os dígitos verificadores.
    """
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto

    if int(cpf[9]) != primeiro_digito:
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    segundo_digito = 0 if resto < 2 else 11 - resto

    if int(cpf[10]) != segundo_digito:
        return False

    return True


def normalizar_endereco(endereco):
    """
    Normaliza e valida o endereço, aceitando CEP com ou sem ponto.
    Retorna o endereço normalizado com CEP sem ponto.
    """
    if not endereco or not isinstance(endereco, str):
        return None

    endereco = endereco.strip()
    partes = [p.strip() for p in endereco.split(" - ")]

    if len(partes) < 3:
        return None

    parte1 = partes[0]
    if "," not in parte1:
        return None
    logradouro_numero = parte1.split(",", 1)
    logradouro = logradouro_numero[0].strip()
    numero = logradouro_numero[1].strip()

    if not numero.isdigit():
        return None

    bairro = partes[1].strip()
    if not bairro:
        return None

    ultima_parte = " - ".join(partes[2:])

    if " - " not in ultima_parte:
        return None

    partes_cep = ultima_parte.rsplit(" - ", 1)
    cidade_uf = partes_cep[0].strip()
    cep_str = partes_cep[1].strip()

    if "/" not in cidade_uf:
        return None

    cidade_uf_partes = cidade_uf.rsplit("/", 1)
    cidade = cidade_uf_partes[0].strip()
    uf = cidade_uf_partes[1].strip()

    if len(uf) != 2 or not uf.isupper():
        uf = uf.upper()
        if len(uf) != 2 or not uf.isalpha():
            return None

    cep_limpo = re.sub(r"[^0-9\-]", "", cep_str)

    if not re.match(r"^\d{5}-\d{3}$", cep_limpo):
        return None

    endereco_normalizado = (
        f"{logradouro}, {numero} - {bairro} - {cidade}/{uf} - {cep_limpo}"
    )

    return endereco_normalizado


def validar_endereco(endereco):
    """Valida o endereço no formato especificado."""
    return normalizar_endereco(endereco) is not None


# ================== MENUS ==================
def menu_primeira_execucao():
    """Menu para primeira execução (sem usuários/contas)."""
    menu_text = """\n
    ================ MENU (Primeira Execução) ================
    [nu]     Novo usuário
    [nc]     Nova conta (após criar usuário)
    [qt]     Sair
    => """
    return input(textwrap.dedent(menu_text))


def menu_dados_existentes():
    """Menu após dados existirem (login disponível)."""
    menu_text = """\n
    ================ MENU ================
    [lg]     Login na conta
    [de]     Depositar
    [sa]     Sacar
    [ex]     Extrato
    [nc]     Nova conta
    [lc]     Listar contas
    [lu]     Listar usuários com contas
    [rel]    Relatório de transações
    [it]     Iterador de contas
    [nu]     Novo usuário
    [lt]     Ver Log de Transações (Arquivo)
    [qt]     Sair
    => """
    return input(textwrap.dedent(menu_text))


# ================== OPERAÇÕES COM USUÁRIOS ==================
def novo_usuario(usuarios):
    """Cria um novo usuário com validação de CPF e endereço."""
    cpf = input("Informe o CPF (somente números): ")
    cpf = re.sub(r"\D", "", cpf)

    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return False

    if any(u.cpf == cpf for u in usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return False

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
    endereco = input(
        "Informe o endereço (logradouro, numero - bairro - cidade/uf - CEP): "
    )

    endereco_normalizado = normalizar_endereco(endereco)
    if not endereco_normalizado:
        print("\n@@@ Endereço em formato inválido! @@@")
        return False

    usuario = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco_normalizado
    )
    usuarios.append(usuario)

    if adicionar_usuario_csv(cpf, nome, data_nascimento, endereco_normalizado):
        print("\n=== Usuário criado com sucesso! ===")
        print(f"Nome: {nome}")
        print(f"CPF: {cpf}")
        return True
    else:
        print("\n@@@ Erro ao salvar usuário! @@@")
        return False


# ================== OPERAÇÕES COM CONTAS ==================
def nova_conta(usuarios, contas):
    """Cria uma nova conta vinculada a um usuário existente."""
    if not usuarios:
        print(
            "\n@@@ Nenhum usuário cadastrado! Crie um usuário antes de criar uma conta. @@@"
        )
        return None

    cpf = input("Informe o CPF do usuário: ")
    cpf = re.sub(r"\D", "", cpf)

    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! @@@")
        return None

    numero_conta = len(contas) + 1
    # ContaCorrente encapsula Agencia, Limite e Limite_Saques
    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
    contas.append(conta)
    usuario.adicionar_conta(conta)

    data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if adicionar_conta_csv(
        cpf, conta.agencia, conta.numero, data_criacao, saldo=conta.saldo
    ):
        print("\n=== Conta criada com sucesso! ===")
        print(f"Titular: {usuario.nome}")
        print(f"Agência: {conta.agencia}")
        print(f"Número da Conta: {conta.numero}")

        return {"usuario": usuario, "conta": conta}
    else:
        print("\n@@@ Erro ao salvar conta! @@@")
        return None


# ================== OPERAÇÕES BANCÁRIAS ==================
def realizar_deposito(usuarios):
    """Interface de usuário para depósito."""
    cpf = input("Informe o CPF do cliente: ")
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not usuario.contas:
        print("\n@@@ O usuário não possui contas! @@@")
        return

    if len(usuario.contas) > 1:
        print("\nEscolha a conta:")
        for i, c in enumerate(usuario.contas, 1):
            print(f"{i}. Agência: {c.agencia} | Conta: {c.numero}")
        idx = int(input("=> ")) - 1
        conta = usuario.contas[idx]
    else:
        conta = usuario.contas[0]

    try:
        valor = float(input("Informe o valor do depósito: R$ "))

        @log_transacao("DEPÓSITO")
        def depositar(cpf, numero_conta, valor):
            """Função interna decorada para bater com o padrão de log do usuário."""
            transacao = Deposito(valor)
            usuario.realizar_transacao(conta, transacao)

            # Persistência
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            adicionar_transacao_csv(
                usuario.cpf, conta.numero, "deposito", valor, agora, conta.saldo
            )
            atualizar_saldo_conta(usuario.cpf, str(conta.numero), conta.saldo)
            return True

        depositar(usuario.cpf, str(conta.numero), valor)

    except ValueError:
        print("\n@@@ Valor inválido! @@@")


def realizar_saque(usuarios):
    """Interface de usuário para saque."""
    cpf = input("Informe o CPF do cliente: ")
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not usuario.contas:
        print("\n@@@ O usuário não possui contas! @@@")
        return

    if len(usuario.contas) > 1:
        print("\nEscolha a conta:")
        for i, c in enumerate(usuario.contas, 1):
            print(f"{i}. Agência: {c.agencia} | Conta: {c.numero}")
        idx = int(input("=> ")) - 1
        conta = usuario.contas[idx]
    else:
        conta = usuario.contas[0]

    try:
        valor = float(input("Informe o valor do saque: R$ "))

        # Obter limites da conta corrente (se for o caso)
        limite = getattr(conta, "limite", 500)
        limite_saques = getattr(conta, "limite_saques", 3)

        @log_transacao("SAQUE")
        def sacar(cpf, numero_conta, valor, limite, limite_saques):
            """Função interna decorada para bater com o padrão de log do usuário."""
            transacao = Saque(valor)
            saldo_anterior = conta.saldo
            usuario.realizar_transacao(conta, transacao)

            # Se o saldo mudou, a transação foi bem sucedida
            if conta.saldo < saldo_anterior:
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                adicionar_transacao_csv(
                    usuario.cpf, conta.numero, "saque", valor, agora, conta.saldo
                )
                atualizar_saldo_conta(usuario.cpf, str(conta.numero), conta.saldo)
                return True
            return False

        sacar(usuario.cpf, str(conta.numero), valor, limite, limite_saques)

    except ValueError:
        print("\n@@@ Valor inválido! @@@")


# ================== VISUALIZAÇÕES ==================
def exibir_extrato(usuarios):
    """Exibe o extrato da conta de um cliente de forma OO."""
    cpf = input("Informe o CPF do cliente: ")
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not usuario.contas:
        print("\n@@@ O usuário não possui contas! @@@")
        return

    if len(usuario.contas) > 1:
        print("\nEscolha a conta:")
        for i, c in enumerate(usuario.contas, 1):
            print(f"{i}. Agência: {c.agencia} | Conta: {c.numero}")
        idx = int(input("=> ")) - 1
        conta = usuario.contas[idx]
    else:
        conta = usuario.contas[0]

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if transacoes:
        print("\nHistórico detalhado de transações:\n")
        for i, transacao in enumerate(transacoes, 1):
            tipo = transacao["tipo"].upper()
            valor = transacao["valor"]
            data = transacao["data"]
            print(f"{i}. [{data}] {tipo}")
            print(f"   Valor: R$ {valor:.2f}\n")
    else:
        print("Nenhuma transação realizada.")

    print(f"\nSaldo Atual:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def exibir_relatorio(usuarios):
    """
    Exibe relatório de transações usando o gerador.
    """
    cpf = input("Informe o CPF do cliente: ")
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not usuario.contas:
        print("\n@@@ O usuário não possui contas! @@@")
        return

    if len(usuario.contas) > 1:
        print("\nEscolha a conta:")
        for i, c in enumerate(usuario.contas, 1):
            print(f"{i}. Agência: {c.agencia} | Conta: {c.numero}")
        idx = int(input("=> ")) - 1
        conta = usuario.contas[idx]
    else:
        conta = usuario.contas[0]

    transacoes = conta.historico.transacoes

    if not transacoes:
        print("\n@@@ Nenhuma transação registrada nesta conta! @@@")
        return

    print("\n================ RELATÓRIO DE TRANSAÇÕES ================")
    print(f"Conta: {conta.numero} | CPF: {usuario.cpf}")
    print("\n[1] Todas as transações")
    print("[2] Apenas depósitos")
    print("[3] Apenas saques")

    opcao = input("\nEscolha uma opção: ")

    filtro = None
    if opcao == "2":
        filtro = "Deposito"
        print("\n--- DEPÓSITOS ---\n")
    elif opcao == "3":
        filtro = "Saque"
        print("\n--- SAQUES ---\n")
    else:
        print("\n--- TODAS AS TRANSAÇÕES ---\n")

    encontrou = False
    for i, transacao in enumerate(gerar_relatorio_transacoes(conta, filtro), 1):
        encontrou = True
        tipo = transacao["tipo"].upper()
        valor = transacao["valor"]
        data = transacao["data"]

        print(f"{i}. [{data}] {tipo}")
        print(f"   Valor: R$ {valor:.2f}\n")

    if not encontrou:
        print("Nenhuma transação encontrada com o filtro selecionado.")

    print("=" * 55)


def listar_contas(contas):
    """Lista todas as contas criadas com informações do titular (OO)."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    print("\n================ CONTAS ================")
    for conta in contas:
        print(f"\nAgência: {conta.agencia}")
        print(f"Número da Conta: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")
        print(f"Saldo: R$ {conta.saldo:.2f}")
        print("-" * 40)
    print("==========================================")


def listar_usuarios_com_contas(usuarios):
    """Lista todos os usuários com suas contas relacionadas (OO)."""
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! @@@")
        return

    print("\n================ USUÁRIOS E CONTAS =================")
    for usuario in usuarios:
        print(f"\n--- Usuário ---")
        print(f"Nome: {usuario.nome}")
        print(f"CPF: {usuario.cpf}")
        print(f"Data de Nascimento: {usuario.data_nascimento}")
        print(f"Endereço: {usuario.endereco}")

        if usuario.contas:
            print(f"\n  Contas ({len(usuario.contas)}):")
            for conta in usuario.contas:
                print(
                    f"    - Agência: {conta.agencia} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}"
                )
        else:
            print(f"\n  Contas: Nenhuma conta cadastrada")

        print("-" * 50)
    print("===================================================")


def exibir_iterador_contas(contas):
    """Usa o iterador personalizado ContaIterador para exibir as contas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    print("\n================ ITERADOR DE CONTAS BANCÁRIAS ================")

    iterador = ContaIterador(contas)

    for i, info_conta in enumerate(iterador, 1):
        print(f"\n{i}. Conta #{info_conta['numero']}")
        print(f"   Agência: {info_conta['agencia']}")
        print(f"   Titular: {info_conta['titular']}")
        print(f"   Saldo Atual: R$ {info_conta['saldo']:.2f}")
        print("-" * 60)

    print("=" * 60)


def exibir_log_transacoes():
    """Lê e exibe o conteúdo do arquivo log_transacoes.txt."""
    caminho_log = "log_transacoes.txt"
    if not Path(caminho_log).exists():
        print("\n@@@ Arquivo de log não encontrado! @@@")
        return

    print("\n================ LOG DE TRANSAÇÕES (ARQUIVO) ================")
    try:
        with open(caminho_log, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readlines()
            if not conteudo:
                print("Arquivo de log está vazio.")
            else:
                # Mostrar as últimas 20 linhas para não inundar o terminal
                for linha in conteudo[-20:]:
                    print(linha.strip())
    except Exception as e:
        print(f"@@@ Erro ao ler o log: {e} @@@")
    print("=============================================================")


def login_conta(usuarios):
    """
    Realiza login por conta de forma OO.
    """
    cpf = input("Informe o CPF: ")
    cpf = re.sub(r"\D", "", cpf)

    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! @@@")
        return None

    if not usuario.contas:
        print(f"\n@@@ O usuário {usuario.nome} não possui contas! @@@")
        return None

    print(f"\n=== Bem-vindo, {usuario.nome}! ===")
    print("\nSuas contas:")

    for i, conta in enumerate(usuario.contas, 1):
        print(
            f"{i}. Agência: {conta.agencia} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}"
        )

    while True:
        try:
            opcao = int(input("\nSelecione a ordem da conta para acessar: "))
            if 1 <= opcao <= len(usuario.contas):
                conta_selecionada = usuario.contas[opcao - 1]
                return {
                    "usuario": usuario,
                    "conta": conta_selecionada,
                }
            else:
                print("@@@ Opção inválida! @@@")
        except ValueError:
            print("Digite um número válido!")


# ================== EXIBIÇÃO DA CONTA ATIVA ==================
def exibir_conta_ativa(conta_ativa):
    """
    Exibe as informações da conta ativa com data/hora (OO).
    """
    if not conta_ativa:
        return

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    usuario_nome = conta_ativa["usuario"].nome
    numero_conta = conta_ativa["conta"].numero

    print(f"\n[{agora}] {usuario_nome} - Conta: {numero_conta}")


# ================== FUNÇÃO PRINCIPAL ==================
def main():
    """Função principal que executa o loop do programa (Versão OO v5.0)."""
    # Inicializar CSVs
    inicializar_csvs()

    # Carregar dados iniciais do CSV como objetos
    usuarios = carregar_usuarios_objetos()
    contas = carregar_contas_objetos(usuarios)

    print("\n" + "=" * 50)
    print("SISTEMA BANCÁRIO PYTHON v5.0 (OOP)")
    print("Herança, Polimorfismo e Persistência CSV")
    print("=" * 50)

    conta_ativa = None

    while True:
        exibir_conta_ativa(conta_ativa)

        if not usuarios:
            opcao = menu_primeira_execucao()
        else:
            opcao = menu_dados_existentes()

        if opcao == "nu":
            novo_usuario(usuarios)

        elif opcao == "nc":
            resultado = nova_conta(usuarios, contas)
            if resultado:
                conta_ativa = resultado

        elif opcao == "lg":
            if not contas:
                print("\n@@@ Nenhuma conta cadastrada! Crie uma conta primeiro. @@@")
                continue

            login = login_conta(usuarios)
            if login:
                conta_ativa = login
                print("\n✓ Login realizado com sucesso!")

        elif opcao == "de":
            realizar_deposito(usuarios)

        elif opcao == "sa":
            realizar_saque(usuarios)

        elif opcao == "ex":
            exibir_extrato(usuarios)

        elif opcao == "rel":
            exibir_relatorio(usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios_com_contas(usuarios)

        elif opcao == "it":
            exibir_iterador_contas(contas)

        elif opcao == "lt":
            exibir_log_transacoes()

        elif opcao == "qt":
            print("\n" + "=" * 50)
            print("Obrigado por usar nosso banco. Até logo!")
            print("=" * 50 + "\n")
            break

        else:
            print("\n@@@ Operação inválida. Tente novamente! @@@")


if __name__ == "__main__":
    main()
