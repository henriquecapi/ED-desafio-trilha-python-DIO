# 📚 INDEX v4.0 - Índice Completo

Navegação rápida de todos os arquivos, componentes e conceitos da v4.0.

---

## 📑 Índice de Conteúdos

1. [Arquivos do Projeto](#arquivos-do-projeto)
2. [Módulos Python](#módulos-python)
3. [Arquivos CSV](#arquivos-csv)
4. [Funções Principais](#funções-principais)
5. [Classes e Padrões](#classes-e-padrões)
6. [Operações do Menu](#operações-do-menu)
7. [Estrutura de Dados](#estrutura-de-dados)
8. [Decoradores e Geradores](#decoradores-e-geradores)
9. [Validações](#validações)
10. [Testes](#testes)
11. [Documentação](#documentação)
12. [Como Navegar](#como-navegar)

---

## 📂 Arquivos do Projeto

### Arquivos Principais

| Arquivo | Linhas | Descrição | Tipo |
|---------|--------|-----------|------|
| `main_v4.0.py` | ~700 | Programa principal com menu e lógica | Python (Código) |
| `csv_manager.py` | ~250 | Gerenciador de persistência | Python (Módulo) |
| `test_v4.0.py` | ~300 | Testes automatizados | Python (Testes) |
| `README.md` | ~900 | Documentação consolidada | Markdown |
| `CHANGELOG_v4.0.md` | ~500 | Mudanças vs v3.0 | Markdown |
| `INDEX_v4.0.md` | Este arquivo | Índice do projeto | Markdown |
| `FLUXOS_v4.0.md` | ~400 | Diagramas e fluxos | Markdown |

### Arquivos Dinâmicos (criados na execução)

| Arquivo | Descrição |
|---------|-----------|
| `usuarios.csv` | Usuários cadastrados |
| `contas.csv` | Contas bancárias |
| `transacoes.csv` | Histórico de transações |

### Pastas

| Pasta | Conteúdo |
|-------|----------|
| `PRDs/` | Especificações (PRD inicial) |
| `__pycache__/` | Cache Python (auto-gerado) |

---

## 🐍 Módulos Python

### main_v4.0.py
**Responsabilidade:** Interface com usuário e lógica de negócio

**Componentes:**
- [Decorador log_transacao](#log_transacao)
- [Classe ContaIterador](#contaiterador)
- [Função gerar_relatorio_transacoes](#gerar_relatorio_transacoes)
- [Menu Primário](#menu-primário)
- [Menu Adaptativo](#menu-dados-existentes)
- [Operações Bancárias](#operações-bancárias)

**Funções Públicas:** ~30

### csv_manager.py
**Responsabilidade:** Persistência e carregamento de dados

**Funções Principais:**
- [inicializar_csvs()](#inicializar_csvs)
- [Operações com Usuários](#operações-com-usuários-1)
- [Operações com Contas](#operações-com-contas)
- [Operações com Transações](#operações-com-transações)
- [Funções de Estado](#funções-de-estado)

**Funções Públicas:** ~15

---

## 💾 Arquivos CSV

### usuarios.csv

**Estrutura:**
```csv
cpf,nome,data_nascimento,endereco
12345678901,João Silva,01/01/1990,Rua A, 100 - Centro - SP/SP - 12345-678
```

**Colunas:**
| Coluna | Tipo | Requerido | Descrição |
|--------|------|-----------|-----------|
| `cpf` | String | ✅ Sim | Chave primária (11 dígitos) |
| `nome` | String | ✅ Sim | Nome completo do usuário |
| `data_nascimento` | String | ✅ Sim | Formato: dd/mm/yyyy |
| `endereco` | String | ✅ Sim | Formato: Rua, num - Bairro - Cidade/UF - CEP |

---

### contas.csv

**Estrutura:**
```csv
cpf,agencia,numero_conta,data_criacao,saldo
12345678901,0001,1,10/04/2026 15:30:00,100.00
```

**Colunas:**
| Coluna | Tipo | Requerido | Descrição |
|--------|------|-----------|-----------|
| `cpf` | String | ✅ Sim | FK para usuarios.csv |
| `agencia` | String | ✅ Sim | Sempre "0001" |
| `numero_conta` | String | ✅ Sim | Auto-incrementado |
| `data_criacao` | String | ✅ Sim | dd/mm/yyyy HH:MM:SS |
| `saldo` | Decimal | ❌ Não | Calculado (depreciado) |

---

### transacoes.csv

**Estrutura:**
```csv
cpf,numero_conta,tipo,valor,data_hora,saldo_apos
12345678901,1,deposito,100.00,10/04/2026 15:35:00,100.00
12345678901,1,saque,30.00,10/04/2026 16:00:00,70.00
```

**Colunas:**
| Coluna | Tipo | Requerido | Descrição |
|--------|------|-----------|-----------|
| `cpf` | String | ✅ Sim | FK para usuarios.csv |
| `numero_conta` | String | ✅ Sim | FK para contas.csv |
| `tipo` | String | ✅ Sim | "deposito" ou "saque" |
| `valor` | Decimal | ✅ Sim | Valor da transação |
| `data_hora` | String | ✅ Sim | dd/mm/yyyy HH:MM:SS |
| `saldo_apos` | Decimal | ✅ Sim | Saldo após transação |

---

## 🔧 Funções Principais

### Em csv_manager.py

#### inicializar_csvs()
**Assinatura:** `inicializar_csvs() -> None`

**Descrição:** Cria os 3 arquivos CSV se não existirem

**Quando é chamada:** Na inicialização de main_v4.0.py (início da execução)

**Efeito:** Cria `usuarios.csv`, `contas.csv`, `transacoes.csv` vazios com headers

**Exemplo:**
```python
inicializar_csvs()  # Cria os CSVs na primeira execução
```

---

#### Operações com Usuários

**carregar_usuarios()**
```python
def carregar_usuarios() -> list[dict]
```
Carrega todos os usuários de usuarios.csv

---

**adicionar_usuario_csv(cpf, nome, data_nascimento, endereco)**
```python
def adicionar_usuario_csv(cpf, nome, data_nascimento, endereco) -> bool
```
Adiciona novo usuário em usuarios.csv

---

**usuario_existe(cpf)**
```python
def usuario_existe(cpf) -> bool
```
Verifica se usuário com CPF existe

---

**obter_usuario(cpf)**
```python
def obter_usuario(cpf) -> dict | None
```
Retorna dados completos do usuário ou None

---

#### Operações com Contas

**carregar_contas()**
```python
def carregar_contas() -> list[dict]
```
Carrega todas as contas de contas.csv

---

**adicionar_conta_csv(cpf, agencia, numero_conta, data_criacao)**
```python
def adicionar_conta_csv(cpf, agencia, numero_conta, data_criacao) -> bool
```
Adiciona nova conta em contas.csv

---

**obter_contas_do_usuario(cpf)**
```python
def obter_contas_do_usuario(cpf) -> list[dict]
```
Retorna lista de contas de um usuário

---

**atualizar_saldo_conta(cpf, numero_conta, novo_saldo)**
```python
def atualizar_saldo_conta(cpf, numero_conta, novo_saldo) -> None
```
Atualiza saldo em contas.csv (depreciado em favor de cálculo)

---

#### Operações com Transações

**adicionar_transacao_csv(cpf, numero_conta, tipo, valor, data_hora, saldo_apos)**
```python
def adicionar_transacao_csv(cpf, numero_conta, tipo, valor, data_hora, saldo_apos) -> bool
```
Registra nova transação em transacoes.csv

---

**obter_transacoes_conta(cpf, numero_conta)**
```python
def obter_transacoes_conta(cpf, numero_conta) -> list[dict]
```
Retorna transações de uma conta

---

**obter_saldo_conta(cpf, numero_conta)**
```python
def obter_saldo_conta(cpf, numero_conta) -> float
```
**IMPORTANTE:** Calcula saldo retornando soma de depósitos - saques

---

#### Funções de Estado

**dados_existem()**
```python
def dados_existem() -> bool
```
Verifica se há dados em usuarios.csv (+ 1 usuário)

---

**contas_existem()**
```python
def contas_existem() -> bool
```
Verifica se há contas em contas.csv

---

### Em main_v4.0.py

**novo_usuario()**
- Cria novo usuário com validações
- Salva em usuarios.csv

**nova_conta()**
- Cria nova conta para usuário existente
- Salva em contas.csv

**depositar()**
- Adiciona valor à conta
- Registra em transacoes.csv

**sacar()**
- Remove valor da conta
- Valida limite, saques/dia, transações/dia
- Registra em transacoes.csv

**exibir_extrato()**
- Mostra histórico de transações
- Carregado de transacoes.csv

**login_conta()**
- Autentica usuário
- Seleciona conta
- Habilita operações

---

## 🎓 Classes e Padrões

### ContaIterador

**Localização:** main_v4.0.py, linhas ~45-65

**Padrão:** Iterator

**Descrição:** Permite iterar sobre contas bancárias uma a uma

**Métodos:**
- `__init__(contas: list)` - Inicializa com lista de contas
- `__iter__()` - Retorna iterador
- `__next__()` - Retorna próxima conta

**Uso:**
```python
contas = carregar_contas()
iterador = ContaIterador(contas)
for conta in iterador:
    print(f"{conta['titular']} - Saldo: R$ {conta['saldo']:.2f}")
```

**Retorna:**
```python
{
    "agencia": "0001",
    "numero": 1,
    "titular": "João Silva",
    "saldo": 100.00
}
```

---

## 🎪 Operações do Menu

### Menu Primeira Execução

| Atalho | Descrição | Função |
|--------|-----------|--------|
| `nu` | Novo usuário | `novo_usuario()` |
| `nc` | Nova conta | `nova_conta()` |
| `qt` | Sair | `exit()` |

---

### Menu Dados Existentes

| Atalho | Descrição | Pré-requisito | Função |
|--------|-----------|---------------|--------|
| `nu` | Novo usuário | - | `novo_usuario()` |
| `nc` | Nova conta | - | `nova_conta()` |
| `lg` | Login | Contas existem | `login_conta()` |
| `de` | Depositar | Conta ativa | `depositar()` |
| `sa` | Sacar | Conta ativa | `sacar()` |
| `ex` | Extrato | Conta ativa | `exibir_extrato()` |
| `rel` | Relatório | Conta ativa | Menu de filtros |
| `lc` | Listar contas | - | Loop com iterador |
| `lu` | Listar usuários | - | Exibe usuarios.csv |
| `it` | Iterador | - | Usa ContaIterador |
| `qt` | Sair | - | `exit()` |

---

## 📊 Estrutura de Dados

### Dicionário Usuario

```python
usuario = {
    'cpf': '12345678901',
    'nome': 'João Silva',
    'data_nascimento': '01/01/1990',
    'endereco': 'Rua A, 100 - Centro - SP/SP - 12345-678'
}
```

### Dicionário Conta

```python
conta = {
    'cpf': '12345678901',
    'agencia': '0001',
    'numero_conta': '1',
    'data_criacao': '10/04/2026 15:30:00',
    'saldo': 100.00  # Depreciado
}
```

### Dicionário Transação

```python
transacao = {
    'cpf': '12345678901',
    'numero_conta': '1',
    'tipo': 'deposito',
    'valor': 100.00,
    'data_hora': '10/04/2026 15:35:00',
    'saldo_apos': 100.00
}
```

### Dicionário Conta Ativa

```python
conta_ativa = {
    'cpf': '12345678901',
    'usuario': {...},  # Dicionário Usuario
    'conta': {...},    # Dicionário Conta
    'numero_conta': 1
}
```

### Dicionário de Transação do Relatório

```python
transacao_relatorio = {
    "agencia": "0001",
    "numero": 1,
    "titular": "João Silva",
    "saldo": 100.00
}
```

---

## ⚙️ Decoradores e Geradores

### log_transacao(tipo_transacao)

**Quando Usar:** Para logar operações com timestamp

**Exemplo:**
```python
@log_transacao("Depósito")
def depositar():
    # [LOG] 10/04/2026 15:35:00 - Transação: Depósito
```

---

### gerar_relatorio_transacoes(cpf, numero_conta, tipo_filtro=None)

**Tipo:** Generator

**Quando Usar:** Para iterar sobre transações filtradas

**Exemplo:**
```python
for transacao in gerar_relatorio_transacoes('12345678901', 1, 'deposito'):
    print(f"Depósito: R$ {transacao['valor']}")
```

---

## ✅ Validações

### validar_cpf(cpf)

**Algoritmo:** Dígitos verificadores brasileiros

**Validações Realizadas:**
- ❌ Se não tem 11 dígitos
- ❌ Se todos dígitos são iguais (111.111.111-11)
- ❌ Se dígitos verificadores inválidos

**Exemplo:**
```python
validar_cpf('12345678901')  # True/False
```

---

### validar_endereco(endereco)

**Formato Expected:** `Rua, número - Bairro - Cidade/UF - CEP`

**Validações Realizadas:**
- ❌ Se não tem vírgula após rua
- ❌ Se não tem hífen separando bairro
- ❌ Se não tem barra separando cidade/UF
- ❌ Se CEP não tem hífen

---

### Validações em Operações

**depositar():**
- ✅ Valor > 0
- ✅ Conta ativa
- ✅ Máximo 10 transações/dia

**sacar():**
- ✅ Valor > 0
- ✅ Saldo suficiente
- ✅ Valor ≤ R$ 500 (limite)
- ✅ Máximo 3 saques/conta/dia
- ✅ Máximo 10 transações/dia

---

## 🧪 Testes

### test_v4.0.py

Arquivo: `test_v4.0.py` (~300 linhas)

**Total de Testes:** 11 ✅

| # | Teste | Status |
|---|-------|--------|
| 1 | CSV creation | ✅ |
| 2 | User addition | ✅ |
| 3 | User duplicate detection | ✅ |
| 4 | User loading | ✅ |
| 5 | Account creation | ✅ |
| 6 | Account loading | ✅ |
| 7 | Transaction addition | ✅ |
| 8 | Transaction loading | ✅ |
| 9 | Balance calculation | ✅ |
| 10 | Data existence check | ✅ |
| 11 | Accounts existence check | ✅ |

**Como executar:**
```bash
python test_v4.0.py
```

---

## 📖 Documentação

### Arquivos Markdown

| Arquivo | Linhas | Tópicos |
|---------|--------|--------|
| `README.md` | ~900 | Quick start, menu, exemplos, requisitos |
| `CHANGELOG_v4.0.md` | ~500 | Mudanças vs v3.0, novos recursos |
| `INDEX_v4.0.md` | ~400 | Este arquivo - Referência |
| `FLUXOS_v4.0.md` | ~400 | Diagramas de fluxo, arquitetura |

---

## 🗺️ Como Navegar

### Por Tipo de Informação

**Quero começar a usar:**
→ Leia [README.md](README.md) - Seção "Quick Start"

**Quero entender a arquitetura:**
→ Leia [FLUXOS_v4.0.md](FLUXOS_v4.0.md)

**Quero referência de funções:**
→ Estou aqui! [INDEX_v4.0.md](#---index-v40---índice-completo)

**Quero saber mudanças vs v3.0:**
→ Leia [CHANGELOG_v4.0.md](CHANGELOG_v4.0.md)

### Por Função

**Novo usuário:**
1. Menu: `[nu]`
2. Função: `novo_usuario()` em main_v4.0.py
3. Persistência: `adicionar_usuario_csv()` em csv_manager.py
4. Arquivo: usuarios.csv

**Fazer login:**
1. Menu: `[lg]`
2. Função: `login_conta()` em main_v4.0.py
3. Validação: `usuario_existe()` em csv_manager.py
4. Carregamento: `obter_contas_do_usuario()` em csv_manager.py

**Depositar:**
1. Menu: `[de]` (requer login)
2. Função: `depositar()` em main_v4.0.py
3. Validação: Máx 10 transações/dia
4. Persistência: `adicionar_transacao_csv()` em csv_manager.py
5. Arquivo: transacoes.csv

**Ver extrato:**
1. Menu: `[ex]` (requer login)
2. Função: `exibir_extrato()` em main_v4.0.py
3. Carregamento: `obter_transacoes_conta()` em csv_manager.py
4. Gerador: `gerar_relatorio_transacoes()` com tipo=None

**Relatório filtrado:**
1. Menu: `[rel]` (requer login)
2. Função: Menu de filtros
3. Gerador: `gerar_relatorio_transacoes()` com tipo específico
4. Tipos: "deposito" ou "saque"

### Por Componente

**Menu:**
- Primeira execução: `menu_primeira_execucao()` em main_v4.0.py
- Dados existentes: `menu_dados_existentes()` em main_v4.0.py
- Operações: 11 atalhos diferentes

**Persistência:**
- todas as funções estão em csv_manager.py
- Inicialização: `inicializar_csvs()`
- Usuários: `carregar_usuarios()`, `adicionar_usuario_csv()`, ...
- Contas: `carregar_contas()`, `adicionar_conta_csv()`, ...
- Transações: `obter_transacoes_conta()`, `adicionar_transacao_csv()`, ...

**Padrões:**
- Iterator: `ContaIterador` em main_v4.0.py
- Generator: `gerar_relatorio_transacoes()` em main_v4.0.py
- Decorator: `@log_transacao()` em main_v4.0.py

---

## 🔍 Buscas Rápidas

**Procurando função para:**

| Tarefa | Função | Arquivo |
|--------|--------|---------|
| Criar CSV | `inicializar_csvs()` | csv_manager.py |
| Validar CPF | `validar_cpf()` | main_v4.0.py |
| Validar Endereço | `validar_endereco()` | main_v4.0.py |
| Carregar usuários | `carregar_usuarios()` | csv_manager.py |
| Adicionar usuário | `adicionar_usuario_csv()` | csv_manager.py |
| Obter contas | `obter_contas_do_usuario()` | csv_manager.py |
| Registrar transação | `adicionar_transacao_csv()` | csv_manager.py |
| Calcular saldo | `obter_saldo_conta()` | csv_manager.py |
| Iterar contas | `ContaIterador` | main_v4.0.py |
| Filtrar transações | `gerar_relatorio_transacoes()` | main_v4.0.py |
| Logar operação | `@log_transacao()` | main_v4.0.py |

---

## 📋 Checklist de Referência

Ao trabalhar com v4.0:

- [ ] Lembrar que `obter_saldo_conta()` CALCULA saldo (não retorna armazenado)
- [ ] Verificar se função está em `main_v4.0.py` ou `csv_manager.py`
- [ ] Usar `carregar_usuarios()` após `adicionar_usuario_csv()` se precisar dados atualizados
- [ ] Menu se adapta baseado em `dados_existem()` e `contas_existem()`
- [ ] Transações são ad-hoc em `transacoes.csv` (sem carregamento prévio)
- [ ] CPF é chave primária para usuários
- [ ] Número de conta é único por CPF
- [ ] Máximo 3 saques por conta por dia
- [ ] Máximo 10 transações por conta por dia
- [ ] Validações são feitas ANTES de adicionar a CSV

---

## 🎯 Roadmap de Documentação

Para adicionar no futuro:
- [ ] Exemplos de integração SQL
- [ ] Diagrama ER do banco de dados
- [ ] Performance benchmarks
- [ ] Plano de migração CSV → SQL
- [ ] API REST endpoints (v5.0)

---

**Última atualização:** 10 de Abril de 2026  
**Status:** ✅ Completo  
**Versão:** v4.0