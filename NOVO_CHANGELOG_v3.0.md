# 🎉 Changelog v3.0 - Iteradores, Geradores e Decoradores

## 📌 Resumo das alterações

O sistema bancário foi completamente transformado com a implementação de novos conceitos do curso:
- ✅ Decoradores de Log para todas as transações
- ✅ Gerador de Relatórios com filtros
- ✅ Iterador Personalizado para contas
- ✅ Registro de data/hora em todas as transações
- ✅ Limite de 10 transações diárias por conta

---

## 🚀 Novas Funcionalidades (v3.0)

### 1. **Decorador de Log** (`@log_transacao`)

Um decorador que registra automaticamente a data, hora e tipo de cada transação banking.

**Como funciona:**
- Aplicado às funções `depositar()` e `sacar()`
- Imprime: `[LOG] DD/MM/YYYY HH:MM:SS - Transação: [TIPO]`
- Registra antes da execução da transação

**Exemplo de saída:**
```
[LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
=== Depósito realizado com sucesso! ===
```

---

### 2. **Gerador de Relatórios** (`gerar_relatorio_transacoes()`)

Um gerador que permite iterar sobre transações com opção de filtros.

**Como funciona:**
```python
# Aceita tiposde filtro:
# - None: retorna todas as transações
# - "deposito": retorna apenas depósitos
# - "saque": retorna apenas saques
```

**Uso:**
```python
# Iterar sobre transações
for transacao in gerar_relatorio_transacoes(conta, tipo_filtro="deposito"):
    print(transacao["valor"])  # Valor da transação
    print(transacao["data_hora_str"])  # Data/hora
    print(transacao["saldo_apos"])  # Saldo após a transação
```

**Opção [rel] - Relatório Interativo:**
- Menu para escolher filtro (Todas, Depósitos, Saques)
- Exibe transações uma a uma com detalhes
- Mostra data/hora, valor e saldo após cada transação

**Exemplo de saída:**
```
================ RELATÓRIO DE TRANSAÇÕES ================
Conta: 1 | Titular: João da Silva

1. [06/04/2026 14:35:22] DEPÓSITO
   Valor: R$ 1000.00
   Saldo após: R$ 1000.00

2. [06/04/2026 14:36:45] SAQUE
   Valor: R$ 150.00
   Saldo após: R$ 850.00
```

---

### 3. **Iterador de Contas** (`ContaIterador`)

Um iterador personalizado que permite iterar sobre todas as contas do banco.

**Classe:**
```python
class ContaIterador:
    def __init__(self, contas)
    def __iter__(self)
    def __next__(self)  # Retorna dict com: agencia, numero, titular, saldo
```

**Informações retornadas:**
```python
{
    "agencia": "0001",
    "numero": 1,
    "titular": "João da Silva",
    "saldo": 850.00
}
```

**Opção [it] - Iterador de Contas:**
- Lista todas as contas do banco
- Calcula saldo de cada conta (somando transações)
- Mo stra agência, número, titular e saldo

**Exemplo de saída:**
```
================ ITERADOR DE CONTAS BANCÁRIAS ================

1. Conta #1
   Agência: 0001
   Titular: João da Silva
   Saldo Atual: R$ 850.00
------------------------------------------------------------

2. Conta #2
   Agência: 0001
   Titular: Maria Santos
   Saldo Atual: R$ 1500.00
------------------------------------------------------------
```

---

### 4. **Data e Hora em Transações**

Todas as transações agora registram data e hora precisas.

**Estrutura de transação:**
```python
transacao = {
    "tipo": "deposito",          # ou "saque"
    "valor": 1000.00,
    "data_hora": datetime(2026, 4, 6, 14, 35, 22),  # Objeto datetime
    "data_hora_str": "06/04/2026 14:35:22",         # String formatada
    "saldo_apos": 1000.00
}
```

**No extrato:**
```
[06/04/2026 14:35:22] Depósito:         R$ 1000.00
[06/04/2026 14:36:45] Saque:            R$ 150.00
```

**Resetamento do contador:**
- Contador de transações reseta automaticamente quando muda de dia
- Contador de saques também reseta a cada novo dia
- Mantém histórico completo de todas as transações

---

### 5. **Limite de 10 Transações Diárias**

Novo limite implementado para controlar transações diárias.

**Como funciona:**
- Cada conta pode fazer **máximo 10 transações por dia**
- Depósitos e saques contam para o limite
- Contador reseta automaticamente à meia-noite
- Mensagem de erro ao exceder limite:
  ```
  @@@ Operação falhou! Você excedeu o número de transações 
  permitidas para hoje (máximo 10). @@@
  ```

**Implementação:**
- Variável `transacoes_hoje` rastreia transações do dia
- Variável `data_transacoes` armazena a data das transações
- Sistema verifica se mudou de dia toda vez que uma operação é executada

---

## 📋 Menu Atualizado (v3.0)

```
================ MENU ================
[de]     Depositar                    ← Com decorador de log
[sa]     Sacar                        ← Com limite de 10 trans/dia
[ex]     Extrato                      ← Com data/hora
[nc]     Nova conta                   ← Inicializa transações
[lc]     Listar contas                ← Lista todas
[lu]     Listar usuários com contas   ← Mostra relação
[rel]    Relatório de transações ⭐  ← Novo: Usa gerador
[it]     Iterador de contas       ⭐  ← Novo: Usa iterador
[nu]     Novo usuário
[qt]     Sair
=> 
```

---

## 🎓 Conceitos Educacionais Aplicados

### Decoradores
- **`@log_transacao(tipo)`**: Decorador parametrizado que:
  - Registra informações antes da execução
  - Preserva metadados da função original com `@wraps`
  - Demonstra padrão decorator com parâmetros

### Geradores
- **`gerar_relatorio_transacoes(conta, tipo_filtro)`**: Função geradora que:
  - Usa `yield` para retornar transações uma a uma
  - Suporta filtros opcionais
  - Implementa padrão lazy evaluation

### Iteradores
- **`ContaIterador`**: Classe iteradora que:
  - Implementa `__iter__()` e `__next__()`
  - Mantém estado interno com `_index`
  - Levanta `StopIteration` quando termina
  - Calcula saldo dinâmico de cada conta

### Data e Hora
- **`datetime`**: Módulo para gerenciar data/hora
  - `datetime.now()`: Captura momento exato
  - `date.today()`: Obtém data do sistema
  - `strftime()`: Formata para string legível

---

## 📊 Exemplo Completo de Sessão

### 1️⃣ Criar usuário
```
[nu] Novo usuário
CPF: 12345678901
Nome: João da Silva
Data: 15/08/1990
Endereço: Rua X, 100 - Centro - São Paulo/SP - 01310-100
```

### 2️⃣ Criar conta (ativa automaticamente)
```
[nc] Nova conta
CPF: 12345678901
→ Conta criada e ativa
```

### 3️⃣ Depositar (com log)
```
[de] Depositar
Valor: 1000
[LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
=== Depósito realizado com sucesso! ===
```

### 4️⃣ Sacar (com log e limite)
```
[sa] Sacar
Valor: 150
[LOG] 06/04/2026 14:36:45 - Transação: SAQUE
=== Saque realizado com sucesso! ===
```

### 5️⃣ Ver extrato detalhado (com data/hora)
```
[ex] Extrato
Histórico detalhado de transações:

1. [06/04/2026 14:35:22] DEPÓSITO
   Valor: R$ 1000.00
   Saldo após transação: R$ 1000.00

2. [06/04/2026 14:36:45] SAQUE
   Valor: R$ 150.00
   Saldo após transação: R$ 850.00

Saldo: R$ 850.00
```

### 6️⃣ Gerar relatório (com filtro)
```
[rel] Relatório
[1] Todas  [2] Depósitos  [3] Saques
→ Escolhe e vê transações filtradas com gerador
```

### 7️⃣ Usar iterador de contas
```
[it] Iterador
1. Conta #1 - João da Silva - R$ 850.00
2. Conta #2 - Maria Santos - R$ 1500.00
```

---

## 🛡️ Recursos de Segurança e Validação

✅ **Mantidos da v2.1:**
- Validação de CPF com algoritmo módulo 11
- Validação de endereço com normalização
- Verificação de CPF duplicado
- Limite de saque por transação
- Limite de saques por dia (3 saques)

✅ **Novos (v3.0):**
- Limite de 10 transações por dia
- Registro data/hora de cada transação
- Contra ativação automática de conta
- Resetamento automático de contadores

---

## 🧪 Como Testar

### Teste 1: Decorador de Log
1. Abra o programa
2. Crie usuário [nu]
3. Crie conta [nc]
4. Faça depósito [de] → Verá `[LOG] DD/MM/YYYY HH:MM:SS - DEPÓSITO`

### Teste 2: Data e Hora no Extrato
1. Faça 3 transações (depósito, saque, depósito)
2. Veja extrato [ex]
3. Verá cada transação com `[DD/MM/YYYY HH:MM:SS]`

### Teste 3: Limite de 10 Transações
1. Tente fazer 11 transações no mesmo dia
2. Na 11ª transação, receberá erro de limite excedido
3. Mude a data do sistema e teste novamente (contador reseta)

### Teste 4: Gerador de Relatórios
1. Crie conta e faça transações variadas
2. Selecione [rel]
3. Teste filtros: Todas, Depósitos, Saques
4. Verás o gerador retornando transações uma a uma

### Teste 5: Iterador de Contas
1. Crie 2 ou 3 contas com usuários diferentes
2. Faça transações em cada uma
3. Selecione [it] → Iterador descreverá cada conta com saldo calculado

---

## 🔄 Conversão da Sessão Anterior

⚠️ **Importante**: A v3.0 resetou o saldo anterior porque agora o saldo é **calculado dinamicamente** a partir do histórico de transações:

**v2.0 (antes):**
```python
saldo = 0  # Variável global
```

**v3.0 (agora):**
```python
conta["transacoes"] = [...]  # Histórico completo
# Saldo = soma de depósitos - saque
```

Isso torna o sistema mais robusto e permite histórico permanente!

---

## 📌 Estrutura de Dados Atualizada

### Conta (v3.0)
```python
conta = {
    "agencia": "0001",
    "numero_conta": 1,
    "usuario": {...},          # Referência ao usuário
    "transacoes": [...],       # ⭐ Novo: Lista de transações
    "data_criacao": datetime   # ⭐ Novo: Quando foi criada
}
```

### Transação (novo em v3.0)
```python
transacao = {
    "tipo": "deposito",        # ou "saque"
    "valor": 1000.00,
    "data_hora": datetime(...),
    "data_hora_str": "06/04/2026 14:35:22",
    "saldo_apos": 1000.00
}
```

---

## ✨ Próximas Melhorias Sugeridas (v4.0)

- [ ] Persistência em banco de dados (SQLite)
- [ ] Autenticação com senha
- [ ] Exportar extrato em PDF
- [ ] Calendário de transações
- [ ] Análise de gastos por período
- [ ] Notificações de limite próximo
- [ ] Multi-threading para operações assíncronas

---

## 📝 Notas Importantes

1. **Conta Ativa**: O sistema agora rastreia qual conta está ativa depois de criar
2. **Contador Diário**: Reseta automáticamente à meia-noite
3. **Histórico Permanente**: Todas as transações ficam registradas na conta
4. **Saldo Dinâmico**: Calculado a partir do histórico de transações

---

**Desenvolvido para:** Trilha Python DIO  
**Versão:** 3.0  
**Data:** Abril de 2026  
**Status:** ✅ Completo com Decoradores, Geradores e Iteradores
