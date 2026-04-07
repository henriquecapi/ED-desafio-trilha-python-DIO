# 🔄 FLUXOS v4.0 - Diagramas e Processos

Visualização completa dos fluxos do Sistema Bancário v4.0.

---

## 📑 Índice de Fluxos

1. [Fluxo Geral de Execução](#-fluxo-geral-de-execução)
2. [Fluxo Menu Adaptativo](#-fluxo-menu-adaptativo)
3. [Fluxo Login](#-fluxo-login)
4. [Fluxo Depositar](#-fluxo-depositar)
5. [Fluxo Sacar](#-fluxo-sacar)
6. [Fluxo Novo Usuário](#-fluxo-novo-usuário)
7. [Fluxo Nova Conta](#-fluxo-nova-conta)
8. [Arquitetura em Camadas](#-arquitetura-em-camadas)
9. [Fluxo de Dados CSV](#-fluxo-de-dados-csv)
10. [Diagrama ER de Dados](#-diagrama-er-de-dados)
11. [Máquina de Estados](#-máquina-de-estados)
12. [Fluxo de Persistência](#-fluxo-de-persistência)

---

## 🚀 Fluxo Geral de Execução

```
┌─────────────────────┐
│   python main_v4.0.py
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│  inicializar_csvs()          │ ← Cria CSVs se não existem
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  usuarios = carregar_usuarios()
│  contas = carregar_contas()
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  dados_existem()?            │
└──────────┬────────────────────┘
           │
      ┌────┴────┐
      │          │
   NÃO│        │SIM
      │         │
      ▼         ▼
┌─────────────────┐  ┌──────────────────────┐
│ Menu Primário   │  │ Menu Dados Existentes│
│ [nu][nc][qt]    │  │ [lg][de][sa][ex]...  │
└────────┬────────┘  └──────────┬───────────┘
         │                      │
         │ ┌────────────────────┘
         │ │
         ▼ ▼
    ┌─────────────────┐
    │  Processar Menu │
    └────────┬────────┘
             │
      ┌──────┴────────┐
      │               │
   [qt]│           (outra)
      │               │
      ▼               ▼
  ┌────────┐    ┌────────────┐
  │  exit()│    │ Salvar CSV  │
  |        |    │ (se aplic.) │
  └────────┘    └─────┬──────┘
                      │
                      ▼
                ┌────────────┐
                │ Loop ^     │
                │ (próxima   │
                │  operação) │
                └────────────┘
```

---

## 🎪 Fluxo Menu Adaptativo

```
┌──────────────────────────────┐
│  Iniciar programa            │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  dados_existem()?                │
│  (há pelo menos 1 usuário?)      │
└──────────┬───────────────────────┘
           │
      ┌────┴────────┐
     NÃO             SIM
      │               │
      ▼               ▼
┌─────────────────┐  ┌──────────────────────┐
│  PRIMEIRA       │  │  PRÓXIMAS EXECUÇÕES  │
│  EXECUÇÃO       │  │  COM DADOS           │
│                 │  │                      │
│ Opções:         │  │ Opções:              │
│ ┌─────────────┐ │  │ ┌──────────────────┐│
│ │[nu] Usuário │ │  │ │[lg] Login        ││
│ │[nc] Conta   │ │  │ │[de] Depositar    ││
│ │[qt] Sair    │ │  │ │[sa] Sacar        ││
│ └─────────────┘ │  │ │[ex] Extrato      ││
│                 │  │ │[rel] Relatório   ││
│ Tudo é novo!    │  │ │[lc] Listar Contas││
│ Sem dados       │  │ │[lu] Listar Users ││
│ armazenados     │  │ │[it] Iterador     ││
│                 │  │ │[nc] Nova Conta   ││
│                 │  │ │[nu] Novo Usuário ││
│                 │  │ │[qt] Sair         ││
│                 │  │ └──────────────────┘│
│                 │  │                      │
│                 │  │ Login é habilitado! ││
│                 │  │ Dados carregados!   ││
│                 │  │                      │
└─────────────────┘  └──────────────────────┘
```

---

## 🔐 Fluxo Login

```
┌───────────────────┐
│  [lg] Login       │
└────────┬──────────┘
         │
         ▼
┌──────────────────────────┐
│ Informe o CPF:           │
│ (validar_cpf?)           │
└────────┬─────────────────┘
         │
    ┌────┴────┐
 Inválido│      │Válido
    │         │
    ▼         ▼
┌────────────────────┐  ┌──────────────────────┐
│ "CPF Inválido"     │  │ usuario_existe(cpf)? │
│ Loop para novo     │  └────────┬─────────────┘
│ CPF               │           │
└────────────────────┘        ┌──┴──┐
                            NÃO│    │SIM
                              │     │
                              ▼     ▼
                         ┌────────┐ ┌──────────────────┐
                         │"Não    │ │obter_contas_     │
                         │encontr.│ │usuario(cpf)      │
                         └────────┘ └────────┬─────────┘
                                            │
                                            ▼
                                    ┌──────────────────┐
                                    │contas_do_usuario │
                                    │(lista)           │
                                    └────────┬─────────┘
                                             │
                                             ▼
                                    ┌──────────────────────┐
                                    │ Listar contas:       │
                                    │ [1] Conta 1 - Saldo  │
                                    │ [2] Conta 2 - Saldo  │
                                    │ Selecione: _         │
                                    └────────┬─────────────┘
                                             │
                                             ▼
                                    ┌──────────────────────┐
                                    │ conta_ativa = {...}  │
                                    │ Menu completo        │
                                    │ habilitado!          │
                                    └──────────────────────┘
```

---

## 💰 Fluxo Depositar

```
┌────────────────────┐
│  [de] Depositar    │
│  (requer login)    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────────┐
│ Quanto deseja?         │
│ Informe valor: _       │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────┐
│ valor > 0?             │
│ & valor é número?      │
└─────────┬──────────────┘
          │
      ┌───┴───┐
    NÃO│       │SIM
      │        │
      ▼        ▼
┌────────────────────┐  ┌───────────────────────┐
│ "Valor inválido"   │  │ contar_transacoes()   │
│ Loop para novo     │  │ (do dia na conta)     │
│ valor              │  └──────┬────────────────┘
└────────────────────┘         │
                               ▼
                      ┌────────────────────┐
                      │ > 10 transações?   │
                      └─────┬──────┬───────┘
                          SIM│      │NÃO
                             │      │
                             ▼      ▼
                        ┌──┐  ┌────────────────┐
                        │❌│  │ depositar()    │
                        └──┘  │ (adiciona no   │
                              │  histórico)    │
                              └───┬────────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │ adicionar_transacao│
                        │_csv(tipo='depósit.│
                        │, valor, saldo...)  │
                        └───┬────────────────┘
                            │
                            ▼
                        ┌────────────────────┐
                        │ transacoes.csv     │
                        │ (salvo)            │
                        │                    │
                        │ "Depósito OK!"     │
                        │ "Saldo: R$ XXX"    │
                        └────────────────────┘
```

---

## 🏦 Fluxo Sacar

```
┌───────────────────┐
│  [sa] Sacar       │
│  (requer login)   │
└────────┬──────────┘
         │
         ▼
┌────────────────────────┐
│ Quanto deseja sacar?   │
│ Valor: _               │
└─────────┬──────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│ Validações (ordem de verificação):         │
│                                            │
│ 1. valor > 0?                              │
│ 2. valor <= 500 (limite)?                  │
│ 3. saldo_conta >= valor?                   │
│ 4. contar_saques_dia() < 3?                │
│ 5. contar_transacoes_dia() < 10?           │
└─────────┬──────────────────────────────────┘
          │
      ┌───┴──────────────────────────┐
    FALHA│                            │OK
      │                              │
      ▼                              ▼
┌──────────────────┐    ┌────────────────────────┐
│ Mensagem de Erro │    │ sacar()               │
│ (qual validação) │    │ (remove na conta)     │
│                  │    └───┬────────────────────┘
│ [1] Valor negativo│        │
│ [2] Limite R$500  │        ▼
│ [3] Saldo insuf.│        ┌────────────────────┐
│ [4] Max 3 saques  │        │ adicionar_transacao│
│ [5] Max 10 transac.│      │_csv(tipo='saque',  │
│                  │        │ valor, saldo...)   │
└──────────────────┘        └───┬────────────────┘
                                │
                                ▼
                        ┌──────────────────────┐
                        │ transacoes.csv       │
                        │ (salvo)              │
                        │                      │
                        │ "Saque OK!"          │
                        │ "Saldo: R$ XXX"      │
                        └──────────────────────┘
```

---

## 👤 Fluxo Novo Usuário

```
┌──────────────────────┐
│  [nu] Novo Usuário   │
└─────────┬────────────┘
          │
          ▼
┌─────────────────────────────┐
│ CPF (11 dígitos): _         │
└─────────┬───────────────────┘
          │
          ▼
┌─────────────────────────────┐
│ validar_cpf()?              │
└─────────┬─────────┬─────────┘
         SIM        NÃO
          │           │
          ▼           ▼
┌──────────────────┐  ┌─────────────────┐
│usuario_existe()?│  │ "CPF Inválido"  │
└─────────┬──────┬┘  │ Loop novo CPF   │
        SIM│    │NÃO └─────────────────┘
          │     │
          ▼     ▼
     ┌──┐ ┌──────────────────┐
     │❌│ │ Nome completo: _ │
     └──┘ └────────┬─────────┘
                   │
                   ▼
          ┌────────────────────┐
          │Data (dd/mm/yyyy): _│
          └────────┬───────────┘
                   │
                   ▼
          ┌──────────────────────────┐
          │ Endereço:                │
          │ Rua, 100 - Bairro - ..._│
          │                          │
          │ validar_endereco()?      │
          └─────────┬───────────┬────┘
                  NÃO│         │SIM
                    │          │
                    ▼          ▼
              ┌────────┐  ┌──────────────────┐
              │❌Erro  │  │adicionar_usuario │
              │        │  │_csv(...)         │
              └────────┘  └──────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ usuarios.csv           │
                    │ (novo usuário salvo!)  │
                    │                        │
                    │ "Usuário criado OK!"   │
                    └────────────────────────┘
```

---

## 🏠 Fluxo Nova Conta

```
┌──────────────────┐
│  [nc] Nova Conta │
└────────┬─────────┘
         │
         ▼
┌────────────────────────┐
│ CPF do usuário: _      │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ usuario_existe(cpf)?   │
└─────────┬──────┬───────┘
        SIM│      │NÃO
         │       │
         ▼       ▼
┌─────────────┐  ┌──────────────────┐
│ Obter user  │  │ "Usuário não     │
│ obter_user_ │  │  encontrado"      │
│ (cpf)       │  │ Loop novo CPF     │
└────────┬────┘  └──────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ carregar_contas()              │
│ contar_contas_usuario(cpf)     │
│ numero_conta = len(...) + 1    │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ adicionar_conta_csv(            │
│   cpf,                          │
│   agencia='0001',              │
│   numero_conta=X,              │
│   data_criacao=agora()         │
│ )                              │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────────┐
│ contas.csv                     │
│ (nova conta salva!)            │
│                                │
│ "Conta criada!"                │
│ "Agência: 0001"                │
│ "Número: X"                    │
└────────────────────────────────┘
```

---

## 🏗️ Arquitetura em Camadas

```
┌────────────────────────────────────────────┐
│          APRESENTAÇÃO (UI)                 │
│                                            │
│  menu_primeira_execucao()                  │
│  menu_dados_existentes()                   │
│  Entrada de dados com input()              │
│  Saída com print()                         │
└────────────────┬─────────────────────────┘
                 │
        ┌────────▼────────┐
        │ main_v4.0.py   │
        └────────┬────────┘
                 │
┌────────────────▼─────────────────────────┐
│       LÓGICA DE NEGÓCIO                 │
│                                         │
│  novo_usuario()      depositar()        │
│  nova_conta()        sacar()            │
│  login_conta()       exibir_extrato()   │
│                                         │
│  Validações:                           │
│  - validar_cpf()                       │
│  - validar_endereco()                  │
│  - contar_transacoes()                 │
│                                         │
│  Padrões Avançados:                    │
│  - @log_transacao (decorator)          │
│  - ContaIterador (iterator)            │
│  - gerar_relatorio() (generator)        │
└────────────────┬──────────────────────┘
                 │
        ┌────────▼────────┐
        │ csv_manager.py │
        └────────┬────────┘
                 │
┌────────────────▼────────────────────────┐
│        PERSISTÊNCIA (DATA LAYER)        │
│                                         │
│  inicializar_csvs()                     │
│  carregar_usuarios()                    │
│  adicionar_usuario_csv()                │
│  obter_contas_do_usuario()              │
│  adicionar_transacao_csv()              │
│  obter_saldo_conta()                    │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       ARMAZENAMENTO (CSV FILES)         │
│                                         │
│  usuarios.csv                           │
│  contas.csv                             │
│  transacoes.csv                         │
└─────────────────────────────────────────┘
```

---

## 💾 Fluxo de Dados CSV

```
EXECUÇÃO DO PROGRAMA
         │
         ▼
┌──────────────────────────┐
│  inicializar_csvs()      │
│  (cria se não existem)   │
└──────────┬───────────────┘
           │
           ├─► usuarios.csv (vazio)
           ├─► contas.csv (vazio)
           └─► transacoes.csv (vazio)
           │
           ▼
┌──────────────────────────┐
│  carregar_usuarios()     │
├──────────────────────────┤
│ Lê usuarios.csv          │
│ Retorna lista de dicts   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  OPERAÇÃO REALIZADA      │
│  [nu] novo_usuario()     │
│  [nc] nova_conta()       │
│  [de] depositar()        │
│  [sa] sacar()            │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  SALVAR EM CSV           │
├──────────────────────────┤
│  usuario → usuarios.csv  │
│  conta → contas.csv      │
│  transação → transacoes. │
│                csv       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  PRÓXIMA EXECUÇÃO        │
├──────────────────────────┤
│  [lg] Faz login          │
│  CPF já existe!          │
│  Contas carregadas!      │
│  Saldo restaurado!       │
└──────────────────────────┘
```

---

## 📊 Diagrama ER de Dados

```
┌─────────────────────────────────────────┐
│           USUÁRIOS                      │
├─────────────────────────────────────────┤
│ ⭐ cpf         (Primary Key)             │
│   nome                                  │
│   data_nascimento                       │
│   endereco                              │
└────────────┬────────────────────────────┘
             │
             │ 1 para N
             │
             ▼
┌─────────────────────────────────────────┐
│           CONTAS                        │
├─────────────────────────────────────────┤
│ ⭐ (cpf, numero_conta)  (Composite Key) │
│   cpf         (FK para usuarios)        │
│   agencia                               │
│   numero_conta                          │
│   data_criacao                          │
│   saldo       (deprecado/calculado)     │
└────────────┬────────────────────────────┘
             │
             │ 1 para N
             │
             ▼
┌─────────────────────────────────────────┐
│         TRANSAÇÕES                      │
├─────────────────────────────────────────┤
│   cpf         (FK para usuarios)        │
│   numero_conta (FK para contas)         │
│ ⭐ (cpf, numero, data_hora) (Composite) │
│   tipo        ('deposito' ou 'saque')   │
│   valor                                 │
│   data_hora                             │
│   saldo_apos                            │
└─────────────────────────────────────────┘

RELACIONAMENTOS:
  usuarios 1──N contas
  contas   1──N transacoes
  (intermediado por cpf e numero_conta)

INTEGRIDADE REFERENCIAL:
  ✓ CPF em contas deve existir em usuarios
  ✓ (cpf, numero_conta) em transacoes deve existir em contas
```

---

## 🎭 Máquina de Estados

```
┌────────────────────────────────────┐
│      ESTADO: PROGRAMA INICIADO     │
├────────────────────────────────────┤
│  Ação: inicializar_csvs()          │
│  Resultado: CSVs criados           │
│  Transição: PROGRAMA_PRONTO        │
└────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────┐
│   ESTADO: PROGRAMA_PRONTO          │
├────────────────────────────────────┤
│  Ação: dados_existem()?            │
│                                    │
│  ┌─► SIM          (dados existem)  │
│  │   Transição: MENU_COMPLETO     │
│  │                                 │
│  └─► NÃO          (sem dados)      │
│      Transição: MENU_PRIMARIO      │
└────────────────────────────────────┘
     │
     ├──────┬─────────────────┐
     │      │                 │
     ▼      ▼                 ▼
┌──────┐ ┌────────┐ ┌───────────────────┐
│Menu  │ │ Menu  │ │ Estado: SEM_DADOS │
│Prim. │ │ Compl.│ │ Opções:           │
│Opç:  │ │ Opç: │ │  [nu] [nc] [qt]   │
│ [nu] │ │ [lg] │ │ Sem login         │
│ [nc] │ │ [de] │ │ Sem operações     │
│ [qt] │ │ [sa] │ │ Sem histórico     │
│      │ │ [ex] │ │                   │
└─┬──┬┘ │ [rel]│ │ Transições:       │
  │  │  │ [lc] │ │ [nu] → +usuario   │
  │  │  │ [lu] │ │ [nc] → +conta     │
  │  │  │ [it] │ │ [qt] → EXIT       │
  │  │  │ [qt] │ └───────────────────┘
  │  │  └──┬──┘
  │  │     │
  │  │     ▼
  │  │   ┌──────────────────────┐
  │  │   │Estado: COM_DADOS     │
  │  │   │ Opções completas     │
  │  │   │ Login habilitado      │
  │  │   │                       │
  │  │   │ Transições:          │
  │  │   │ [lg] → LOGIN_PENDENTE│
  │  │   │ [qt] → EXIT          │
  │  │   └──────┬───────────────┘
  │  │          │
  │  │    ┌─────▼──────┐
  │  │    │ LOGIN_PEND.│
  │  │    │ (selec conta)
  │  │    └─────┬──────┘
  │  │          │
  │  │          ▼
  │  │   ┌─────────────────┐
  │  │   │Estado: LOGIN_OK │
  │  │   │ Conta ativa:    │
  │  │   │  cpf            │
  │  │   │  usuario        │
  │  │   │  numero_conta   │
  │  │   │                 │
  │  │   │ Transições:    │
  │  │   │ [de] →deposit  │
  │  │   │ [sa] → saque   │
  │  │   │ [ex] →extrato  │
  │  │   │ [qt] → EXIT    │
  │  │   └─────────────────┘
  │  │
  │  └──────► [...todos levam para...]
  │
  └────────────┬──────────────────────┐
               ▼                      ▼
          ┌──────┐            ┌──────────┐
          │ EXIT │            │ ERRO/    │
          │      │            │ VOLTAR   │
          └──────┘            └──────────┘
```

---

## 🔄 Fluxo de Persistência

### Ciclo Completo Usuario

```
[1] Usuario preenche dados
    └─► nome, cpf, data, endereco
           │
[2] Validações
    └─► validar_cpf()
    └─► validar_endereco()
    └─► usuario_existe(cpf)?
           │
[3] Se passou em todas
    └─► novo_usuario()
           │
[4] Salva em CSV
    └─► adicionar_usuario_csv()
           │
           ▼
    usuarios.csv ← nova linha
           │
[5] Próxima execução
    └─► carregar_usuarios()
           │
[6] Usuario carregado na memória
    └─► pode fazer login
```

### Ciclo Completo Transação

```
[1] Usuario autenticado ([lg])
    └─► conta_ativa = {...}
           │
[2] Operação (depositar ou sacar)
    └─► [de] ou [sa]
           │
[3] Entrada de dados
    └─► valor
           │
[4] Validações
    └─► valor > 0?
    └─► limite?
    └─► saldo?
    └─► saques/dia?
    └─► transações/dia?
           │
[5] Se passou
    └─► calcula novo saldo
    └─► saldo_novo = obter_saldo_conta(...) + valor
           │
[6] Registra em CSV
    └─► adicionar_transacao_csv(
            tipo='deposito'/'saque',
            valor,
            saldo_apos=saldo_novo
        )
           │
           ▼
    transacoes.csv ← nova linha
           │
[7] Próxima operação [ex] (extrato)
    └─► obter_transacoes_conta(cpf, numero_conta)
           │
[8] Renderiza histórico
    └─► gerar_relatorio_transacoes()
```

---

## 🔐 Fluxo de Segurança e Validações

```
ENTRADA DE DADOS
      │
      ▼
┌─────────────────────────┐
│  Validação de Tipo      │
│  (int, str, float)      │
└─────────┬───────────────┘
          │
    ┌─────┴──────┐
   NÃO│          │OK
     │           │
     ▼           ▼
┌──────┐  ┌─────────────────────────┐
│Erro  │  │ Validação Específica    │
│Retry │  │  - CPF (11 dígitos)     │
└──────┘  │  - Endereço (formato)   │
          │  - Valores (> 0)        │
          │  - Limites (R$ 500)     │
          │  - Contagens (3 saques) │
          │  - Duplicação (CPF)     │
          └─────────┬───────────────┘
                    │
              ┌─────┴──────┐
             NÃO│          │OK
               │           │
               ▼           ▼
          ┌──────┐   ┌────────────┐
          │Erro  │   │ Persistência
          │Retry │   │ (CSV)      │
          └──────┘   └────────────┘
```

---

## 📈 Volume de Dados Esperado

```
PRIMEIRA EXECUÇÃO
├─ usuarios.csv       (0 registros + header)
├─ contas.csv         (0 registros + header)
└─ transacoes.csv     (0 registros + header)


APÓS CRIAR 3 USUARIOS E 2 CONTAS
├─ usuarios.csv       (3 registros + header)
├─ contas.csv         (2 registros + header)
└─ transacoes.csv     (0 registros + header)


APÓS REALIZAR 50 TRANSAÇÕES
├─ usuarios.csv       (3 registros + header)
├─ contas.csv         (2 registros + header)
└─ transacoes.csv     (50 registros + header)


TAMANHO ESTIMADO
├─ usuarios.csv       ≈ 200-300 bytes
├─ contas.csv         ≈ 150-200 bytes
└─ transacoes.csv     ≈ 2KB per 100 transações
                      Total: < 1MB para 1000 transações
```

---

## ⏱️ Performance: Timeline de Operação

```
OPERAÇÃO: Fazer Depósito

inicio
  ├─► [de] menu item               (< 1ms)
  ├─► Pedir valor                  (blocking I/O - user input)
  ├─► Validar valor                (< 1ms)
  ├─► contar_transacoes_dia()      (lê transacoes.csv - 1-5ms)
  ├─► Validar limite               (< 1ms)
  ├─► obter_saldo_conta()          (lê transacoes.csv - 1-5ms)
  ├─► Validar saldo                (< 1ms)
  ├─► adicionar_transacao_csv()    (escreve transacoes.csv - 5-10ms)
  └─► Mostra resultado             (< 1ms)
fim

Total: ~10-25ms (excluindo I/O do usuário)

Para 100 transações: < 100ms
Para 1000 transações: < 500ms
Para 10000 transações (limite prático): ~2-3s

NOTA: CSV começa a ficar lento em 10K+ registros.
      Para produção, considere banco de dados SQL.
```

---

## 🎯 Resumo Executivo dos Fluxos

| Fluxo | Entrada | Saída | Local Principal |
|-------|---------|-------|-----------------|
| Login | CPF, seleção de conta | conta_ativa | main_v4.0.py |
| Depositar | Valor | CSV transação | csv_manager.py |
| Sacar | Valor | CSV transação | csv_manager.py |
| Novo Usuário | CPF, nome, data, endereço | CSV usuário | csv_manager.py |
| Nova Conta | CPF | CSV conta | csv_manager.py |
| Extrato | - | Console output | main_v4.0.py |
| Iterador | - | Console output | main_v4.0.py |
| Relatório | Tipo (dep/saq) | Console output | main_v4.0.py |

---

## 🔗 Relacionamentos Chave

```
Usuario [1..1] ──── [0..N] Contas
         cpf                  cpf (FK)
         
Contas [1..1] ──── [1..N] Transações
  cpf+numero      cpf+numero (FK)
  
Menu ──► Função ──► Operação CSV ──► Arquivo
         
Iterador ──► Contas ──► Loop de exibição
         
Gerador ──► Transações ──► Filtragem lazy
```

---

**Data:** 10 de Abril de 2026  
**Versão:** 4.0  
**Status:** ✅ Completo