# 🏦 Sistema Bancário em Python - Documentação Completa

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Validações](#validações)
3. [Gerenciamento de Usuários](#gerenciamento-de-usuários)
4. [Gerenciamento de Contas](#gerenciamento-de-contas)
5. [Operações Bancárias](#operações-bancárias)
6. [Interface do Menu](#interface-do-menu)
7. [Fluxo Principal](#fluxo-principal)
8. [Estrutura de Dados](#estrutura-de-dados)

---

## 🎯 Visão Geral

Este sistema é um **banco digital funcional** desenvolvido em Python que permite gerenciar usuários, contas bancárias e realizar operações financeiras básicas. O programa implementa validações robustas e segue as boas práticas de desenvolvimento.

### Tecnologias Utilizadas
- **Linguagem**: Python 3.x
- **Estruturas de Dados**: Listas e Dicionários
- **Módulos**: `textwrap` (formatação de texto) e `re` (expressões regulares)

---

## ✅ Validações

### 🆔 `validar_cpf(cpf: str) -> bool`

Realiza validação completa de um CPF conforme as regras brasileiras.

**O que faz:**
- Remove caracteres especiais (mantém apenas dígitos)
- Verifica se possui exatamente 11 dígitos
- Rejeita CPFs com todos os dígitos iguais (111.111.111-11, 222.222.222-22, etc.)
- Valida o **primeiro dígito verificador** usando algoritmo módulo 11
- Valida o **segundo dígito verificador** usando algoritmo módulo 11

**Parâmetros:**
- `cpf` (str): CPF a ser validado (com ou sem formatação)

**Retorno:**
- `True`: CPF é válido
- `False`: CPF é inválido

**Exemplos de Uso:**
```python
validar_cpf("123.456.789-09")  # True (se válido)
validar_cpf("111.111.111-11")  # False (todos dígitos iguais)
validar_cpf("123.456.789-10")  # False (dígito verificador inválido)
validar_cpf("12345")           # False (menos de 11 dígitos)
```

**Algoritmo de Validação:**
1. **Primeiro Dígito**: Multiplica os 9 primeiros dígitos por 10, 9, 8, ..., 2
2. **Segundo Dígito**: Multiplica os 10 primeiros dígitos por 11, 10, 9, ..., 2
3. **Cálculo**: Se resto < 2, dígito = 0, senão dígito = 11 - resto

---

### 📍 `normalizar_endereco(endereco: str) -> str | None` (NOVO v2.1)

Normaliza e valida o endereço, aceitando CEP com ou sem ponto.

**O que faz:**
- Converte `63.113-420` em `63113-420` automaticamente
- Valida todos os componentes do endereço
- Retorna o endereço normalizado ou `None` se inválido
- Remove espaços extras desnecessários

**Formato Aceito:**
```
logradouro, numero - bairro - cidade/uf - CEP
```

**CEP Aceito:**
- `XXXXX-XXX` (sem ponto) ✅
- `XXXXX.XXX` (com ponto) ✅ - Será convertido para sem ponto
- Exemplos: `01310-100` ou `01.310-100`

**Exemplos Válidos:**
```
Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63113-420
Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63.113-420 (com ponto)
Avenida Paulista, 1000 - Centro - São Paulo/SP - 01310-100
Rua das Flores, 42 - Jaraguá - Blumenau/SC - 89012-500
```

**O que valida:**
- ✅ Presença de vírgula após o logradouro
- ✅ Número após a vírgula (apenas dígitos)
- ✅ Bairro após primeiro hífen
- ✅ Cidade/UF com formato correto (slash / entre cidade e 2 letras maiúsculas)
- ✅ CEP com formato XXXXX-XXX ou XXXXX.XXX

**Parâmetros:**
- `endereco` (str): Endereço a ser validado e normalizado

**Retorno:**
- `str`: Endereço normalizado (se válido)
- `None`: Se endereço for inválido

**Exemplo:**
```python
resultado = normalizar_endereco("Rua X, 100 - Centro - São Paulo/SP - 01.310-100")
# Resultado: "Rua X, 100 - Centro - São Paulo/SP - 01310-100"

resultado = normalizar_endereco("Endereço inválido")
# Resultado: None
```

---

### 📍 `validar_endereco(endereco: str) -> bool`

Valida se um endereço está no formato correto.

**O que faz:**
- Usa `normalizar_endereco()` internamente
- Retorna `True` se o endereço for válido
- Retorna `False` se o endereço for inválido
- Aceita CEP com ou sem ponto (veja `normalizar_endereco()` para detalhes)

**Parâmetros:**
- `endereco` (str): Endereço a ser validado

**Retorno:**
- `True`: Endereço segue o formato correto  
- `False`: Endereço não segue o formato

**Mudanças na v2.1:**
- Agora aceita CEP com ponto (ex: `63.113-420`)
- Mensagens de erro mais detalhadas com exemplos
- Validação mais robusta baseada em componentes

---

## 👥 Gerenciamento de Usuários

### 🆕 `novo_usuario(usuarios: list) -> None`

Cria um novo usuário com todas as validações necessárias.

**Processo de Cadastro:**
1. Solicita CPF e valida (máximo 3 tentativas implícitas)
2. Verifica se CPF já existe na lista
3. Coleta nome completo
4. Coleta data de nascimento (sem validação de formato específico)
5. Coleta endereço e valida o formato
6. Armazena usuário como dicionário na lista

**Estrutura do Usuário:**
```python
{
    "nome": "João da Silva",
    "data_nascimento": "15/08/1990",
    "cpf": "12345678901",          # Apenas números
    "endereco": "Rua X, 100 - Centro - São Paulo/SP - 01310-100"
}
```

**Validações Implementadas:**
- ✅ CPF válido (algoritmo mod-11)
- ✅ CPF não duplicado
- ✅ Endereço no formato correto
- ✅ Feedback ao usuário para erros

**Mensagens:**
- `"CPF inválido!"` - CPF não passa na validação
- `"Já existe usuário com esse CPF!"` - CPF duplicado
- `"Endereço em formato inválido!"` - Endereço não segue o padrão
- `"Usuário criado com sucesso!"` - Sucesso!

---

### 🔍 `filtrar_usuario(cpf: str, usuarios: list) -> dict | None`

Busca um usuário específico na lista pelo CPF.

**O que faz:**
- Pesquisa na lista de usuários
- Retorna o primeiro usuário com CPF correspondente
- Usa compreensão de lista para eficiência

**Parâmetros:**
- `cpf` (str): CPF a ser buscado (apenas números)
- `usuarios` (list): Lista de usuários cadastrados

**Retorno:**
- Dicionário com dados do usuário (se encontrado)
- `None` (se não encontrado)

**Exemplos de Uso:**
```python
usuario = filtrar_usuario("12345678901", usuarios)
if usuario:
    print(f"Usuário encontrado: {usuario['nome']}")
else:
    print("Usuário não encontrado!")
```

---

## 🏧 Gerenciamento de Contas

### 💳 `nova_conta(agencia: str, numero_conta: int, usuarios: list) -> dict`

Cria uma nova conta bancária vinculada a um usuário existente.

**Processo de Criação:**
1. Verifica se existem usuários cadastrados (NOVO v2.0)
2. Solicita CPF do usuário titular
3. **CORRIGIDO v2.0**: Remove espaços e caracteres especiais do CPF
4. Valida existência do usuário
5. Cria conta vinculada ao usuário
6. Retorna a conta criada com feedback detalhado (MELHORADO v2.0)

**Estrutura da Conta:**
```python
{
    "agencia": "0001",           # Agência fixa
    "numero_conta": 1,            # Sequencial
    "usuario": { ... }            # Referência ao dicionário do usuário
}
```

**Características:**
- Agência fixa: **"0001"**
- Número sequencial: começando em **1**
- Vincular apenas usuários que existem
- Um usuário pode ter múltiplas contas
- Uma conta pertence a apenas um usuário

**Validações:**
- ✅ Verifica se há usuários cadastrados (NOVO v2.0)
- ✅ CPF informado deve existir (com 11 dígitos)
- ✅ Limpeza melhorada do CPF (espaços e caracteres especiais)
- ✅ Usuário encontrado com êxito

**Mensagens:**
- `"Nenhum usuário cadastrado!"` - Sem usuários no sistema (NOVO v2.0)
- `"CPF inválido! Deve conter 11 dígitos."` - Formato inválido (NOVO v2.0)
- `"Usuário com CPF XXXXX não encontrado!"` - CPF específico não existe (MELHORADO v2.0)
- Após não encontrar, lista CPFs disponíveis (NOVO v2.0)
- `"Conta criada com sucesso!"` - Sucesso com informações da conta (MELHORADO v2.0)

**Melhorias na v2.0:**
- Limpeza de CPF melhorada: `re.sub(r'\\s+', '', cpf)` remove espaços
- Validação do tamanho do CPF antes de buscar
- Feedback detalhado mostrando CPFs disponíveis se não encontrar
- Mensagens mais informativas sobre o erro

**Exemplo de Uso:**
```python
numero_conta = len(contas) + 1
conta = nova_conta("0001", numero_conta, usuarios)
if conta:
    contas.append(conta)
    print(f"Conta #{numero_conta} criada para {conta['usuario']['nome']}")
```

---

### 📱 `listar_contas(contas: list) -> None`

Exibe todas as contas cadastradas com informações do titular.

**O que exibe:**
- Número da agência
- Número da conta
- Nome do titular
- Separação visual entre contas

**Formatação:**
```
================ CONTAS ================
Agência: 0001
Número da Conta: 1
Titular: João da Silva
----------------------------------------
Agência: 0001
Número da Conta: 2
Titular: Maria Santos
==========================================
```

**Tratamento Especial:**
- Se não há contas: `"Nenhuma conta cadastrada!"`
- Iteração sobre lista de contas
- Acesso aos dados do usuário vinculado

---

### 👥 `listar_usuarios_com_contas(usuarios: list, contas: list) -> None`

Exibe todos os usuários cadastrados com suas contas relacionadas (NOVO v2.0).

**O que exibe:**
- Nome do usuário
- CPF (apenas dígitos)
- Data de nascimento
- Endereço completo
- Lista de contas associadas (agência e número)
- Quantidade de contas por usuário

**Formatação:**
```
================ USUÁRIOS E CONTAS =================

--- Usuário ---
Nome: João da Silva
CPF: 12345678901
Data de Nascimento: 15/08/1990
Endereço: Rua X, 100 - Centro - São Paulo/SP - 01310-100

  Contas (2):
    - Agência: 0001 | Conta: 1
    - Agência: 0001 | Conta: 2

--------------------------------------------------

--- Usuário ---
Nome: Maria Santos
CPF: 98765432109
Data de Nascimento: 22/11/1985
Endereço: Avenida Y, 200 - Bairro Z - Rio de Janeiro/RJ - 20000-000

  Contas: Nenhuma conta cadastrada

==================================================
```

**Tratamento Especial:**
- Se não há usuários: `"Nenhum usuário cadastrado!"`
- Filtra contas do usuário usando CPF
- Exibe "Nenhuma conta cadastrada" se usuário não tiver contas
- Mostra contagem de contas por usuário

---

## 💰 Operações Bancárias

### 💵 `depositar(saldo: float, valor: float, extrato: str, /) -> tuple`

Realiza um depósito na conta bancária.

**Parâmetros (Posicionais Obrigatórios):**
- `saldo` (float): Saldo atual da conta
- `valor` (float): Valor a depositar
- `extrato` (str): Histórico de transações

**Retorno:**
- Tupla: `(novo_saldo, novo_extrato)`

**Validações:**
- ✅ Valor deve ser maior que 0
- ❌ Rejeita valores negativos ou zero

**Comportamento:**
- Sucesso: Soma valor ao saldo, registra no extrato
- Erro: Exibe mensagem e não altera saldo

**Formato no Extrato:**
```
Depósito:		R$ 100.00
```

**Exemplo:**
```python
saldo, extrato = depositar(1000, 150, extrato)
# Resultado: saldo = 1150, extrato atualizado
```

---

### 💸 `sacar(*, saldo: float, valor: float, extrato: str, limite: float, numero_saques: int, limite_saques: int) -> tuple`

Realiza um saque com múltiplas validações de segurança.

**Parâmetros (Somente Nomeados):**
- `saldo` (float): Saldo disponível
- `valor` (float): Valor do saque
- `extrato` (str): Histórico de transações
- `limite` (float): Limite de saque por transação
- `numero_saques` (int): Saques realizados hoje
- `limite_saques` (int): Máximo de saques permitidos

**Retorno:**
- Tupla: `(novo_saldo, novo_extrato, novo_numero_saques)`
- Se erro: retorna valores inalterados

**Validações (em ordem):**
1. ✅ Verificar saldo suficiente
2. ✅ Verificar limite de saque
3. ✅ Verificar número máximo de saques
4. ✅ Verificar se valor é positivo

**Mensagens de Erro:**
- `"Você não tem saldo suficiente."` - Saldo insuficiente
- `"O valor do saque excede o limite."` - Acima do limite
- `"Número máximo de saques excedido."` - Limite diário atingido
- `"O valor informado é inválido."` - Valor negativo ou zero

**Exemplo:**
```python
saldo, extrato, numero_saques = sacar(
    saldo=1000,
    valor=150,
    extrato=extrato,
    limite=500,
    numero_saques=1,
    limite_saques=3
)
```

---

### 📄 `exibir_extrato(saldo: float, /, *, extrato: str) -> None`

Exibe o extrato completo da conta com histórico de transações.

**Parâmetros:**
- `saldo` (float): Saldo posicional*
- `extrato` (str): Histórico nomeado

**O que exibe:**
- Cabeçalho formatado
- Histórico de transações (depósitos e saques)
- Saldo final com 2 casas decimais
- Rodapé formatado

**Formatação:**
```
================ EXTRATO ================
Depósito:		R$ 100.00
Saque:			R$ 50.00

Saldo:			R$ 50.00
==========================================
```

**Tratamento Especial:**
- Se sem transações: `"Nenhuma transação realizada."`
- Cada transação em linha separada
- Saldo sempre exibido

---

## 🎯 Interface do Menu

### 📺 `menu() -> str`

Exibe o menu de opções e captura a escolha do usuário.

**Menu Disponível:**
```
================ MENU ================
[de]     Depositar
[sa]     Sacar
[ex]     Extrato
[nc]     Nova conta
[lc]     Listar contas
[lu]     Listar usuários com contas
[nu]     Novo usuário
[qt]     Sair
=> 
```

**Opções Disponíveis:**
| Código | Operação | Descrição |
|--------|----------|-----------|
| `de` | Depositar | Realizar um depósito na conta |
| `sa` | Sacar | Realizar um saque na conta |
| `ex` | Extrato | Visualizar histórico e saldo |
| `nc` | Nova Conta | Criar uma nova conta para usuário |
| `lc` | Listar Contas | Ver todas as contas cadastradas |
| `lu` | Listar Usuários com Contas | Ver usuários com suas contas (NOVO v2.0) |
| `nu` | Novo Usuário | Cadastrar um novo usuário |
| `qt` | Sair | Encerrar o programa |

**Retorno:**
- String com a opção selecionada (em minúsculas)

---

## 🔄 Fluxo Principal

### 🏃 `main() -> None`

Gerencia o loop principal do programa e coordena todas as operações.

**Variáveis Iniciadas:**
```python
LIMITE_SAQUES = 3          # Máximo de saques por dia
AGENCIA = "0001"           # Agência fixa

saldo = 0                  # Saldo inicial
limite = 500               # Limite por saque
extrato = ""               # Histórico vazio
numero_saques = 0          # Contador de saques
usuarios = []              # Lista de usuários
contas = []                # Lista de contas
```

**Fluxo de Execução:**

```
┌─────────────────────────────────────┐
│      Inicializar Programa           │
│  (variáveis e listas vazias)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│      Exibir Menu                    │
│   (capturar opção do usuário)       │
└────────────┬────────────────────────┘
             │
    ┌────────┴─────────┬──────────────┬──────────┬─────────┬─────────┬─────────┐
    │                  │              │          │         │         │         │
    ▼                  ▼              ▼          ▼         ▼         ▼         ▼
  [nu]              [de]            [sa]       [ex]      [nc]      [lc]      [qt]
Novo            Depositar          Sacar     Extrato  Nova       Listar    Sair
Usuário                                       Conta    Contas     Loop

    │                  │              │          │         │         │         │
    └────────────┬──────────────────┬──────────┬─────────┴─────────┘         │
                 │                  │          │                            │
                 └──────────────────┴──────────┘                            ▼
                                    │                              ┌──────────────┐
                                    │                              │ Encerrar     │
                                    └─────────────■────────────────│ Programa     │
                                                                    └──────────────┘
```

**Tratamento de Erros:**
- ✅ Captura `ValueError` em operações numéricas
- ✅ Mensagem `"Operação inválida"` para opção desconhecida
- ✅ Loop contínuo até seleção `[qt]`

**Fluxo de Cada Operação:**

**[de] Depositar:**
```
1. Solicita valor do depósito
2. Valida se é número
3. Chama depositar()
4. Atualiza saldo e extrato
```

**[sa] Sacar:**
```
1. Solicita valor do saque
2. Valida se é número
3. Chama sacar() com todos os parâmetros
4. Se OK, atualiza saldo, extrato e contador
```

**[ex] Extrato:**
```
1. Chama exibir_extrato()
2. Exibe histórico e saldo
```

**[nu] Novo Usuário:**
```
1. Chama novo_usuario()
2. Coleta dados com validações
3. Adiciona à lista
```

**[nc] Nova Conta:**
```
1. Calcula próximo número (len(contas) + 1)
2. Chama nova_conta()
3. Valida vinculação com usuário
4. Adiciona à lista
```

**[lc] Listar Contas:**
```
1. Chama listar_contas()
2. Exibe todas as contas e titulares
```

**[lu] Listar Usuários com Contas (NOVO v2.0):**
```
1. Chama listar_usuarios_com_contas()
2. Exibe todos os usuários com seus dados
3. Mostra as contas de cada usuário
4. Facilita visualização das relações usuário-conta
```

**[qt] Sair:**
```
1. Exibe mensagem de despedida
2. Break do loop
3. Fim do programa
```

---

## 📊 Estrutura de Dados

### Usuário (Dicionário)
```python
usuario = {
    "nome": str,                    # Nome completo do usuário
    "data_nascimento": str,         # DD/MM/YYYY
    "cpf": str,                     # 11 dígitos (sem formatação)
    "endereco": str                 # Formato: rua, num - bairro - cidade/uf - cep
}
```

### Conta (Dicionário)
```python
conta = {
    "agencia": str,                 # Agência fixa "0001"
    "numero_conta": int,            # Número sequencial (1, 2, 3, ...)
    "usuario": dict                 # Referência ao dicionário do usuário
}
```

### Extrato (String)
```python
extrato = """Depósito:\t\tR$ 100.00
Saque:\t\t\tR$ 50.00
Depósito:\t\tR$ 200.00"""
```

---

## 🎓 Conceitos Aplicados

### Estruturas de Dados Utilizadas
- **Listas**: Armazenar usuários e contas
- **Dicionários**: Dados estruturados de usuário e conta
- **Strings**: Histórico de transações e formatação

### Parâmetros Especiais do Python
- **`/` (Posicional)**: `depositar()` e `exibir_extrato()` (parâmetro à esquerda)
- **`*` (Nomeado)**: `sacar()` e `exibir_extrato()` (parâmetros à direita)

### Expressões Regulares
- Validação de CPF, endereço e formato
- Limpeza de caracteres especiais

### Tratamento de Exceções
- `try/except` para entrada de valores numéricos

### Boas Práticas
- Funções pequenas e bem definidas
- Mensagens de erro claras
- Validações em camadas
- Separação de responsabilidades

---

## 🚀 Como Usar

### Iniciar o Programa
```bash
python main.py
```

### Exemplo de Sessão
```
1. [nu] Novo Usuário
   - CPF: 12345678901
   - Nome: João Silva
   - Data: 15/08/1990
   - Endereço: Rua X, 100 - Centro - São Paulo/SP - 01310-100

2. [nc] Nova Conta
   - CPF: 12345678901
   - Conta criada! (Agência: 0001, N°: 1)

3. [de] Depositar
   - Valor: 1000
   - Saldo atualizado para R$ 1000.00

4. [sa] Sacar
   - Valor: 200
   - Saldo atualizado para R$ 800.00

5. [ex] Extrato
   - Visualiza histórico completo

6. [lc] Listar Contas
   - Vê todas as contas cadastradas

7. [qt] Sair
   - Encerra o programa
```

---

## ⚠️ Limitações e Considerações

1. **Saldo não persiste** - Reinicia a cada execução (sem banco de dados)
2. **Limite de saques diário** - Reseta a cada sesão
3. **CPF único** - Não permite CPF duplicado na lista
4. **Endereço rígido** - Formato deve ser exatamente conforme especificado
5. **Sem autenticação** - Qualquer operação sem login

---

## 📝 Changelog

### v2.1 - Correção Crítica de Validação de Endereço
- ✅ **CORRIGIDO CRÍTICO**: Endereço rejeitava CEP com ponto (ex: `63.113-420`)
- ✅ **NOVO**: Função `normalizar_endereco()` que normaliza CEP automaticamente
- ✅ **MELHORADO**: Validação de endereço muito mais robusta (baseada em componentes)
- ✅ **MELHORADO**: Mensagens de erro agora mostram exemplos válidos
- ✅ **ADICIONADO**: Script `test_sistema.py` para validação automática
- ✅ **DOCUMENTAÇÃO**: Atualizada com todas as mudanças e exemplos

### v2.0 - Bugfix & Novas Funcionalidades
- ✅ **NOVO**: Opção [lu] para listar usuários com contas relacionadas
- ✅ **CORRIGIDO**: Bug de "Usuário não encontrado" melhorando limpeza de CPF
- ✅ **MELHORADO**: Mensagens de erro mais detalhadas mostrando usuários disponíveis
- ✅ **ADICIONADO**: Verificação se há usuários antes de criar conta
- ✅ **ADICIONADO**: Validação de tamanho do CPF (deve ter 11 dígitos)
- ✅ **MELHORADO**: Feedback visual ao criar conta com informações completas
- ✅ **DOCUMENTAÇÃO**: Atualizada com todas as mudanças

### v1.0 - Versão Final
- ✅ Todas as funcionalidades conforme PRD-1, PRD-2, PRD-3
- ✅ Validações completas (CPF, Endereço)
- ✅ Menu conforme especificado
- ✅ Gerenciamento de usuários e contas
- ✅ Operações bancárias funcionais

---

## 🐛 Solução de Bugs (v2.1)

### Problema: "Endereço em formato inválido!" mesmo com endereço correto

**Causa Identificada:**
- Regex muito rígida que não aceitava CEP com ponto (ex: `63.113-420`)
- Usuários brasileiros naturalmente usam formatação com ponto no CEP
- Validação rejeitava endereços válidos que não tinham formatação exata

**Solução Implementada:**
```python
# Versão v2.1: Função normalizar_endereco()
def normalizar_endereco(endereco):
    """Normaliza endereço, aceitando CEP com ou sem ponto"""
    # Aceita: Rua X, 100 - Bairro - Cidade/SP - 63.113-420
    # Retorna: Rua X, 100 - Bairro - Cidade/SP - 63113-420
    # Valida cada componente separadamente (mais robusta)
```

**Como Funciona:**
1. Divide o endereço em partes usando " - " como separador
2. Valida cada componente (logradouro, número, bairro, cidade, UF, CEP)
3. Limpa CEP de pontos/hífens extras
4. Retorna endereço normalizado ou `None` se inválido

**Como testar a correção (v2.1):**
1. Execute o programa: `python main.py`
2. Opção [nu] - Novo usuário
3. Quando solicitar endereço, digite com ponto no CEP:
   ```
   Rua Manoel Almino de Lima, 600 - Novo Crato - Crato/CE - 63.113-420
   ```
4. Sistema agora aceita e converte automaticamente para: `63113-420`

---

## 🐛 Solução de Bugs (v2.0)

### Problema: "Usuário não encontrado!" mesmo com usuário criado

**Causa Identificada:**
- Problema na limpeza do CPF ao buscar (espaços em branco não eram removidos)
- Falta de feedback sobre CPFs disponíveis quando não encontra
- Tentativa de buscar usuário sem validar primeiro o CPF

**Solução Implementada:**
```python
# Antes (v1.0):
cpf = re.sub(r'\D', '', cpf)  # Remove apenas o padrão não-dígito

# Depois (v2.0):
cpf = re.sub(r'\s+', '', cpf)  # Remove espaços em branco
cpf = re.sub(r'\D', '', cpf)   # Remove todos os caracteres não-numéricos

# Validação adicionada:
if not cpf or len(cpf) != 11:
    print("CPF inválido! Deve conter 11 dígitos.")
    return None

# Feedback melhorado quando não encontra:
if not usuario:
    print(f"Usuário com CPF {cpf} não encontrado!")
    print("Usuários cadastrados:")
    for u in usuarios:
        print(f"  - {u['nome']} (CPF: {u['cpf']})")
```

**Como testar a correção:**
1. Execute [nu] e crie um usuário com CPF válido (ex: `12345678901`)
2. Depois execute [nc] e digite o mesmo CPF (pode usar com formatação: `123.456.789-01`)
3. Sistema agora encontrará corretamente o usuário

---

**Desenvolvido para:** Trilha Python DIO
**Data:** 2024 | **Atualizado:** 2026
**Status:** ✅ Completo e Funcional (v2.0)

