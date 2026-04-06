import textwrap
import re
from datetime import datetime, date
from functools import wraps

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
        
        # Calcular saldo da conta (contas podem ter transações)
        saldo_conta = 0
        if "transacoes" in conta:
            for transacao in conta["transacoes"]:
                if transacao["tipo"] == "deposito":
                    saldo_conta += transacao["valor"]
                elif transacao["tipo"] == "saque":
                    saldo_conta -= transacao["valor"]
        
        return {
            "agencia": conta["agencia"],
            "numero": conta["numero_conta"],
            "titular": conta["usuario"]["nome"],
            "saldo": saldo_conta
        }

# ================== GERADOR DE RELATÓRIOS ==================
def gerar_relatorio_transacoes(conta, tipo_filtro=None):
    """
    Gerador que permite iterar sobre as transações de uma conta.
    Retorna uma a uma as transações realizadas.
    
    Args:
        conta: Dicionário da conta
        tipo_filtro: Opcional - pode ser "deposito", "saque" ou None (todos)
    
    Yields:
        Transação formatada
    """
    if "transacoes" not in conta or not conta["transacoes"]:
        return
    
    for transacao in conta["transacoes"]:
        if tipo_filtro is None or transacao["tipo"] == tipo_filtro:
            yield transacao

# ================== VALIDAÇÕES ==================
def validar_cpf(cpf):
    """
    Valida um CPF seguindo as regras brasileiras.
    Verifica se o CPF possui 11 dígitos e valida os dígitos verificadores.
    """
    # Remove caracteres que não sejam dígitos
    cpf = re.sub(r'\D', '', cpf)
    
    # CPF deve ter exatamente 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Não pode ser todos os mesmos dígitos
    if cpf == cpf[0] * 11:
        return False
    
    # Validar primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != primeiro_digito:
        return False
    
    # Validar segundo dígito verificador
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
    
    Formato esperado: logradouro, numero - bairro - cidade/uf - CEP
    Exemplo: Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63.113-420
    """
    if not endereco or not isinstance(endereco, str):
        return None
    
    endereco = endereco.strip()
    
    # Dividir o endereço em partes usando " - " como separador
    partes = [p.strip() for p in endereco.split(" - ")]
    
    # Deve ter 3 partes: (logradouro,numero), (bairro), (cidade/uf + CEP)
    if len(partes) < 3:
        return None
    
    # Primeira parte: logradouro e número
    parte1 = partes[0]
    if ',' not in parte1:
        return None
    logradouro_numero = parte1.split(',', 1)
    logradouro = logradouro_numero[0].strip()
    numero = logradouro_numero[1].strip()
    
    # Validar se número contém apenas dígitos
    if not numero.isdigit():
        return None
    
    # Segunda parte: bairro
    bairro = partes[1].strip()
    if not bairro:
        return None
    
    # Última parte: cidade/uf - CEP
    ultima_parte = " - ".join(partes[2:])  # Caso tenha mais de 3 partes
    
    # Dividir na última ocorrência de " - "
    if " - " not in ultima_parte:
        return None
    
    partes_cep = ultima_parte.rsplit(" - ", 1)  # Split da direita para esquerda
    cidade_uf = partes_cep[0].strip()
    cep_str = partes_cep[1].strip()
    
    # Validar cidade/uf (formato: CIDADE/UF)
    if '/' not in cidade_uf:
        return None
    
    cidade_uf_partes = cidade_uf.rsplit('/', 1)
    cidade = cidade_uf_partes[0].strip()
    uf = cidade_uf_partes[1].strip()
    
    # Validar UF (deve ter 2 letras maiúsculas)
    if len(uf) != 2 or not uf.isupper():
        # Tenta converter para maiúsculas
        uf = uf.upper()
        if len(uf) != 2 or not uf.isalpha():
            return None
    
    # Validar e extrair CEP
    # CEP pode estar em formato 12345-678 ou 12.345-678
    cep_limpo = re.sub(r'[^0-9\-]', '', cep_str)  # Remove tudo que não é dígito ou hífen
    
    # Padrão: 5 dígitos, hífen, 3 dígitos
    if not re.match(r'^\d{5}-\d{3}$', cep_limpo):
        return None
    
    # Reconstruir endereço normalizado
    endereco_normalizado = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf} - {cep_limpo}"
    
    return endereco_normalizado

def validar_endereco(endereco):
    """
    Valida o endereço no formato especificado:
    logradouro, numero - bairro - cidade/uf - CEP
    Aceita CEP com ou sem ponto (ex: 01234-567 ou 01.234-567)
    """
    return normalizar_endereco(endereco) is not None

def menu():
    """Exibe o menu e retorna a opção selecionada."""
    menu_text = """\n
    ================ MENU ================
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

@log_transacao("DEPÓSITO")
def depositar(saldo, valor, extrato, transacoes, /):
    """
    Realiza um depósito na conta.
    Registra a transação com data e hora.
    """
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato, transacoes
    
    saldo += valor
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
    
    extrato += f"[{data_hora}] Depósito:\t\tR$ {valor:.2f}\n"
    
    # Registrar transação
    transacao = {
        "tipo": "deposito",
        "valor": valor,
        "data_hora": agora,
        "data_hora_str": data_hora,
        "saldo_apos": saldo
    }
    transacoes.append(transacao)
    
    print("\n=== Depósito realizado com sucesso! ===")
    return saldo, extrato, transacoes

@log_transacao("SAQUE")
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, transacoes, transacoes_hoje):
    """
    Realiza um saque na conta.
    Verifica limite de 10 transações diárias.
    Registra a transação com data e hora.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    excedeu_transacoes_dia = transacoes_hoje >= 10  # Novo: limite de 10 transações diárias
    
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif excedeu_transacoes_dia:
        print("\n@@@ Operação falhou! Você excedeu o número de transações permitidas para hoje (máximo 10). @@@")
    elif valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    else:
        saldo -= valor
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        
        extrato += f"[{data_hora}] Saque:\t\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        
        # Registrar transação
        transacao = {
            "tipo": "saque",
            "valor": valor,
            "data_hora": agora,
            "data_hora_str": data_hora,
            "saldo_apos": saldo
        }
        transacoes.append(transacao)
        
        print("\n=== Saque realizado com sucesso! ===")
        return saldo, extrato, numero_saques, transacoes, transacoes_hoje + 1
    
    return saldo, extrato, numero_saques, transacoes, transacoes_hoje

def exibir_extrato(saldo, /, *, extrato, transacoes=None):
    """
    Exibe o extrato da conta com todas as transações.
    Se transações forem fornecidas, exibe com data/hora detalhada.
    """
    print("\n================ EXTRATO ================")
    
    if transacoes and len(transacoes) > 0:
        print("\nHistórico detalhado de transações:\n")
        for i, transacao in enumerate(transacoes, 1):
            tipo = transacao["tipo"].upper()
            valor = transacao["valor"]
            data_hora = transacao["data_hora_str"]
            saldo_apos = transacao["saldo_apos"]
            
            if transacao["tipo"] == "deposito":
                print(f"{i}. [{data_hora}] DEPÓSITO")
                print(f"   Valor: R$ {valor:.2f}")
                print(f"   Saldo após transação: R$ {saldo_apos:.2f}\n")
            else:
                print(f"{i}. [{data_hora}] SAQUE")
                print(f"   Valor: R$ {valor:.2f}")
                print(f"   Saldo após transação: R$ {saldo_apos:.2f}\n")
    elif extrato:
        print(extrato)
    else:
        print("Nenhuma transação realizada.")
    
    print(f"\nSaldo:\t\t\tR$ {saldo:.2f}")
    print("==========================================")

def novo_usuario(usuarios):
    """Cria um novo usuário com validação de CPF e endereço."""
    cpf = input("Informe o CPF (somente números): ")
    cpf = re.sub(r'\D', '', cpf)
    
    # Validar CPF
    if not validar_cpf(cpf):
        print("\n@@@ CPF inválido! @@@")
        return
    
    # Verificar se CPF já existe
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/uf - CEP): ")
    
    # Validar e normalizar endereço
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
        return
    
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco_normalizado
    }
    
    usuarios.append(usuario)
    print("\n=== Usuário criado com sucesso! ===")
    print(f"Nome: {nome}")
    print(f"CPF: {cpf}")

def filtrar_usuario(cpf, usuarios):
    """Filtra um usuário pelo CPF na lista de usuários."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def nova_conta(agencia, numero_conta, usuarios):
    """Cria uma nova conta vinculada a um usuário existente."""
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! Crie um usuário antes de criar uma conta. @@@")
        return None
    
    cpf = input("Informe o CPF do usuário: ")
    # Limpar CPF: remover espaços, pontos, hífens e outros caracteres não numéricos
    cpf = re.sub(r'\s+', '', cpf)  # Remove espaços em branco
    cpf = re.sub(r'\D', '', cpf)   # Remove todos os caracteres que não são dígitos
    
    if not cpf or len(cpf) != 11:
        print("\n@@@ CPF inválido! Deve conter 11 dígitos. @@@")
        return None
    
    usuario = filtrar_usuario(cpf, usuarios)
    
    if not usuario:
        print(f"\n@@@ Usuário com CPF {cpf} não encontrado! @@@")
        print("\nUsários cadastrados:")
        for u in usuarios:
            print(f"  - {u['nome']} (CPF: {u['cpf']})")
        return None
    
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "transacoes": [],  # Novo: lista para armazenar transações com data/hora
        "data_criacao": datetime.now()  # Novo: data de criação da conta
    }
    
    print("\n=== Conta criada com sucesso! ===")
    print(f"Titular: {usuario['nome']}")
    print(f"Agência: {agencia}")
    print(f"Número da Conta: {numero_conta}")
    return conta

def exibir_relatorio(conta):
    """
    Exibe relatório de transações usando o gerador.
    Permite ao usuário escolher se quer filtrar por tipo.
    """
    if not conta or "transacoes" not in conta or not conta["transacoes"]:
        print("\n@@@ Nenhuma transação registrada nesta conta! @@@")
        return
    
    print("\n================ RELATÓRIO DE TRANSAÇÕES ================")
    print(f"Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
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
    for i, transacao in enumerate(gerar_relatorio_transacoes(conta, filtro), 1):
        encontrou = True
        tipo = transacao["tipo"].upper()
        valor = transacao["valor"]
        data_hora = transacao["data_hora_str"]
        saldo_apos = transacao["saldo_apos"]
        
        print(f"{i}. [{data_hora}] {tipo}")
        print(f"   Valor: R$ {valor:.2f}")
        print(f"   Saldo após: R$ {saldo_apos:.2f}\n")
    
    if not encontrou:
        print("Nenhuma transação encontrada com o filtro selecionado.")
    
    print("=" * 55)

def listar_contas(contas):
    """Lista todas as contas criadas com informações do titular."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return
    
    print("\n================ CONTAS ================")
    for conta in contas:
        print(f"\nAgência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("-" * 40)
    print("==========================================")
def listar_usuarios_com_contas(usuarios, contas):
    """Lista todos os usuários com suas contas relacionadas."""
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
        
        # Filtrar contas deste usuário
        contas_usuario = [conta for conta in contas if conta['usuario']['cpf'] == usuario['cpf']]
        
        if contas_usuario:
            print(f"\n  Contas ({len(contas_usuario)}):")
            for conta in contas_usuario:
                print(f"    - Agência: {conta['agencia']} | Conta: {conta['numero_conta']}")
        else:
            print(f"\n  Contas: Nenhuma conta cadastrada")
        
        print("-" * 50)
    print("===================================================")

def exibir_iterador_contas(contas):
    """
    Usa o iterador personalizado ContaIterador para exibir as contas.
    Mostra número, saldo (calculado), agência e titular.
    """
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

def main():
    """Função principal que executa o loop do programa."""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    transacoes = []  # Novo: lista global de transações da conta ativa
    transacoes_hoje = 0  # Novo: contador de transações do dia
    data_transacoes = date.today()  # Novo: data das transações para resetar contador
    conta_ativa = None  # Novo: rastrear qual conta está ativa
    
    print("\n" + "="*50)
    print("BEM-VINDO AO SISTEMA BANCÁRIO PYTHON v3.0")
    print("Com suporte a Data/Hora, Decoradores, Geradores e Iteradores")
    print("="*50)
    
    while True:
        opcao = menu()
        
        # Verificar se precisa resetar contador de transações (novo dia)
        if transacoes_hoje > 0 and date.today() != data_transacoes:
            data_transacoes = date.today()
            transacoes_hoje = 0
            numero_saques = 0
            print("\n[INFO] Novo dia! Contadores de transações e saques resetados.")
        
        if opcao == "nu":
            novo_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = nova_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                conta_ativa = conta  # Novo: define a conta ativa
                transacoes = conta["transacoes"]
                saldo = 0  # Reset de saldo para a nova conta
                numero_saques = 0
                transacoes_hoje = 0
        
        elif opcao == "de":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Crie uma nova conta primeiro. @@@")
                continue
            
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                saldo, extrato, transacoes = depositar(saldo, valor, extrato, transacoes)
                conta_ativa["transacoes"] = transacoes  # Atualizar transações da conta
                transacoes_hoje += 1
            except ValueError:
                print("\n@@@ Valor inválido! @@@")
        
        elif opcao == "sa":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Crie uma nova conta primeiro. @@@")
                continue
            
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                resultado = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                    transacoes=transacoes,
                    transacoes_hoje=transacoes_hoje
                )
                saldo, extrato, numero_saques, transacoes, transacoes_hoje = resultado
                conta_ativa["transacoes"] = transacoes  # Atualizar transações da conta
            except ValueError:
                print("\n@@@ Valor inválido! @@@")
        
        elif opcao == "ex":
            exibir_extrato(saldo, extrato=extrato, transacoes=transacoes)
        
        elif opcao == "rel":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa! Crie uma nova conta primeiro. @@@")
                continue
            exibir_relatorio(conta_ativa)
        
        elif opcao == "it":
            exibir_iterador_contas(contas)
        
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "lu":
            listar_usuarios_com_contas(usuarios, contas)
        
        elif opcao == "qt":
            print("\n" + "="*50)
            print("Obrigado por usar nosso banco. Até logo!")
            print("="*50 + "\n")
            break
        
        else:
            print("\n@@@ Operação inválida. Tente novamente! @@@")

if __name__ == "__main__":
    main()