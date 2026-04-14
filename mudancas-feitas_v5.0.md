# Mudanças Feitas - Sistema Bancário v5.0 (POO)

Concluí a refatoração completa do seu sistema bancário para o paradigma de **Programação Orientada a Objetos (POO)**. O sistema agora utiliza conceitos avançados como Herança, Polimorfismo, Classes Abstratas (ABC) e Encapsulamento, mantendo a persistência em CSV que já funcionava perfeitamente.

## Mudanças Principais

### 1. Novo Modelo de Dados (`models.py`)
Criei um arquivo centralizado para os modelos, separando a lógica de negócio da interface:
- **Herança**: `PessoaFisica` herda de `Cliente`. `ContaCorrente` herda de `Conta`.
- **Classes Abstratas**: `Transacao` é uma `ABC` (Abstract Base Class) com as implementações concretas `Deposito` e `Saque`.
- **Encapsulamento**: Atributos como `_saldo` e `_historico` são protegidos, e constantes como `AGENCIA` (0001) estão agora dentro das classes.

### 2. Camada de Persistência Inteligente (`csv_manager.py`)
O gerenciador de CSV foi evoluído para lidar com objetos Python:
- Implementei `carregar_usuarios_objetos` e `carregar_contas_objetos`.
- Ao carregar os dados, o sistema agora reconstrói todo o grafo de objetos, vinculando cada conta ao seu respectivo titular e restaurando o histórico de transações.

### 3. Refatoração da Interface (`main.py`)
A lógica do menu foi simplificada para utilizar os métodos das classes:
- **Polimorfismo**: As transações são processadas via `cliente.realizar_transacao(conta, transacao)`, onde `transacao` pode ser um depósito ou um saque.
- **Iteradores e Geradores**: O `ContaIterador` e o `gerar_relatorio_transacoes` foram atualizados para ler dados diretamente das propriedades das instâncias de classe.

## Como as constantes foram encapsuladas?

> [!IMPORTANT]
> Agora você não verá mais `AGENCIA`, `LIMITE` ou `LIMITE_SAQUES` como variáveis soltas no `main()`. Eles estão definidos dentro da classe `ContaCorrente`:
> - A `AGENCIA` é fixa em "0001" na classe base `Conta`.
> - O `LIMITE` (R$ 500,00) e `LIMITE_SAQUES` (3) são atributos de instância de `ContaCorrente`.

## Arquivos Criados/Modificados

- [main.py](file:///c:/Cursos/web.dio.me/Python/LuizaLabs-1/trilha-python-dio/Desafio/main.py): Refatorado para usar objetos.
- [csv_manager.py](file:///c:/Cursos/web.dio.me/Python/LuizaLabs-1/trilha-python-dio/Desafio/csv_manager.py): Novos métodos de carregamento de objetos.
- [models.py](file:///c:/Cursos/web.dio.me/Python/LuizaLabs-1/trilha-python-dio/Desafio/models.py): [NOVO] Definição de todas as classes do sistema.
- [PLANO_DE_ACAO_V5.md](file:///c:/Cursos/web.dio.me/Python/LuizaLabs-1/trilha-python-dio/Desafio/PLANO_DE_ACAO_V5.md): Plano de ação em português.

## Novas Funcionalidades Adicionadas
- **Log de Transações (Arquivo)**: Opção `[lt]` adicionada ao menu para visualizar as execuções de funções decoradas com `@log_transacao`, lendo diretamente do arquivo `log_transacoes.txt`.
- **Restauração do Padrão de Log**: Refatoração técnica usando *closures* para garantir que o arquivo `log_transacoes.txt` continue registrando argumentos primitivos (CPF, valor, etc.) em vez de endereços de memória de objetos, mantendo a compatibilidade com o histórico anterior.

---
Você pode agora testar o sistema normalmente. O funcionamento visual continua o mesmo, mas o "coração" do código agora segue as melhores práticas de POO que você está estudando!
