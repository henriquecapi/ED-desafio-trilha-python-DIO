# Plano de Implementação - Sistema Bancário v5.0 (Refatoração para POO)

Este plano descreve a refatoração do Sistema Bancário da versão 4.0 (procedural) para a versão 5.0 (Orientada a Objetos), seguindo os conceitos aprendidos na trilha de Python da DIO.

## Mudanças Propostas

### 1. Definição do Modelo (main.py)
Introduziremos a estrutura de classes baseada no estudo do `desafio_v2.py`, mas adaptada para funcionar com a sua persistência CSV existente.

#### Hierarquia de Classes:
- **`Historico`**: Gerencia uma lista de transações.
- **`Transacao` (ABC)**: Interface abstrata com o método `registrar(conta)`.
    - **`Deposito`**: Implementação concreta.
    - **`Saque`**: Implementação concreta.
- **`Cliente`**: Classe base para clientes do banco.
    - **`PessoaFisica`**: Implementação específica com CPF e nome.
- **`Conta`**: Classe base para contas.
    - **`ContaCorrente`**: Implementação específica que lida com `limite` e `limite_saques`. Encapsula a `AGENCIA` ("0001") como um atributo de classe.

### 2. Atualização do CSV Manager (csv_manager.py)
Atualizar o gerenciador para atuar como uma Camada de Acesso a Dados (DAL) que comunica entre os arquivos CSV e os modelos POO.
- **`carregar_usuarios`**: Deve agora retornar uma lista de objetos `PessoaFisica`.
- **`carregar_contas`**: Deve agora retornar uma lista de objetos `ContaCorrente`.
- **`salvar_dados`**: Garantir que, quando os objetos forem atualizados, as linhas correspondentes no CSV sejam sincronizadas.

### 3. Lógica Principal e Menu (main.py)
- **Métodos do Menu**: Refatorar `depositar`, `sacar`, `exibir_extrato`, etc., para usar os métodos definidos nas classes (ex: `cliente.realizar_transacao(conta, transacao)`).
- **Encapsulamento**: Remover as constantes globais `AGENCIA`, `LIMITE`, `LIMITE_SAQUES` e usar atributos de classe/propriedades de instância.
- **Decoradores/Iteradores**: Manter o atual `@log_transacao` e `ContaIterador`, integrando-os aos métodos das classes.

## Considerações Importantes

> [!IMPORTANT]
> **Integridade de Dados**: Garantirei que os formatos existentes de `usuarios.csv`, `contas.csv` e `transacoes.csv` permaneçam compatíveis. Os objetos serão mapeados para essas colunas existentes.

> [!NOTE]
> **Refatoração da Lógica do Menu**: O loop `main()` atual será atualizado para lidar com os objetos `Cliente` e `Conta` em vez de dicionários.

## Plano de Verificação

### Testes Automatizados (Verificação Manual)
1. Executar o sistema.
2. Criar um usuário e uma conta.
3. Realizar um depósito e verificar a atualização do CSV.
4. Realizar um saque excedendo o limite e verificar a falha.
5. Realizar um saque dentro do limite e verificar o sucesso.
6. Listar contas usando o `ContaIterador`.

### Verificação Manual
- Executar o software e percorrer os fluxos comuns de usuário.
