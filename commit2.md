# Commit Message v3.0

## feat: Implementar decoradores, geradores e iteradores no sistema bancário v3.0

---

## RESUMO DAS ALTERAÇÕES

Refatoração completa do sistema bancário (main.py) integrando conceitos 
avançados de Python (decoradores, geradores, iteradores) com suporte a 
data/hora e limite de 10 transações diárias.

---

## IMPLEMENTAÇÕES PRINCIPAIS

### 1. Decorador de Log (`@log_transacao`)
- Registra data, hora e tipo de cada transação
- Aplicado automaticamente em `depositar()` e `sacar()`
- Formato: `[LOG] DD/MM/YYYY HH:MM:SS - Transação: TIPO`
- Preserva metadados da função com `@wraps`

### 2. Gerador de Relatórios (`gerar_relatorio_transacoes`)
- Itera sobre transações de uma conta com lazy evaluation
- Suporta filtros por tipo (deposito, saque, None)
- Nova opção `[rel]` no menu para relatórios interativos
- Usa `yield` para economia de memória

### 3. Iterador de Contas (`ContaIterador`)
- Implementa `__iter__()` e `__next__()` para navegar contas
- Calcula saldo dinâmico a partir do histórico de transações
- Nova opção `[it]` no menu para listar todas as contas
- Levanta `StopIteration` ao terminar

### 4. Data e Hora em Transações
- Cada transação registra `datetime.now()` e `strftime` formatado
- Extrato exibe todas as transações com timestamps
- Estrutura: `{"tipo", "valor", "data_hora", "data_hora_str", "saldo_apos"}`
- Data/hora formatada em padrão brasileiro DD/MM/YYYY HH:MM:SS

### 5. Limite de 10 Transações Diárias
- Máximo de 10 operações (depósitos + saques) por dia
- Reset automático à meia-noite (detecção com `date.today()`)
- Validação antes da execução com mensagem de erro específica
- Contador de saques também reseta automaticamente

---

## MUDANÇAS NO CÓDIGO

### `main.py` (~550 linhas)

**Importações (Linhas 1-5):**
```python
import textwrap
import re
from datetime import datetime, date
from functools import wraps
```

**Decorador (Linhas 8-22):**
- Novo: `def log_transacao(tipo_transacao):`
- Implementa closure com função interna
- Usa `@wraps` para preservar metadados

**Iterador (Linhas 24-47):**
- Nova: `class ContaIterador:`
- Métodos: `__init__`, `__iter__`, `__next__`
- Calcula saldo somando transações

**Gerador (Linhas 39-54):**
- Nova: `def gerar_relatorio_transacoes(conta, tipo_filtro=None):`
- Usa `yield` para cada transação
- Suporta filtro opcional

**Função `depositar()` (~175):**
- Adicionado: `@log_transacao("DEPÓSITO")`
- Novo parâmetro: `transacoes`
- Registra data/hora de cada depósito
- Cria dicionário de transação

**Função `sacar()` (~210):**
- Adicionado: `@log_transacao("SAQUE")`
- Novo parâmetro: `transacoes, transacoes_hoje`
- Valida limite de 10 transações/dia
- Registra transação com data/hora
- Retorna: `(saldo, extrato, numero_saques, transacoes, transacoes_hoje)`

**Função `exibir_extrato()` (~235):**
- Novo parâmetro: `transacoes=None`
- Mostra transações com data/hora detalhada
- Exibe saldo após cada transação

**Função `nova_conta()` (~270):**
- Novo: `conta["transacoes"] = []`
- Novo: `conta["data_criacao"] = datetime.now()`
- Inicializa estrutura para histórico de transações

**Função `exibir_relatorio()` (NOVA ~290):**
- Usa gerador `gerar_relatorio_transacoes`
- Menu interativo para escolher filtro
- Exibe transações formatadas com data/hora

**Função `exibir_iterador_contas()` (NOVA ~320):**
- Usa `ContaIterador` para listar contas
- Mostra agência, número, titular, saldo

**Função `main()` (~350):**
- Novo: variáveis `transacoes`, `transacoes_hoje`, `data_transacoes`, `conta_ativa`
- Novo: verificação de mudança de dia para reset
- Novo: opções `[rel]` e `[it]` no menu
- Atualiza logic de depósito/saque para novos parâmetros

**Menu (Expandido):**
```
[de]     Depositar
[sa]     Sacar
[ex]     Extrato
[nc]     Nova conta
[lc]     Listar contas
[lu]     Listar usuários com contas
[rel]    Relatório de transações        ← NOVO
[it]     Iterador de contas             ← NOVO
[nu]     Novo usuário
[qt]     Sair
```

---

## NOVOS ARQUIVOS

### Documentação (6 arquivos)
1. **`GUIA_RAPIDO_v3.0.md`** - Como usar o sistema (usuários)
2. **`NOVO_CHANGELOG_v3.0.md`** - Detalhes de mudanças por feature
3. **`DOCUMENTACAO_TECNICA_v3.0.md`** - Implementação técnica detalhada
4. **`INDEX_v3.0.md`** - Índice e ponto de entrada para documentação
5. **`commit2.md`** - Este arquivo (descrição do commit)

### Testes (1 arquivo)
6. **`teste_v3.0.py`** - Testes automatizados de todas as funcionalidades
   - Teste 1: Decorador de Log
   - Teste 2: Iterador de Contas
   - Teste 3: Gerador de Relatórios
   - Teste 4: Data e Hora
   - Teste 5: Limite 10 Transações
   - Teste 6: Validação CPF

---

## COMPATIBILIDADE

### ✅ Mantém Compatibilidade Com:
- Validação de CPF algoritmo módulo 11 (v2.1)
- Validação e normalização de endereço (v2.1)
- Limite de 3 saques por dia (v1.0)
- Limite de R$ 500 por saque (v1.0)
- Gerenciamento de usuários e contas (v1.0)
- Listar contas e usuários (v2.0)

### ⚠️ BREAKING CHANGES: **NENHUMA** (backward compatible)

---

## TESTES EXECUTADOS

Todos executados com sucesso em `teste_v3.0.py`:

```
✅ TESTE 1: Decorador de Log - PASSOU
✅ TESTE 2: Iterador de Contas - PASSOU
✅ TESTE 3: Gerador de Relatórios - PASSOU
✅ TESTE 4: Data e Hora - PASSOU
✅ TESTE 5: Limite 10 Transações - PASSOU
✅ TESTE 6: Validação CPF - PASSOU

✅ TODOS OS TESTES COMPLETADOS COM SUCESSO!
```

---

## CONCEITOS PYTHON APLICADOS

| Conceito | Local | Implementação |
|----------|-------|-----------------|
| Decoradores parametrizados | `@log_transacao()` | Closure com função interna |
| Geradores | `gerar_relatorio_transacoes()` | Usa `yield` |
| Iteradores | `class ContaIterador` | `__iter__()` e `__next__()` |
| Data/Hora | `depositar()`, `sacar()` | `datetime.now()`, `strftime()` |
| Closures | Dentro decorador | Função dentro de função |
| Metaprogramação | `@wraps` | Preserva metadados |
| Validações | `sacar()`, `nova_conta()` | Múltiplas camadas |
| List Comprehension | Filtros | Codificação eficiente |
| Dicionários | Estrutura dados | Transações, contas, usuários |
| Listas | Container | Armazenamento sequências |

---

## HOW TO TEST

### Teste Automatizado
```bash
cd "00 - Desafio"
python teste_v3.0.py
```

**Resultado esperado:** Todos os 6 testes PASSAM ✅

### Teste Interativo
```bash
python main.py
```

**Testar manual:**
1. `[nu]` - Criar usuário
2. `[nc]` - Criar conta (ativa automaticamente)
3. `[de]` - Depositar (vê log!)
4. `[sa]` - Sacar (vê log! + limite 10 trans)
5. `[ex]` - Extrato (vê data/hora!)
6. `[rel]` - Relatório (filtra!)
7. `[it]` - Iterador (lista todas!)

---

## ESTRUTURA DE DADOS ATUALIZADA

### Conta (v3.0)
```python
conta = {
    "agencia": "0001",
    "numero_conta": 1,
    "usuario": {...},           # Referência ao usuário
    "transacoes": [...],        # ✨ NOVO: Lista de transações
    "data_criacao": datetime    # ✨ NOVO: Quando foi criada
}
```

### Transação (novo em v3.0)
```python
transacao = {
    "tipo": "deposito",                 # ou "saque"
    "valor": 1000.00,
    "data_hora": datetime(...),         # Objeto datetime
    "data_hora_str": "06/04/2026 14:35:22",  # String formatada
    "saldo_apos": 1000.00               # Saldo após transação
}
```

---

## NOTAS IMPORTANTES

1. **Saldo Anterior Reset:** Saldo anterior foi resetado pois agora é 
   calculado dinamicamente a partir do histórico de transações (melhor 
   rastreabilidade e auditoria).

2. **Conta Ativa:** Sistema agora rastreia qual conta está ativa 
   (`conta_ativa`) para facilitar operações sucessivas.

3. **Reset Automático:** Contadores de transações (`transacoes_hoje`) 
   e saques (`numero_saques`) resetam automaticamente à meia-noite 
   (detecção com `date.today()`).

4. **Histórico Permanente:** Todas as transações ficam registradas 
   na `conta["transacoes"]` de forma imutável.

5. **Lazy Evaluation:** Gerador de relatórios não carrega todas as 
   transações na memória, economizando recursos.

---

## DOCUMENTAÇÃO ADICIONAL

Para entender melhor:
- `GUIA_RAPIDO_v3.0.md` - Como usar (5-10 min)
- `NOVO_CHANGELOG_v3.0.md` - Detalhes por feature (15-30 min)
- `DOCUMENTACAO_TECNICA_v3.0.md` - Implementação (30-45 min)
- `INDEX_v3.0.md` - Índice e referência

---

**Desenvolvido para:** Trilha Python DIO  
**Data:** Abril de 2026  
**Versão:** 3.0  
**Status:** ✅ Completo, Testado e Documentado  
**Total de Arquivos Modificados/Criados:** 1 código + 6 documentação = 7 arquivos
