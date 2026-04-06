# 🏗️ Documentação Técnica v3.0 - Implementação de Decoradores, Geradores e Iteradores

## 📑 Índice
1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Componentes Principais](#componentes-principais)
3. [Exemplos de Código](#exemplos-de-código)
4. [Fluxo de Execução](#fluxo-de-execução)
5. [Casos de Uso](#casos-de-uso)

---

## 🎯 Visão Geral da Arquitetura

O sistema v3.0 foi refatorado para implementar três conceitos chave do curso intermediário de Python:

```
┌─────────────────────────────────────────────────────┐
│         Sistema Bancário v3.0                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ Decoradores  │  │  Geradores   │  │ Iteradores ││
│  │              │  │              │  │            ││
│  │@log_transacao│  │gerar_relat() │  │ContaIter...││
│  └──────────────┘  └──────────────┘  └────────────┘│
│         │                │                │         │
│         └────────────────┼────────────────┘         │
│                          │                          │
│         ┌────────────────┴────────────────┐        │
│         │   Transações com Data/Hora      │        │
│         │   + Limite 10 Transações/Dia    │        │
│         └──────────────────────────────────┘       │
│                                                      │
│  Mantém:                                            │
│  • Validação de CPF (v2.1)                         │
│  • Validação de Endereço (v2.1)                    │
│  • Limite de saques por dia (v1.0)                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Componentes Principais

### 1. Decorador de Log (`@log_transacao`)

**Tipo:** Decorador parametrizado

**Localização:** Linhas 8-22 do `main.py`

**Função:**
```python
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
```

**Uso:**
```python
@log_transacao("DEPÓSITO")
def depositar(saldo, valor, extrato, transacoes, /):
    # Implementação...
    pass

@log_transacao("SAQUE")
def sacar(*, saldo, valor, ...):
    # Implementação...
    pass
```

**Saída:**
```
[LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
=== Depósito realizado com sucesso! ===
```

**Conceitos aplicados:**
- ✅ Closures (função dentro de função)
- ✅ Decoradores com parâmetros
- ✅ `@wraps` para preservar metadados
- ✅ Captura de data/hora com `datetime.now()`

---

### 2. Gerador de Relatórios (`gerar_relatorio_transacoes`)

**Tipo:** Função geradora

**Localização:** Linhas 39-54 do `main.py`

**Função:**
```python
def gerar_relatorio_transacoes(conta, tipo_filtro=None):
    """
    Gerador que permite iterar sobre as transações de uma conta.
    Retorna uma a uma as transações realizadas.
    
    Args:
        conta: Dicionário da conta
        tipo_filtro: Opcional - "deposito", "saque" ou None
    
    Yields:
        Transação formatada
    """
    if "transacoes" not in conta or not conta["transacoes"]:
        return
    
    for transacao in conta["transacoes"]:
        if tipo_filtro is None or transacao["tipo"] == tipo_filtro:
            yield transacao
```

**Uso:**
```python
# Todas as transações
for transacao in gerar_relatorio_transacoes(conta):
    print(f"{transacao['data_hora_str']} - R$ {transacao['valor']}")

# Apenas depósitos
for transacao in gerar_relatorio_transacoes(conta, "deposito"):
    print(f"Depósito: R$ {transacao['valor']}")

# Apenas saques
for transacao in gerar_relatorio_transacoes(conta, "saque"):
    print(f"Saque: R$ {transacao['valor']}")
```

**Conceitos aplicados:**
- ✅ Keyword argument opcional (`tipo_filtro=None`)
- ✅ Declaração `yield` (lazy evaluation)
- ✅ Filtragem dentro do gerador
- ✅ Iteração eficiente em memória

---

### 3. Iterador de Contas (`ContaIterador`)

**Tipo:** Classe iteradora

**Localização:** Linhas 24-47 do `main.py`

**Classe:**
```python
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
```

**Uso:**
```python
iterador = ContaIterador(contas)

for info_conta in iterador:
    print(f"Conta: {info_conta['numero']}")
    print(f"Saldo: R$ {info_conta['saldo']:.2f}")
```

**Conceitos aplicados:**
- ✅ Método `__iter__()` (retorna self)
- ✅ Método `__next__()` (retorna items)
- ✅ `StopIteration` para terminação
- ✅ Estado interno (`_index`)
- ✅ Cálculo dinâmico (saldo a partir de transações)

---

### 4. Estrutura de Transações com Data/Hora

**Localização:** `conta["transacoes"]`

**Estrutura:**
```python
transacao = {
    "tipo": "deposito",                    # ou "saque"
    "valor": 1000.00,                      # Valor em float
    "data_hora": datetime(...),            # Objeto datetime
    "data_hora_str": "06/04/2026 14:35:22",  # String formatada
    "saldo_apos": 1000.00                  # Saldo após transação
}
```

**Criação (em `depositar()`):**
```python
agora = datetime.now()
data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")

transacao = {
    "tipo": "deposito",
    "valor": valor,
    "data_hora": agora,
    "data_hora_str": data_hora,
    "saldo_apos": saldo
}
transacoes.append(transacao)
```

**Conceitos aplicados:**
- ✅ `datetime.now()` para capturar momento exato
- ✅ `strftime()` para formatação em string
- ✅ Armazenamento em ambas as formas
- ✅ Rastreamento de saldo após cada transação

---

### 5. Limite de 10 Transações Diárias

**Implementação no `main()`:**

```python
# Variáveis de controle
transacoes_hoje = 0          # Contador do dia
data_transacoes = date.today()  # Data das transações

# No loop principal:
# Verificar se precisa resetar (novo dia)
if transacoes_hoje > 0 and date.today() != data_transacoes:
    data_transacoes = date.today()
    transacoes_hoje = 0
    numero_saques = 0
    print("\n[INFO] Novo dia! Contadores resetados.")

# Na função sacar():
excedeu_transacoes_dia = transacoes_hoje >= 10

if excedeu_transacoes_dia:
    print("\n@@@ Operação falhou! Você excedeu o número de transações...")
else:
    # Executar saque
    transacoes_hoje += 1

```

**Conceitos aplicados:**
- ✅ `date.today()` para data do sistema
- ✅ Comparação de datas para reset automático
- ✅ Validação antes da transação
- ✅ Incremento do contador após sucesso

---

## 📝 Exemplos de Código

### Exemplo 1: Usar Decorador e Transação

```python
# O decorador é transparente ao usuário
valor = 1000.0
saldo, extrato, transacoes = depositar(
    saldo=0, 
    valor=valor, 
    extrato="", 
    transacoes=[]
)

# Saída:
# [LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
# === Depósito realizado com sucesso! ===
```

### Exemplo 2: Iterar Sobre Contas

```python
contas = [
    {
        "agencia": "0001",
        "numero_conta": 1,
        "usuario": {"nome": "João"},
        "transacoes": [...]
    },
    {
        "agencia": "0001",
        "numero_conta": 2,
        "usuario": {"nome": "Maria"},
        "transacoes": [...]
    }
]

# Usar iterador
for info in ContaIterador(contas):
    print(f"Conta {info['numero']}: {info['titular']}")
    print(f"Saldo: R$ {info['saldo']:.2f}")
```

### Exemplo 3: Gerar Relatório Filtrado

```python
conta = {
    "usuario": {"nome": "João"},
    "transacoes": [
        {"tipo": "deposito", "valor": 1000.0, ...},
        {"tipo": "saque", "valor": 150.0, ...},
        {"tipo": "deposito", "valor": 500.0, ...},
    ]
}

# Apenas saques
print("SAQUES REALIZADOS:")
for i, trans in enumerate(gerar_relatorio_transacoes(conta, "saque"), 1):
    print(f"{i}. R$ {trans['valor']:.2f}")

# Saída:
# SAQUES REALIZADOS:
# 1. R$ 150.00
```

---

## 🔄 Fluxo de Execução

### Fluxo de Depósito (com Decorador)

```
┌─ [de] Depositar
│
├─ Entrada: Valor do depósito
│
├─ @log_transacao("DEPÓSITO") ← DECORADOR ATIVA
│  │
│  ├─ Registra: [LOG] 06/04/2026 14:35:22 - DEPÓSITO
│  │
│  └─ Chama depositar()
│     │
│     ├─ Valida valor > 0
│     ├─ Cria objeto datetime.now()
│     ├─ Formata data/hora com strftime()
│     ├─ Cria dicionário transacao
│     ├─ Adiciona à lista transacoes
│     ├─ Atualiza saldo
│     ├─ Imprime sucesso
│     │
│     └─ Retorna (saldo, extrato, transacoes)
│
├─ Atualiza conta_ativa["transacoes"]
├─ Incrementa transacoes_hoje
│
└─ Volta ao menu
```

### Fluxo de Saque (com Limite Diário)

```
┌─ [sa] Sacar
│
├─ Entrada: Valor do saque
│
├─ Verifica mudança de dia → reseta contadores
│
├─ @log_transacao("SAQUE") ← DECORADOR ATIVA
│  │
│  ├─ Registra: [LOG] 06/04/2026 14:36:45 - SAQUE
│  │
│  └─ Chama sacar()
│     │
│     ├─ Valida transacoes_hoje < 10 ← LIMITE DIÁRIO
│     ├─ Valida: saldo suficiente, limite, saques/dia, valor > 0
│     │
│     ├─ Se todas validações OK:
│     │  ├─ Cria objeto datetime.now()
│     │  ├─ Formata data/hora
│     │  ├─ Cria dicionário transacao
│     │  ├─ Adiciona à lista transacoes
│     │  ├─ Atualiza saldo
│     │  ├─ Incrementa numero_saques
│     │  └─ Retorna valores atualizados + transacoes_hoje+1
│     │
│     └─ Se alguma validação falhar:
│        └─ Imprime erro específico
│
├─ Atualiza conta_ativa["transacoes"]
├─ Incrementa transacoes_hoje (se sucesso)
│
└─ Volta ao menu
```

### Fluxo de Relatório (com Gerador)

```
┌─ [rel] Relatório
│
├─ Pede: filtro (Todas/Depósitos/Saques)
│
├─ Chama exibir_relatorio(conta)
│  │
│  ├─ Chama gerar_relatorio_transacoes(conta, filtro)
│  │
│  ├─ Gerador:
│  │  ├─ Itera sobre conta["transacoes"]
│  │  ├─ Yield cada transação que passa no filtro
│  │  ├─ (Execução lazy - não carrega tudo na memória)
│  │  └─ Stop quando termina
│  │
│  ├─ For loop consome o gerador
│  │  ├─ Formata cada transação
│  │  ├─ Imprime com data/hora
│  │  └─ Mostra saldo após cada uma
│  │
│  └─ Fecha com footer
│
└─ Volta ao menu
```

### Fluxo de Iterador de Contas

```
┌─ [it] Iterador
│
├─ Chama exibir_iterador_contas(contas)
│
├─ Cria ContaIterador(contas)
│
├─ For loop com iterador:
│  │
│  └─ Para cada iteração:
│     │
│     ├─ Chama __next__()
│     │  │
│     │  ├─ Verifica if _index >= len(contas)
│     │  │  └─ Se SIM: raise StopIteration (encerra)
│     │  │
│     │  ├─ Pega conta em contas[_index]
│     │  ├─ Calcula saldo (somando transacoes)
│     │  ├─ Cria dict com: agencia, numero, titular, saldo
│     │  ├─ Incrementa _index
│     │  └─ Retorna dict
│     │
│     ├─ No for loop: recebe dict
│     ├─ Formata e imprime informações
│     └─. Próxima iteração
│
└─ Volta ao menu
```

---

## 💡 Casos de Uso

### Caso 1: Auditoria de Transações

**Problema:** Auditor precisa ver todas as transações com data/hora

```python
# Usa Gerador + Data/Hora
for trans in gerar_relatorio_transacoes(conta):
    print(f"{trans['data_hora_str']} | {trans['tipo']:8} | {trans['valor']}")
    
# Saída:
# 06/04/2026 14:35:22 | deposito | 1000.00
# 06/04/2026 14:36:45 | saque    | 150.00
```

### Caso 2: Análise de Contas do Banco

**Problema:** Gerente precisa ver todas as contas com seus saldos

```python
# Usa Iterador + Cálculo Dinâmico
for conta_info in ContaIterador(contas):
    if conta_info['saldo'] > 1000:
        print(f"⭐ {conta_info['titular']}: R$ {conta_info['saldo']}")

# Saída:
# ⭐ Maria Santos: R$ 2000.00
# ⭐ João Silva: R$ 1500.00
```

### Caso 3: Rastreamento de Fraude

**Problema:** Sistema precisa registrar cada transação com precisão

```python
# Usa Decorador + Data/Hora + Limite Diário
# Decorador registra: [LOG] 06/04/2026 14:35:22 - SAQUE
# Data/Hora exata capturada
# Limite previne abuso (máx 10 transações/dia)

# Resultado: Trilha de auditoria completa!
```

### Caso 4: Relatórios Personalizados

**Problema:** Cliente quer ver apenas seus depósitos

```python
# Usa Gerador com filtro
print("Meus depósitos:")
for trans in gerar_relatorio_transacoes(minha_conta, "deposito"):
    print(f"+ R$ {trans['valor']:.2f} em {trans['data_hora_str']}")

# Saída:
# Meus depósitos:
# + R$ 1000.00 em 06/04/2026 14:35:22
# + R$ 500.00 em 06/04/2026 15:00:10
```

### Caso 5: Controle de Limite

**Problema:** Prevenir abuso com muitas transações

```python
# No loop principal:
if date.today() != data_transacoes:
    transacoes_hoje = 0  # Reset automático
    print("[INFO] Novo dia! Limite resetado")

# Na validação de saque:
if transacoes_hoje >= 10:
    print("❌ Limite diário atingido")

# Resultado: Segurança contra abuso automática!
```

---

## 🎓 Conceitos de Programação Exercitados

| Conceito | Localização | Descrição |
|----------|-------------|-----------|
| Decoradores | `@log_transacao` | Funcionalidade adicional sem modificar função original |
| Geradores | `gerar_relatorio_transacoes` | Economia de memória com `yield` |
| Iteradores | `ContaIterador` | Interface `__iter__` e `__next__` |
| Closures | Dentro de decorador | Função dentro de função |
| Data/Hora | `datetime`, `date` | Manipulação de tempo |
| List Comprehension | Filtros | Filtragem eficiente |
| Dicionários | Estrutura de dados | Dados estruturados |
| Listas | Container | Armazenamento de sequências |

---

## 🔐 Segurança e Validações

✅ **Implementadas:**
- Decorador registra cada operação (trilha de auditoria)
- Limite de 10 transações previne DDoS de transações
- Data/hora precisa para rastreamento
- Estrutura imutável de transações (histórico não pode ser alterado após criado)

---

## 📊 Performance

| Operação | Complexidade | Benefício |
|----------|-------------|-----------|
| Gerador (yield) | O(1) memória | Não carrega todas as transações |
| Iterador | O(n) tempo | Percorre contas uma a uma |
| Cálculo de saldo | O(n) tempo | Sempre atualizado a partir do histórico |
| Filtro de tipo | O(n) comparações | Eficiente com `if` no generator |

---

**Desenvolvido para:** Trilha Python DIO  
**Versão:** 3.0  
**Conceitos:** Decoradores, Geradores, Iteradores, Data/Hora  
**Status:** ✅ Implementação Completa e Testada
