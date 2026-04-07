# 📝 CHANGELOG v4.0

## O que mudou de v3.0 para v4.0?

---

## 🎯 Visão Geral das Mudanças

A v4.0 introduz **persistência de dados em CSV**, permitindo que todas as operações sejam salvas e recuperadas nas próximas execuções do programa. Esta é a mudança mais significativa desde a v3.0.

---

## 📊 Comparação Completa

| Feature | v3.0 | v4.0 | Tipo |
|---------|------|------|------|
| **Persistência de Dados** | ❌ Não | ✅ Sim (CSV) | 🆕 NOVO |
| **Menu Adaptativo** | ❌ Não | ✅ Sim | 🆕 NOVO |
| **Login por Conta** | ❌ Não | ✅ Sim | 🆕 NOVO |
| **Arquivos CSV** | ❌ Não | ✅ 3 arquivos | 🆕 NOVO |
| **Módulo csv_manager.py** | ❌ Não | ✅ Sim | 🆕 NOVO |
| **Menu Primário** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Decorador log_transacao** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Iterador ContaIterador** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Gerador gerar_relatorio** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Validações (CPF, endereço)** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Operações (depositar, sacar)** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Histórico de Transações** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Data/Hora em Transações** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Limite de Saque (R$ 500)** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Máx 3 Saques/Dia** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |
| **Máx 10 Transações/Dia** | ✅ Sim | ✅ Sim | ➡️ MANTIDO |

---

## 🆕 Novos Recursos em v4.0

### 1. **Persistência em CSV** ⭐
**O que é:**
- Dados salvos automaticamente em 3 arquivos CSV
- Cada execução carrega dados da execução anterior
- Zero perda de informações

**Como funciona:**
```python
# v4.0: Dados são salvos em CSV
[nu] → Cria usuário → Salva em usuarios.csv
[nc] → Cria conta → Salva em contas.csv
[de] → Deposita → Salva em transacoes.csv
```

**Arquivos criados:**
- `usuarios.csv` - Usuários cadastrados
- `contas.csv` - Contas criadas
- `transacoes.csv` - Histórico de transações

---

### 2. **Menu Adaptativo** ⭐
**O que é:**
- Menu diferente na primeira e segunda execução
- Adaptação automática baseada no estado do sistema

**Primeira Execução (sem dados):**
```
[nu] Novo usuário
[nc] Nova conta
[qt] Sair

❌ Login desabilitado
❌ Operações bancárias desabilitadas
```

**Segunda Execução (com dados):**
```
[nu] Novo usuário      ← Ainda disponível
[nc] Nova conta        ← Ainda disponível
[lg] Login na conta    ← ✨ NOVO!
[de] Depositar         ← Requer login
[sa] Sacar             ← Requer login
[ex] Extrato           ← Requer login
[rel] Relatório        ← Requer login
[lc] Listar contas     ← Ainda disponível
[lu] Listar usuários   ← Ainda disponível
[it] Iterador          ← Ainda disponível
[qt] Sair
```

---

### 3. **Login por Conta** ⭐
**O que é:**
- Autenticação baseada em CPF + seleção de conta
- Isolamento total de dados entre contas

**Como funciona:**
```
[lg] → Informe CPF: 12345678901
    → [1] Agência 0001 | Conta 1 | Saldo R$ 100.00
    → [2] Agência 0001 | Conta 2 | Saldo R$ 250.00
    → Selecione: 1
    → ✓ Acesso liberado à Conta 1
```

---

### 4. **csv_manager.py** ⭐
**O que é:**
- Novo módulo (~250 linhas) dedicado à persistência
- Abstração completa de operações CSV
- Separação clara entre apresentação e dados

**Funções principais:**
```python
inicializar_csvs()                          # Cria CSVs se não existem
adicionar_usuario_csv(cpf, nome, ...)      # Adiciona usuário
carregar_usuarios()                         # Carrega todos
usuario_existe(cpf)                         # Verifica duplicação
obter_usuario(cpf)                          # Obtém dados do usuário
adicionar_conta_csv(cpf, agencia, ...)      # Adiciona conta
carregar_contas()                           # Carrega todas
obter_contas_do_usuario(cpf)                # Contas de um usuário
adicionar_transacao_csv(...)                # Registra transação
obter_transacoes_conta(cpf, numero_conta)   # Transações de uma conta
obter_saldo_conta(cpf, numero_conta)        # Calcula saldo
dados_existem()                             # Verifica se há dados
contas_existem()                            # Verifica se há contas
```

---

## 📝 Mudanças no Código Existente

### 1. **main_v4.0.py**
**Antes (v3.0):**
```python
# Dados só em memória
usuarios = []
contas = []
transacoes = []
```

**Depois (v4.0):**
```python
# Dados carregados de CSV
inicializar_csvs()
usuarios = carregar_usuarios()
contas = carregar_contas()
# Transações carregadas sob demanda

# Menu se adapta conforme dados existem
if dados_existem():
    menu_dados_existentes()
else:
    menu_primeira_execucao()
```

### 2. **Operações de Persitência**
**Antes (v3.0):**
```python
def novo_usuario(usuarios):
    # Adiciona à lista em memória
    usuarios.append({...})
    # Dados perdidos ao encerrar
```

**Depois (v4.0):**
```python
def novo_usuario():
    # Cria o usuário
    usuario = {...}
    # Salva em CSV
    adicionar_usuario_csv(...)
    # Dados persistem entre execuções
```

### 3. **Método de Carregamento de Dados**
**Antes (v3.0):**
```
[Iniciar] → Menu vazio
```

**Depois (v4.0):**
```
[Iniciar] → Inicializar CSVs
         → Carregar usuarios.csv
         → Carregar contas.csv
         → Menu adaptativo
```

---

## 🔄 Impacto nas Funcionalidades Principais

### ✅ Operações Preservadas (com melhorias)

| Operação | v3.0 | v4.0 | Melhoria |
|----------|------|------|----------|
| `novo_usuario()` | Memória | **CSV + Memória** | Persistência |
| `nova_conta()` | Memória | **CSV + Memória** | Persistência |
| `depositar()` | Memória | **CSV + Memória** | Persistência |
| `sacar()` | Memória | **CSV + Memória** | Persistência |
| `exibir_extrato()` | Memória | **CSV (sob demanda)** | Eficiência |
| `validar_cpf()` | Mesmo | Mesmo | Sem mudança |
| `validar_endereco()` | Mesmo | Mesmo | Sem mudança |
| `@log_transacao` | Mesmo | Mesmo | Sem mudança |
| `ContaIterador` | Mesmo | Mesmo | Sem mudança |
| `gerar_relatorio()` | Mesmo | Mesmo | Sem mudança |

---

## 📂 Estrutura de Arquivos

### v3.0
```
00 - Desafio/
├── main.py
├── teste_v3.0.py
├── DOCUMENTACAO.md
├── INDICE.md
└── ... (outros arquivos)
```

### v4.0
```
00 - Desafio/
├── main_v4.0.py          ← Versão com persistência
├── csv_manager.py        ← ✨ NOVO
├── test_v4.0.py          ← Testes da v4.0
├── README.md             ← Documentação consolidada
├── usuarios.csv          ← ✨ Criado automaticamente
├── contas.csv            ← ✨ Criado automaticamente
├── transacoes.csv        ← ✨ Criado automaticamente
└── PRDs/                 ← Especificação
```

---

## 🧪 Impacto nos Testes

**v3.0:**
- Sem testes automatizados para persistência
- Dados perdidos entre execuções

**v4.0:**
- `test_v4.0.py` - 11 testes automatizados
- Valida criação de CSVs
- Valida carregamento de dados
- Valida persistência entre sessões
- Valida cálculo de saldo

```bash
python test_v4.0.py
# ✅ Teste 1: CSV creation passed
# ✅ Teste 2: User addition passed
# ✅ Teste 3: Data loading passed
# ✅ ... 8 testes a mais
```

---

## ⚙️ Mudanças Técnicas Importantes

### 1. **Inicialização do Sistema**
**v3.0:**
```python
def main():
    print("Bem-vindo!")
    menu_principal()
```

**v4.0:**
```python
def main():
    inicializar_csvs()  # ← NOVO: Cria CSVs se não existem
    usuarios = carregar_usuarios()  # ← NOVO: Carrega dados
    
    if dados_existem():
        menu_dados_existentes()
    else:
        menu_primeira_execucao()
```

### 2. **Validação de CPF Duplicado**
**v3.0:**
```python
for usuario in usuarios:
    if usuario['cpf'] == cpf:  # Só em memória
        # Mensagem de erro
```

**v4.0:**
```python
if usuario_existe(cpf):  # Valida em CSV
    # Mensagem de erro
```

### 3. **Cálculo de Saldo**
**v3.0:**
```python
# Saldo armazenado em transacoes
saldo = transacao['saldo']
```

**v4.0:**
```python
# Saldo CALCULADO a partir de transações
saldo = obter_saldo_conta(cpf, numero_conta)
# Garante consistência absoluta
```

---

## 🚀 Performance & Escalabilidade

### v3.0
- Todos os dados em memória
- Rápido para poucos registros
- Perde qualidade com muitos usuários
- Limite prático: ~1000 usuários

### v4.0
- Dados em CSV (leitura sob demanda)
- Escalável para médios volumes
- Melhor separação de responsabilidades
- Preparado para migração para SQL

---

## 🔒 Mudanças de Segurança

### v3.0
- Dados apenas em memória
- Sem backup automático
- Sem log de acesso

### v4.0
- ✅ Dados persistidos em CSV (backup)
- ✅ Histórico completo de transações
- ✅ Integridade referencial (CPF-Contas-Transações)
- ✅ Validação de duplicação
- ✅ UTF-8 encoding (suporta acentos)

---

## 📊 Resumo de Mudanças

| Categoria | Mudanças |
|-----------|----------|
| **Novos Recursos** | 4 grandes features |
| **Novos Modules** | 1 (csv_manager.py) |
| **Novos Arquivos** | 3 (usuarios.csv, contas.csv, transacoes.csv) |
| **Operações Modificadas** | 8 (novo_usuario, nova_conta, depositar, sacar, etc) |
| **Operações Preservadas** | 3 (validações, decoradores, iteradores) |
| **Linhas de Código** | +250 (csv_manager) |
| **Testes Adicionados** | 11 testes automatizados |
| **Documentação** | +2000 linhas |

---

## ✨ Destaques Principais da v4.0

### 🏆 Maior Impacto
**Persistência de Dados em CSV**
- Mudança fundamental no funcionamento
- Dados não são perdidos entre execuções
- Abre porta para recursos futuros

### 🎯 Segunda Mudança Mais Importante
**Menu Adaptativo**
- Experiência de usuário melhorada
- Interface se ajusta ao estado do sistema
- Menos confusão para iniciantes

### 💡 Melhoria Arquitetural
**csv_manager.py**
- Separação clara entre apresentação e dados
- Facilita testes e manutenção
- Preparado para migração para banco de dados

---

## 📈 Matriz de Compatibilidade

| Recurso v3.0 | Compatível com v4.0? | Notas |
|--------------|----------------------|-------|
| Scripts que leem dados | ❌ Não | Dados agora em CSV |
| Formato de entrada (menu) | ✅ Sim | Mesmos atalhos |
| Validações | ✅ Sim | Idênticas |
| Estrutura de dados | ⚠️ Parcial | Estrutura + CSV |

---

## 🔮 Preparação para Versões Futuras

A v4.0 foi projetada de modo que:

1. **Migração para SQL será fácil**
   - csv_manager.py pode virar database_manager.py
   - Interface das funções permanece igual
   - main_v4.0.py precisa de ajustes mínimos

2. **Adição de autenticação será simples**
   - Já existe estrutura de login
   - Só falta adicionar senha

3. **API REST será possível**
   - Dados já estão em estrutura padrão
   - csv_manager funciona como base de dados

---

## 🎓 Lições Aprendidas

### Decisões de Design na v4.0

1. **CSV ao invés de Banco de Dados**
   - Razão: Simplicidade, sem dependências externas
   - Custo: Performance com muitos dados
   - Benefício: Aprendizado de file I/O

2. **Menu Adaptativo**
   - Razão: UX melhor para primeira execução
   - Custo: Lógica mais complexa na main
   - Benefício: Menos confusão do usuário

3. **Saldo Calculado vs Armazenado**
   - Razão: Garantir consistência
   - Custo: Performance em extratos grandes
   - Benefício: Impossível ter inconsistência

---

## 📋 Migração de v3.0 para v4.0

### Para Desenvolvedores
```python
# Código v3.0:
usuarios.append(novo_usuario)

# Código v4.0:
novo_usuario()  # Salva automaticamente em CSV
usuarios = carregar_usuarios()  # Carrega se necessário
```

### Para Usuários
```
v3.0: Dados perdidos ao encerrar
v4.0: Dados salvos automaticamente ✓
```

---

## 🏁 Conclusão

A v4.0 marca a evolução do Sistema Bancário Python de um **protótipo educacional** para uma **aplicação com persistência de dados**. 

Mantém toda a qualidade pedagógica (decoradores, iteradores, geradores) enquanto adiciona relevância prática (dados persistem, menu adaptativo, login).

**Próxima evolução esperada:** v5.0 com banco de dados SQL.

---

**Data:** 10 de Abril de 2026  
**Status:** ✅ Completo  
**Compatibilidade:** Python 3.8+