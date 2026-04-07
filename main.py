"""
SISTEMA BANCÁRIO PYTHON v4.0 - COM PERSISTÊNCIA DE DADOS EM CSV
Implementa carregamento e salvamento de dados em arquivos CSV
"""

import textwrap
import re
from datetime import datetime, date
from functools import wraps
from csv_manager import (
    inicializar_csvs, 
    adicionar_usuario_csv, 
    carregar_usuarios,
    usuario_existe,
    obter_usuario,
    adicionar_conta_csv,
    carregar_contas,
    obter_contas_do_usuario,
    atualizar_saldo_conta,
    adicionar_transacao_csv,
    obter_transacoes_conta,
    obter_saldo_conta,
    dados_existem,
    contas_existem
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
        
        # Calcular saldo da conta
        saldo_conta = obter_saldo_conta(conta['cpf'], conta['numero_conta'])
        
        return {
            "agencia": conta['agencia'],
            "numero": conta['numero_conta'],
            "titular": obter_usuario(conta['cpf'])['nome'],
            "saldo": saldo_conta
        }

# ================== GERADOR DE RELATÓRIOS ==================
def gerar_relatorio_transacoes(cpf, numero_conta, tipo_filtro=None):
    """
    Gerador que permite iterar sobre as transações de uma conta.
    Retorna uma a uma as transações realizadas.
    """
    transacoes = obter_transacoes_conta(cpf, numero_conta)
    
    for transacao in transacoes:
        if tipo_filtro is None or transacao['tipo'] == tipo_filtro:
            yield transacao

# ================== VALIDAÇÕES ==================
def validar_cpf(cpf):
    """
    Valida um CPF seguindo as regras brasileiras.
    Verifica se o CPF possui 11 dígitos e valida os dígitos verificadores.
    """
    cpf = re.sub(r'\D', '', cpf)
    
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
    if ',' not in parte1:
        return None
    logradouro_numero = parte1.split(',', 1)
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
    
    if '/' not in cidade_uf:
        return None
    
    cidade_uf_partes = cidade_uf.rsplit('/', 1)
    cidade = cidade_uf_partes[0].strip()
    uf = cidade_uf_partes[1].strip()
    
    if len(uf) != 2 or not uf.isupper():
        uf = uf.upper()
        if len(uf) != 2 or not uf.isalpha():
            return None
    
    cep_limpo = re.sub(r'[^0-9\-]', '', cep_str)
    
    if not re.match(r'^\d{5}-\d{3}$', cep_limpo):
        return None
    
    endereco_normalizado = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf} - {cep_limpo}"
    
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
    [qt]     Sair
    => """
    return input(textwrap.dedent(menu_text))

# ================== OPERAÇÕES COM USUÁRIOS ==================
def novo_usuario():
    """Cria um novo usuário com validação de CPF e endereço."""
    cpf = input("Informe o CPF (somente números): ")
    cpf = re.sub(r'\D', '', cpf)
    
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return False
    
    if usuario_existe(cpf):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return False
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/uf - CEP): ")
    
    endereco_normalizado = normalizar_endereco(endereco)
    if not endereco_normalizado:
        print("\n@@@ Endereço em formato inválido! @@@")
        print("Exemplos válidos:")
        print("  - Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63113-420")
        print("  - Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63.113-420 (com ponto)")
        print("Certifique-se de:")
        print("  ✓ Rua/avenida, número")
        print("  ✓ Bairro")
        print("  ✓ Cidade/UF (2 letras maiúsculas)")
        print("  ✓ CEP no formato XXXXX-XXX ou XXXXX.XXX")
        return False
    
    if adicionar_usuario_csv(cpf, nome, data_nascimento, endereco_normalizado):
        print("\n=== Usuário criado com sucesso! ===")
        print(f"Nome: {nome}")
        print(f"CPF: {cpf}")
        return True
    else:
        print("\n@@@ Erro ao salvar usuário! @@@")
        return False

# ================== OPERAÇÕES COM CONTAS ==================
def nova_conta(agencia):
    """Cria uma nova conta vinculada a um usuário existente."""
    usuarios = carregar_usuarios()
    
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! Crie um usuário antes de criar uma conta. @@@")
        return None
    
    cpf = input("Informe o CPF do usuário: ")
    cpf = re.sub(r'\s+', '', cpf)
    cpf = re.sub(r'\D', '', cpf)
    
    if not cpf or len(cpf) != 11:
        print("\n@@@ CPF inválido! Deve conter 11 dígitos. @@@")
        return None
    
    usuario = obter_usuario(cpf)
    
    if not usuario:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! @@@")
        print("\nUsários cadastrados:")
        for u in usuarios:
            print(f"  - {u['nome']} (CPF: {u['cpf']})")
        return None
    
    # Descobrir próximo número de conta
    contas = carregar_contas()
    numero_conta = len(contas) + 1
    data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    if adicionar_conta_csv(cpf, agencia, numero_conta, data_criacao, saldo=0):
        print("\n=== Conta criada com sucesso! ===")
        print(f"Titular: {usuario['nome']}")
        print(f"Agência: {agencia}")
        print(f"Número da Conta: {numero_conta}")
        
        # Retornar estrutura completa igual a login_conta()
        conta_criada = {
            'cpf': cpf,
            'agencia': agencia,
            'numero_conta': numero_conta,
            'data_criacao': data_criacao,
            'saldo': 0
        }
        
        return {
            'cpf': cpf,
            'usuario': usuario,
            'conta': conta_criada,
            'numero_conta': numero_conta
        }
    else:
        print("\n@@@ Erro ao salvar conta! @@@")
        return None

# ================== OPERAÇÕES BANCÁRIAS ==================
@log_transacao("DEPÓSITO")
def depositar(cpf, numero_conta, valor):
    """Realiza um depósito na conta."""
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False
    
    # Obter saldo atual
    saldo = obter_saldo_conta(cpf, numero_conta)
    novo_saldo = saldo + valor
    
    # Adicionar transação
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
    
    if adicionar_transacao_csv(cpf, numero_conta, "deposito", valor, data_hora, novo_saldo):
        print("\n=== Depósito realizado com sucesso! ===")
        print(f"Valor: R$ {valor:.2f}")
        print(f"Saldo anterior: R$ {saldo:.2f}")
        print(f"Saldo atual: R$ {novo_saldo:.2f}")
        return True
    else:
        print("\n@@@ Erro ao processar depósito! @@@")
        return False

@log_transacao("SAQUE")
def sacar(cpf, numero_conta, valor, limite=500, limite_saques=3):
    """Realiza um saque na conta com verificações de limite."""
    saldo = obter_saldo_conta(cpf, numero_conta)
    
    # Contar saques de hoje
    transacoes = obter_transacoes_conta(cpf, numero_conta)
    data_hoje = date.today().strftime("%d/%m/%Y")
    saques_hoje = sum(1 for t in transacoes if t['tipo'] == 'saque' and t['data_hora'].startswith(data_hoje))
    
    # Contar transações de hoje
    transacoes_hoje = sum(1 for t in transacoes if t['data_hora'].startswith(data_hoje))
    
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = saques_hoje >= limite_saques
    excedeu_transacoes_dia = transacoes_hoje >= 10
    
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print(f"\n@@@ Operação falhou! Número máximo de saques ({limite_saques}) excedido. @@@")
    elif excedeu_transacoes_dia:
        print("\n@@@ Operação falhou! Você excedeu o número de transações permitidas para hoje (máximo 10). @@@")
    elif valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        novo_saldo = saldo - valor
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        
        if adicionar_transacao_csv(cpf, numero_conta, "saque", valor, data_hora, novo_saldo):
            print("\n=== Saque realizado com sucesso! ===")
            print(f"Valor: R$ {valor:.2f}")
            print(f"Saldo anterior: R$ {saldo:.2f}")
            print(f"Saldo atual: R$ {novo_saldo:.2f}")
            return True
        else:
            print("\n@@@ Erro ao processar saque! @@@")
            return False
    
    return False

# ================== VISUALIZAÇÕES ==================
def exibir_extrato(cpf, numero_conta):
    """Exibe o extrato da conta com todas as transações."""
    transacoes = obter_transacoes_conta(cpf, numero_conta)
    saldo = obter_saldo_conta(cpf, numero_conta)
    
    print("\n================ EXTRATO ================")
    
    if transacoes:
        print("\nHistórico detalhado de transações:\n")
        for i, transacao in enumerate(transacoes, 1):
            tipo = transacao['tipo'].upper()
            valor = transacao['valor']
            data_hora = transacao['data_hora']
            saldo_apos = transacao['saldo_apos']
            
            if transacao['tipo'] == 'deposito':
                print(f"{i}. [{data_hora}] DEPÓSITO")
            else:
                print(f"{i}. [{data_hora}] SAQUE")
            print(f"   Valor: R$ {valor:.2f}")
            print(f"   Saldo após transação: R$ {saldo_apos:.2f}\n")
    else:
        print("Nenhuma transação realizada.")
    
    print(f"\nSaldo Atual:\t\tR$ {saldo:.2f}")
    print("==========================================")

def exibir_relatorio(cpf, numero_conta):
    """
    Exibe relatório de transações usando o gerador.
    Permite ao usuário escolher se quer filtrar por tipo.
    """
    transacoes = obter_transacoes_conta(cpf, numero_conta)
    
    if not transacoes:
        print("\n@@@ Nenhuma transação registrada nesta conta! @@@")
        return
    
    print("\n================ RELATÓRIO DE TRANSAÇÕES ================")
    print(f"Conta: {numero_conta} | CPF: {cpf}")
    print("\n[1] Todas as transações")
    print("[2] Apenas depósitos")
    print("[3] Apenas saques")
    
    opcao = input("\nEscolha uma opção: ")
    
    filtro = None
    if opcao == "2":
        filtro = "deposito"
        print("\n--- DEPÓSITOS ---\n")
    elif opcao == "3":
        filtro = "saque"
        print("\n--- SAQUES ---\n")
    else:
        print("\n--- TODAS AS TRANSAÇÕES ---\n")
    
    encontrou = False
    for i, transacao in enumerate(gerar_relatorio_transacoes(cpf, numero_conta, filtro), 1):
        encontrou = True
        tipo = transacao["tipo"].upper()
        valor = transacao["valor"]
        data_hora = transacao["data_hora"]
        saldo_apos = transacao["saldo_apos"]
        
        print(f"{i}. [{data_hora}] {tipo}")
        print(f"   Valor: R$ {valor:.2f}")
        print(f"   Saldo após: R$ {saldo_apos:.2f}\n")
    
    if not encontrou:
        print("Nenhuma transação encontrada com o filtro selecionado.")
    
    print("=" * 55)

def listar_contas():
    """Lista todas as contas criadas com informações do titular."""
    contas = carregar_contas()
    
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return
    
    print("\n================ CONTAS ================")
    for conta in contas:
        usuario = obter_usuario(conta['cpf'])
        saldo = obter_saldo_conta(conta['cpf'], conta['numero_conta'])
        
        print(f"\nAgência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Titular: {usuario['nome']}")
        print(f"Saldo: R$ {saldo:.2f}")
        print("-" * 40)
    print("==========================================")

def listar_usuarios_com_contas():
    """Lista todos os usuários com suas contas relacionadas."""
    usuarios = carregar_usuarios()
    contas = carregar_contas()
    
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! @@@")
        return
    
    print("\n================ USUÁRIOS E CONTAS =================")
    for usuario in usuarios:
        print(f"\n--- Usuário ---")
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        
        contas_usuario = [c for c in contas if c['cpf'] == usuario['cpf']]
        
        if contas_usuario:
            print(f"\n  Contas ({len(contas_usuario)}):")
            for conta in contas_usuario:
                saldo = obter_saldo_conta(conta['cpf'], conta['numero_conta'])
                print(f"    - Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Saldo: R$ {saldo:.2f}")
        else:
            print(f"\n  Contas: Nenhuma conta cadastrada")
        
        print("-" * 50)
    print("===================================================")

def exibir_iterador_contas():
    """Usa o iterador personalizado ContaIterador para exibir as contas."""
    contas = carregar_contas()
    
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

def login_conta():
    """
    Realiza login por conta.
    Pede CPF, valida usuário, lista suas contas e permite selecionar uma.
    """
    cpf = input("Informe o CPF: ")
    cpf = re.sub(r'\s+', '', cpf)
    cpf = re.sub(r'\D', '', cpf)
    
    if not cpf or len(cpf) != 11:
        print("\n@@@ CPF inválido! Deve conter 11 dígitos. @@@")
        return None
    
    usuario = obter_usuario(cpf)
    if not usuario:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! @@@")
        return None
    
    contas_usuario = obter_contas_do_usuario(cpf)
    
    if not contas_usuario:
        print(f"\n@@@ O usuário {usuario['nome']} não possui contas! @@@")
        return None
    
    print(f"\n=== Bem-vindo, {usuario['nome']}! ===")
    print("\nSuas contas:")
    
    for i, conta in enumerate(contas_usuario, 1):
        saldo = obter_saldo_conta(conta['cpf'], conta['numero_conta'])
        print(f"{i}. Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Saldo: R$ {saldo:.2f}")
    
    while True:
        try:
            numero_conta_digitado = int(input("\nSelecione o número da conta para acessar: "))
            # Validar se o número da conta digitado existe entre as contas do usuário
            conta_selecionada = None
            for conta in contas_usuario:
                # Converter numero_conta para int para comparação (pode vir como string do CSV)
                if int(conta['numero_conta']) == numero_conta_digitado:
                    conta_selecionada = conta
                    break
            
            if conta_selecionada:
                return {
                    'cpf': cpf,
                    'usuario': usuario,
                    'conta': conta_selecionada,
                    'numero_conta': conta_selecionada['numero_conta']
                }
            else:
                print("@@@ Número de conta inválido! Selecione um dos números listados acima. @@@")
        except ValueError:
            print("Digite um número válido!")

# ================== EXIBIÇÃO DA CONTA ATIVA ==================
def exibir_conta_ativa(conta_ativa):
    """
    Exibe as informações da conta ativa com data/hora.
    Chamada antes do menu sempre que há conta logada.
    """
    if not conta_ativa:
        return
    
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    usuario_nome = conta_ativa['usuario']['nome'] if isinstance(conta_ativa.get('usuario'), dict) else "Desconhecido"
    numero_conta = conta_ativa.get('numero_conta', '')
    
    print(f"\n[{agora}] {usuario_nome} - Conta: {numero_conta}")

# ================== FUNÇÃO PRINCIPAL ==================
def main():
    """Função principal que executa o loop do programa."""
    AGENCIA = "0001"
    LIMITE = 500
    LIMITE_SAQUES = 3
    
    # Inicializar CSVs
    inicializar_csvs()
    
    print("\n" + "="*50)
    print("BEM-VINDO AO SISTEMA BANCÁRIO PYTHON v4.0")
    print("Com Persistência de Dados em CSV")
    print("="*50)
    
    conta_ativa = None  # Rastrear conta ativa do usuário
    
    while True:
        # Exibir informações da conta ativa se houver
        exibir_conta_ativa(conta_ativa)
        
        # Verificar se é primeira execução ou se já há dados
        if not dados_existem():
            opcao = menu_primeira_execucao()
        else:
            opcao = menu_dados_existentes()
        
        if opcao == "nu":
            novo_usuario()
        
        elif opcao == "nc":
            conta = nova_conta(AGENCIA)
            if conta:
                conta_ativa = conta
                usuario = obter_usuario(conta['cpf'])
                print(f"\n✓ Conta criada com sucesso e definida como ativa!")
        
        elif opcao == "lg":
            if not contas_existem():
                print("\n@@@ Nenhuma conta cadastrada! Crie uma conta primeiro. @@@")
                continue
            
            login = login_conta()
            if login:
                conta_ativa = login
                print("\n✓ Login realizado com sucesso!")
        
        elif opcao == "de":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Faça login em uma conta primeiro. @@@")
                continue
            
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                depositar(conta_ativa['cpf'], conta_ativa['numero_conta'], valor)
            except ValueError:
                print("\n@@@ Valor inválido! @@@")
        
        elif opcao == "sa":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Faça login em uma conta primeiro. @@@")
                continue
            
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                sacar(conta_ativa['cpf'], conta_ativa['numero_conta'], valor, LIMITE, LIMITE_SAQUES)
            except ValueError:
                print("\n@@@ Valor inválido! @@@")
        
        elif opcao == "ex":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Faça login em uma conta primeiro. @@@")
                continue
            
            exibir_extrato(conta_ativa['cpf'], conta_ativa['numero_conta'])
        
        elif opcao == "rel":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Faça login em uma conta primeiro. @@@")
                continue
            
            exibir_relatorio(conta_ativa['cpf'], conta_ativa['numero_conta'])
        
        elif opcao == "lc":
            listar_contas()
        
        elif opcao == "lu":
            listar_usuarios_com_contas()
        
        elif opcao == "it":
            exibir_iterador_contas()
        
        elif opcao == "qt":
            print("\n" + "="*50)
            print("Obrigado por usar nosso banco. Até logo!")
            print("="*50 + "\n")
            break
        
        else:
            print("\n@@@ Operação inválida. Tente novamente! @@@")

if __name__ == "__main__":
    main()
