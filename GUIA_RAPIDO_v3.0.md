# 🚀 Guia Rápido v3.0 - Como Usar as Novas Funcionalidades

## ✨ O que há de novo?

### 1. 🎯 Decorador de Log
Cada transação de banco agora é registrada automaticamente com data e hora.

**Como funciona:**
- Quando você faz um depósito ou saque, o sistema printa:
  ```
  [LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
  === Depósito realizado com sucesso! ===
  ```

**Nenhuma ação necessária!** É automático.

---

### 2. 📊 Extrato com Data/Hora
O extrato agora mostra a data e hora exata de cada transação.

**Como usar:**
1. Selecione `[ex]` - Extrato no menu
2. Veja seu histórico com timestamps:
   ```
   [06/04/2026 14:35:22] DEPÓSITO: R$ 1000.00
   [06/04/2026 14:36:45] SAQUE: R$ 150.00
   ```

---

### 3. 📈 Relatório com Gerador (NOVO: `[rel]`)
Veja suas transações com filtros personalizados.

**Como usar:**
1. Crie uma conta e faça algunas transações
2. Selecione `[rel]` - Relatório de transações
3. Escolha uma opção:
   - `[1]` Todas as transações
   - `[2]` Apenas depósitos
   - `[3]` Apenas saques
4. Sistema mostra uma a uma com detalhes:
   ```
   1. [06/04/2026 14:35:22] DEPÓSITO
      Valor: R$ 1000.00
      Saldo após: R$ 1000.00
   ```

---

### 4. 💳 Iterador de Contas (NOVO: `[it]`)
Veja todas as contas do banco com saldos calculados.

**Como usar:**
1. Crie 2 ou 3 contas com usuários diferentes
2. Faça transações em cada conta
3. Selecione `[it]` - Iterador de contas
4. Sistema lista todas as contas:
   ```
   1. Conta #1
      Agência: 0001
      Titular: João da Silva
      Saldo Atual: R$ 850.00

   2. Conta #2
      Agência: 0001
      Titular: Maria Santos
      Saldo Atual: R$ 2000.00
   ```

---

### 5. ⏰ Limite de 10 Transações por Dia
O sistema agora limita a 10 transações por dia (depósitos + saques).

**Como funciona:**
- Você pode fazer no máximo 10 operações em um dia
- Contador reseta automaticamente à meia-noite
- Se tentar fazer a 11ª transação:
  ```
  @@@ Operação falhou! Você excedeu o número de transações 
  permitidas para hoje (máximo 10). @@@
  ```

**Nenhuma ação necessária!** É automático e transparente.

---

## 📋 Menu Completo (v3.0)

```
================ MENU ================
[de]     Depositar
[sa]     Sacar
[ex]     Extrato
[nc]     Nova conta
[lc]     Listar contas
[lu]     Listar usuários com contas
[rel]    Relatório de transações ⭐ NOVO
[it]     Iterador de contas       ⭐ NOVO
[nu]     Novo usuário
[qt]     Sair
=> 
```

---

## 🎮 Exemplo Completo de Sessão

### Passo 1: Criar Usuário
```
=> nu
Informe o CPF: 12345678901
Informe o nome completo: João da Silva
Informe a data de nascimento: 15/08/1990
Informe o endereço: Rua X, 100 - Centro - São Paulo/SP - 01310-100

=== Usuário criado com sucesso! ===
```

### Passo 2: Criar Conta
```
=> nc
Informe o CPF do usuário: 12345678901

=== Conta criada com sucesso! ===
Titular: João da Silva
Agência: 0001
Número da Conta: 1
```

### Passo 3: Depositar (com Decorador)
```
=> de
Informe o valor do depósito: 1000

[LOG] 06/04/2026 14:35:22 - Transação: DEPÓSITO
=== Depósito realizado com sucesso! ===
```

### Passo 4: Sacar (com Decorador e Limite)
```
=> sa
Informe o valor do saque: 150

[LOG] 06/04/2026 14:36:45 - Transação: SAQUE
=== Saque realizado com sucesso! ===
```

### Passo 5: Ver Extrato (com Data/Hora)
```
=> ex

================ EXTRATO ================

Histórico detalhado de transações:

1. [06/04/2026 14:35:22] DEPÓSITO
   Valor: R$ 1000.00
   Saldo após transação: R$ 1000.00

2. [06/04/2026 14:36:45] SAQUE
   Valor: R$ 150.00
   Saldo após transação: R$ 850.00

Saldo: R$ 850.00
==========================================
```

### Passo 6: Ver Relatório (com Gerador e Filtro)
```
=> rel

================ RELATÓRIO DE TRANSAÇÕES ================
Conta: 1 | Titular: João da Silva

[1] Todas as transações
[2] Apenas depósitos
[3] Apenas saques

Escolha uma opção: 2

--- DEPÓSITOS ---

1. [06/04/2026 14:35:22] DEPOSITO
   Valor: R$ 1000.00
   Saldo após: R$ 1000.00

=======================================================
```

### Passo 7: Ver Iterador de Contas
```
=> it

================ ITERADOR DE CONTAS BANCÁRIAS ================

1. Conta #1
   Agência: 0001
   Titular: João da Silva
   Saldo Atual: R$ 850.00

============================================================
```

---

## 🧪 Como Testar Tudo

Existem 2 formas:

### Forma 1: Teste Automatizado (Recomendado)
```bash
python teste_v3.0.py
```

Mostra:
- ✅ Decorador de Log
- ✅ Iterador de Contas
- ✅ Gerador de Relatórios
- ✅ Data e Hora
- ✅ Limite de 10 transações
- ✅ Validação de CPF

### Forma 2: Interativo (Explore você mesmo)
```bash
python main.py
```

Teste cada funcionalidade:
1. `[nu]` → Criar usuário
2. `[nc]` → Criar conta
3. `[de]` → Depositar (veja o log!)
4. `[sa]` → Sacar (veja o log!)
5. `[ex]` → Extrato (veja data/hora!)
6. `[rel]` → Relatório (filtre!)
7. `[it]` → Iterador (lista todas!)

---

## 📚 Conceitos Python Utilizados

| Conceito | Exemplos |
|----------|----------|
| **Decoradores** | `@log_transacao("DEPÓSITO")` |
| **Geradores** | `gerar_relatorio_transacoes(conta, "saque")` |
| **Iteradores** | `ContaIterador(contas)` |
| **Data/Hora** | `datetime.now()`, `date.today()` |
| **List Comprehension** | Filtros em loopings |
| **Dicionários** | Estrutura de transações |
| **Validação** | CPF, Endereço, Limites |

---

## ⚙️ Configurações

### Limite Diário (pode ser alterado)
Localizado em `main()` linha ~270:
```python
transacoes_hoje >= 10  # Mudar para outro número se quiser
```

### Limite de Saques por Dia (v1.0 - mantido)
Localizado em `main()` linha ~260:
```python
LIMITE_SAQUES = 3  # Máximo 3 saques por dia
```

### Limite por Saque (v1.0 - mantido)
Localizado em `main()` linha ~261:
```python
limite = 500  # Máximo R$ 500 por saque
```

---

## 🐛 Solução de Problemas

### Problema: "Nenhuma conta ativa!"
**Solução:** Crie uma conta primeiro usando `[nc]`

### Problema: "Você excedeu o número de transações"
**Solução:** Você fez 10 transações hoje. Tente amanhã ou mude a data do sistema.

### Problema: "CPF inválido!"
**Solução:** Use um CPF com 11 dígitos válido (ex: 12345678901)

### Problema: "Endereço em formato inválido!"
**Solução:** Use: `Rua X, 100 - Bairro - Cidade/SP - 01234-567`

---

## 📞 Suporte

Para entender melhor os conceitos, consulte:
- `DOCUMENTACAO_TECNICA_v3.0.md` - Detalhes técnicos
- `NOVO_CHANGELOG_v3.0.md` - O que mudou
- Arquivos de exemplo em `../03 - Decoradores, Iteradores e Geradores/`

---

## ✅ Checklist de Funcionalidades

- [x] Decorador de Log para transações
- [x] Gerador de Relatórios com filtros
- [x] Iterador de Contas do banco
- [x] Data/Hora em cada transação
- [x] Limite de 10 transações/dia
- [x] Reset automático de contadores
- [x] Menu com [rel] e [it]
- [x] Testes automatizados
- [x] Documentação completa

---

**Pronto para usar! 🎉**

Desenvol vido para: Trilha Python DIO
Versão: 3.0
Data: Abril de 2026
