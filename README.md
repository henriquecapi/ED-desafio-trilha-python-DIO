# 🏦 Sistema Bancário Python v4.0

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Completo-brightgreen.svg)
![Versão](https://img.shields.io/badge/Versão-4.0-orange.svg)

## 📌 Bem-vindo

Sistema Bancário Python com **persistência automática de dados em CSV**. Dados salvos em uma execução são carregados na próxima, sem perda de informações.

---

## ✨ Principais Características

- ✅ **Persistência em CSV** - Dados salvos automaticamente
- ✅ **Menu Adaptativo** - Interface muda conforme o estado do sistema
- ✅ **Login por Conta** - Autenticação inteligente por banco
- ✅ **Isolamento Total** - Cada conta com dados independentes
- ✅ **Histórico Completo** - Todas transações com data/hora
- ✅ **Validações Robustas** - CPF, endereço, limites
- ✅ **Relatórios Filtrados** - Por tipo de transação
- ✅ **Padrões Avançados** - Decoradores, Iteradores, Geradores

---

## 🚀 Quick Start

### 1. Executar
```bash
python main_v4.0.py
```

### 2. Primeira Execução
```
[nu] → Criar usuário
[nc] → Criar conta
[qt] → Sair
```
Arquivos CSV serão criados automaticamente!

### 3. Próximas Execuções
```
[lg] → Login (dados carregados!)
[de] → Depositar
[sa] → Sacar
[ex] → Extrato
... mais opções
```

### 4. Testar
```bash
python test_v4.0.py
```

---

## 📋 Menu Completo

| Opção | Descrição | Disponível em |
|-------|-----------|---------------|
| `[nu]` | Novo usuário | Sempre |
| `[nc]` | Nova conta | Sempre |
| `[lg]` | Login na conta | Quando houver contas |
| `[de]` | Depositar | Com conta ativa |
| `[sa]` | Sacar | Com conta ativa |
| `[ex]` | Extrato | Com conta ativa |
| `[rel]` | Relatório de transações | Com conta ativa |
| `[lc]` | Listar contas | Sempre |
| `[lu]` | Listar usuários | Sempre |
| `[it]` | Iterador de contas | Sempre |
| `[qt]` | Sair | Sempre |

---

## 💻 Exemplo de Uso

```bash
$ python main_v4.0.py

[nu] → João Silva (CPF: 12345678901)
[nc] → Conta criada para João
[de] → Depositar R$ 100.00 ✓
[ex] → Mostra transações e saldo
[qt] → Sair (dados salvos!)

$ python main_v4.0.py (2ª execução)

[lg] → CPF: 12345678901
     → Seleciona conta
     → Saldo R$ 100.00 ✓ (dados carregados!)
```

---

## 📂 Arquivos

### Código
- **main_v4.0.py** - Programa principal (~700 linhas)
- **csv_manager.py** - Gerenciador de persistência (~250 linhas)

### Testes
- **test_v4.0.py** - Validação automática

### Dados (criados na execução)
- **usuarios.csv** - Usuários cadastrados
- **contas.csv** - Contas criadas
- **transacoes.csv** - Histórico de transações

---

## 📊 Estrutura de Dados

### usuarios.csv
```csv
cpf,nome,data_nascimento,endereco
12345678901,João Silva,01/01/1990,Rua A, 100 - Centro - SP/SP - 12345-678
```

### contas.csv
```csv
cpf,agencia,numero_conta,data_criacao,saldo
12345678901,0001,1,10/04/2026 15:30:00,100.00
```

### transacoes.csv
```csv
cpf,numero_conta,tipo,valor,data_hora,saldo_apos
12345678901,1,deposito,100.00,10/04/2026 15:35:00,100.00
12345678901,1,saque,30.00,10/04/2026 16:00:00,70.00
```

---

## 🏗️ Arquitetura

```
┌────────────────────┐
│  Apresentação      │  Menu, Input/Output
├────────────────────┤
│  Lógica de Negócio │  Depositar, Sacar, Login
├────────────────────┤
│  Persistência      │  csv_manager.py
├────────────────────┤
│  Armazenamento     │  CSV Files
└────────────────────┘
```

### Padrões de Design Utilizados
- **Decorator:** `@log_transacao` - Registra operações
- **Iterator:** `ContaIterador` - Itera sobre contas
- **Generator:** `gerar_relatorio_transacoes` - Lazy loading
- **Facade:** `csv_manager` - Abstração de acesso aos dados

---

## ✅ Validações Implementadas

| Validação | Detalhes |
|-----------|----------|
| **CPF** | Algoritmo brasileiro (11 dígitos, dígitos verificadores) |
| **Endereço** | Formato: `Rua, número - Bairro - Cidade/UF - CEP` |
| **Valores** | Devem ser > 0 |
| **Limite Saque** | R$ 500 máximo |
| **Saques/Dia** | Máximo 3 saques |
| **Transações/Dia** | Máximo 10 por dia |
| **Saldo** | Deve ser suficiente para saques |
| **CPF Único** | Não permite duplicação |

---

## 🧪 Testes

O arquivo `test_v4.0.py` valida:
- ✅ Criação de CSVs
- ✅ Adição de usuários
- ✅ Carregamento de dados
- ✅ Detecção de CPF duplicado
- ✅ Adição de contas
- ✅ Adição de transações
- ✅ Cálculo de saldo
- ✅ Carregamento de transações

**Executar:**
```bash
python test_v4.0.py
```

---

## 📈 Comparação com v3.0

| Feature | v3.0 | v4.0 |
|---------|------|------|
| Persistência | ❌ | ✅ |
| Menu Adaptativo | ❌ | ✅ |
| Login por Conta | ❌ | ✅ |
| CSV | ❌ | ✅ |
| Histórico | ✅ | ✅ |
| Validações | ✅ | ✅ |
| Decoradores | ✅ | ✅ |
| Iteradores | ✅ | ✅ |
| Geradores | ✅ | ✅ |

---

## 🔒 Segurança & Proteções

- ✅ **Atomicidade** - Transações completas ou nenhuma
- ✅ **Integridade Referencial** - Chaves estrangeiras validadas
- ✅ **Consistência** - Saldo sempre calculado das transações
- ✅ **Isolamento** - Cada conta independente
- ✅ **UTF-8 Encoding** - Suporta caracteres acentuados

---

## 💡 Exemplos Práticos

### Criar Usuário
```bash
[nu] → CPF: 12345678901
    → Nome: João Silva
    → Data: 01/01/1990
    → Endereço: Rua A, 100 - Centro - São Paulo/SP - 12345-678
    → ✓ Usuário criado em usuarios.csv
```

### Fazer Login
```bash
[lg] → CPF: 12345678901
    → [1] Agência 0001 | Conta 1 | Saldo R$ 100.00
    → [2] Agência 0001 | Conta 2 | Saldo R$ 250.00
    → Seleciona: 1
    → ✓ Acesso liberado
```

### Depositar
```bash
[de] → Valor: 50.00
    → ✓ Deposito adicionado em transacoes.csv
    → Novo saldo: R$ 150.00
```

### Ver Extrato
```bash
[ex] → Mostra todas as transações com:
       - Data/Hora
       - Tipo (Depósito/Saque)
       - Valor
       - Saldo após transação
```

---

## ⚙️ Requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa
- Windows, macOS ou Linux

```bash
python --version
```

---

## 🐛 Troubleshooting

| Erro | Solução |
|------|---------|
| "Arquivo não encontrado" | Criado automaticamente na 1ª execução |
| "CPF inválido" | Verificar: 11 dígitos + algoritmo válido |
| "Endereço inválido" | Formato: `Rua, 100 - Bairro - Cidade/UF - CEP` |
| "Nenhuma conta" | Executar: `[nu]` depois `[nc]` |
| "Saldo insuficiente" | Fazer depósito antes de sacar |
| "Limite de saques" | Máximo 3 saques por conta |
| "Transações do dia" | Máximo 10 por dia |

---

## 📋 Requisitos do PRD (Implementados)

### Primeira Execução ✅
- [x] Criar arquivos CSV vazios
- [x] Menu com apenas opções de cadastro
- [x] Sem opções de login habilitadas
- [x] Usuários podem ser criados
- [x] Contas podem ser criadas

### Segunda Execução ✅
- [x] Carregar dados dos CSVs
- [x] Validar duplicação de CPF
- [x] Liberar login apenas com contas
- [x] Login por conta (CPF + seleção)
- [x] Menu completo disponível
- [x] Contas isoladas por usuário
- [x] Operações isoladas por conta

### Persistência ✅
- [x] `usuarios.csv` com CPF como chave
- [x] `contas.csv` com relacionamento por CPF
- [x] `transacoes.csv` com histórico
- [x] Integridade de dados garantida
- [x] Relacionamentos mantêm consistência

---

## 📊 Estatísticas

- **Linhas de Código:** ~950
- **Funções:** 30+
- **Operações:** 11
- **Arquivos CSV:** 3
- **Padrões de Design:** 4

---

## 🎯 Fluxo Principal

```
EXECUÇÃO
  ↓
Inicializar CSVs
  ↓
Dados existem?
  ├─ NÃO → Menu Primário ([nu], [nc], [qt])
  └─ SIM → Menu Completo ([lg], [de], [sa], ...)
  ↓
Processar Opção
  ↓
Salvar em CSV (se aplicável)
  ↓
Mostrar Resultado
  ↓
Loop para próxima operação
  ↓
[qt] → Sair (dados persistem!)
```

---

## 🚀 Começar Agora!

### Passo 1: Executar
```bash
python main_v4.0.py
```

### Passo 2: Criar Usuário
```
→ Digite: nu
→ Preencha dados do usuário
```

### Passo 3: Criar Conta
```
→ Digite: nc
→ Informe CPF do usuário
```

### Passo 4: Usar o Sistema
```
→ Digite: lg (login)
→ Realize operações normalmente
```

### Passo 5: Verificar Persistência
```
→ Feche o programa
→ Execute novamente
→ Seus dados estarão lá! ✓
```

---

## 📞 Como Usar Cada Opção

### [nu] Novo Usuário
- CPF (11 dígitos, validado)
- Nome completo
- Data de nascimento (dd/mm/yyyy)
- Endereço (Rua, num - Bairro - Cidade/UF - CEP)

### [nc] Nova Conta
- CPF do usuário
- Conta criada automaticamente
- Agência: 0001
- Número: auto-incrementado

### [lg] Login
- Informe seu CPF
- Selecione a conta desejada
- Acesso liberado para operações

### [de] Depositar
- Informe valor
- Depositado na conta ativa
- Saldo atualizado

### [sa] Sacar
- Informe valor
- Validações: saldo, limite, saques/dia, transações/dia
- Saque realizado se passou

### [ex] Extrato
- Mostra todas as transações
- Data, hora, tipo, valor, saldo
- Saldo final no final

### [rel] Relatório
- [1] Todas as transações
- [2] Apenas depósitos
- [3] Apenas saques
- Filtrado conforme seleção

### [lc] Listar Contas
- Mostra todas as contas
- Titular, agência, número, saldo

### [lu] Listar Usuários
- Mostra usuários e suas contas
- Com saldo de cada conta

### [it] Iterador
- Usa padrão Iterator
- Lista contas uma a uma

---

## 🎓 Conceitos Implementados

| Conceito | Onde | Como |
|----------|------|------|
| **Decoradores** | @log_transacao | Registra data/hora de operações |
| **Iteradores** | ContaIterador | Itera sobre contas bancárias |
| **Geradores** | gerar_relatorio_transacoes | Filtra transações dynamicamente |
| **CSV** | csv_manager.py | Persistência de dados |
| **Validações** | validar_cpf, normalizar_endereco | Robustez |
| **Data/Hora** | datetime | Timestamp em transações |
| **Dicts** | conta_ativa, transacao | Estrutura de dados |
| **Listas** | usuarios, contas, transacoes | Colecções |

---

## 💾 Fluxo de Persistência

```
Operação Realizada
  ↓
[nu] → adicionar_usuario_csv() → usuarios.csv
[nc] → adicionar_conta_csv() → contas.csv
[de] → adicionar_transacao_csv() → transacoes.csv
[sa] → adicionar_transacao_csv() → transacoes.csv
  ↓
Dados Salvos em CSV
  ↓
Próxima Execução
  ↓
carregar_usuarios() → Lista de usuários
carregar_contas() → Lista de contas
carregar_transacoes() → Carregadas sob demanda
  ↓
Sistema Restaurado!
```

---

## 🔄 Menu Adaptativo

### Primeira Execução (Sem Dados)
```
[nu] Novo usuário          ← Criar usuários
[nc] Nova conta            ← Criar contas
[qt] Sair

Operações bancárias DESABILITADAS
Login DESABILITADO
```

### Segunda Execução (Com Dados)
```
[nu] Novo usuário          ← Ainda disponível
[nc] Nova conta            ← Ainda disponível
[lg] Login na conta        ← ✨ HABILITADO
[de] Depositar             ← ✨ Requer login
[sa] Sacar                 ← ✨ Requer login
[ex] Extrato               ← ✨ Requer login
[rel] Relatório            ← ✨ Requer login
[lc] Listar contas         ← Ainda disponível
[lu] Listar usuários       ← Ainda disponível
[it] Iterador de contas    ← Ainda disponível
[qt] Sair
```

---

## ✨ Destaques Técnicos

### Cálculo de Saldo
```python
# Saldo é CALCULADO, não armazenado
saldo = sum(depositos) - sum(saques)
# Garante consistência absoluta
```

### Conta Ativa
```python
conta_ativa = {
    'cpf': '12345678901',
    'usuario': {...},
    'conta': {...},
    'numero_conta': 1
}
# Isolamento total de dados
```

### Transação com Timestamp
```python
transacao = {
    'cpf': '12345678901',
    'numero_conta': 1,
    'tipo': 'deposito',
    'valor': 100.00,
    'data_hora': '10/04/2026 15:35:00',
    'saldo_apos': 100.00
}
# Histórico completo e auditável
```

---

## 📈 Performance

| Operação | Complexidade | Observação |
|----------|-------------|-----------|
| novo_usuario | O(n) | Valida duplicação |
| nova_conta | O(n) | Obtém contas para número |
| depositar | O(n) | Calcula saldo |
| sacar | O(n) | Conta transações do dia |
| exibir_extrato | O(n) | Itera transações |
| login_conta | O(n) | Lista contas do usuário |

**Nota:** Adequado para datasets pequenos/médios. Para milhões de registros, considere banco de dados SQL.

---

## 🎯 Status Final

| Item | Status |
|------|--------|
| Código | ✅ Completo |
| Testes | ✅ Passando |
| Documentação | ✅ Completa |
| Requisitos PRD | ✅ 100% |
| Pronto para Uso | ✅ Sim |

---

## 🚀 Próximas Etapas

Sugestões para futuras versões:
- [ ] Autenticação com senha
- [ ] Banco de dados SQL
- [ ] API REST
- [ ] Interface gráfica
- [ ] Módulo de investimentos
- [ ] Relatórios PDF
- [ ] Backup automático
- [ ] Multi-usuário simultâneo

---

## 📄 Estrutura de Arquivos

```
00 - Desafio/
├── main_v4.0.py              ⭐ Programa
├── csv_manager.py            ⭐ Gerenciador
├── test_v4.0.py              ⭐ Testes
├── README.md                  ✨ Este arquivo
└── usuarios.csv, contas.csv, transacoes.csv (dinâmicos)
```

---

## ✅ Checklist de Uso

- [ ] Executei `python main_v4.0.py`
- [ ] Criei usuário com `[nu]`
- [ ] Criei conta com `[nc]`
- [ ] Fiz depósito com `[de]`
- [ ] Vi extrato com `[ex]`
- [ ] Fiz saque com `[sa]`
- [ ] Encerrei com `[qt]`
- [ ] Executei novamente e dados estavam lá ✓
- [ ] Rodei `python test_v4.0.py` e passou ✓

---

**Status:** ✅ Completo e Testado  
**Versão:** 4.0  
**Data:** 10 de Abril de 2026  
**Requisitos:** Python 3.8+

**Execute agora: `python main_v4.0.py` 🚀**
