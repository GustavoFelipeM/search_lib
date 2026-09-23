# search_lib

Biblioteca desenvolvida para implementação e experimentação de algoritmos de busca em espaços de estados.

A `search_lib` fornece uma arquitetura modular para representar problemas, estados, ações e estratégias de busca. A estrutura permite adicionar novos problemas e algoritmos sem modificar o núcleo da biblioteca.

## Equipe

* **Gustavo Felipe**
* **Lucas Carvalho**
* **Cauan Abraão**

## Sobre o projeto

A biblioteca foi projetada para separar a representação de um problema da estratégia utilizada para solucioná-lo.

A arquitetura principal é composta por:

```text
Problem
├── State
├── Action
└── SearchStrategy
    └── SearchNode
```

Essa separação permite que diferentes problemas sejam executados utilizando diferentes algoritmos de busca.

## Componentes principais

| Componente       | Responsabilidade                                                       |
| ---------------- | ---------------------------------------------------------------------- |
| `State`          | Representa uma configuração ou estado do problema.                     |
| `Action`         | Representa uma transformação entre estados.                            |
| `Problem`        | Define as regras do problema, suas ações, objetivo e heurística.       |
| `SearchNode`     | Representa um nó durante a busca e mantém o estado, pai, ação e custo. |
| `SearchStrategy` | Define a estrutura base para os algoritmos de busca.                   |

## `State`

Representa uma configuração do problema.

Um estado deve permitir **comparação e hash**, pois pode ser utilizado em estruturas como `set` e `dict`. Sempre que possível, sua representação interna deve utilizar estruturas imutáveis, como `tuple` ou `frozenset`.

## `Action`

Representa uma ação capaz de transformar um estado em outro.

O método `apply(state)` deve:

* receber o estado atual;
* retornar o novo estado quando a ação for válida;
* retornar `None` quando a ação não puder ser aplicada.

Ações não devem alterar diretamente o estado recebido.

## `Problem`

Representa as regras e características do problema de busca.

Toda implementação deve fornecer:

* `actions(state)` — retorna as ações válidas para o estado;
* `is_goal(state)` — verifica se o estado é um estado objetivo;
* `heuristic(state)` — fornece uma estimativa do custo restante, quando aplicável.

A classe `Problem` deve representar as regras do problema e não controlar o estado da busca. Informações como estados visitados devem ser responsabilidade da estratégia de busca.

## `SearchNode`

Representa um nó gerado durante a busca.

Cada nó mantém:

| Atributo | Responsabilidade                    |
| -------- | ----------------------------------- |
| `state`  | Estado representado pelo nó.        |
| `parent` | Nó que gerou o estado atual.        |
| `action` | Ação utilizada para gerar o nó.     |
| `cost`   | Custo acumulado desde o nó inicial. |

A relação entre `parent` e os nós permite reconstruir o caminho encontrado pela busca.

## `SearchStrategy`

Classe base para implementação dos algoritmos de busca.

Novos algoritmos devem estender `SearchStrategy` e utilizar a interface fornecida pelo núcleo da biblioteca.

Podem ser implementadas estratégias como:

* Busca em Largura (BFS);
* Busca em Profundidade (DFS);
* Busca de Custo Uniforme;
* Busca Gulosa;
* A*;
* IDA*;
* RBFS;
* Busca Bidirecional.

A estratégia de busca é responsável pelo controle da fronteira, dos estados explorados e das características específicas do algoritmo.

## Tree Search e Graph Search

A distinção entre Tree Search e Graph Search deve ser tratada pela estratégia de busca.

**Tree Search** permite que um mesmo estado apareça mais de uma vez durante a exploração.

**Graph Search** mantém controle dos estados já explorados para evitar expansões desnecessárias e ciclos.

O controle de estados explorados deve permanecer na estratégia de busca, e não na classe `Problem`.

## Métricas

Estratégias utilizadas em experimentos podem coletar métricas para análise de desempenho, como:

| Métrica             | Descrição                              |
| ------------------- | -------------------------------------- |
| `nodes_expanded`    | Quantidade de nós expandidos.          |
| `max_frontier_size` | Maior tamanho atingido pela fronteira. |
| `execution_time`    | Tempo de execução do algoritmo.        |
| `cost`              | Custo da solução encontrada.           |

As métricas devem ser mantidas separadas da representação do problema.

## Adição de novos problemas

A implementação de um novo problema deve seguir a estrutura:

1. Criar uma implementação de `State` para representar suas configurações.
2. Criar as `Action` necessárias para representar suas transições.
3. Criar uma implementação de `Problem` contendo suas regras.
4. Implementar `actions()`, `is_goal()` e `heuristic()` quando aplicável.
5. Validar o problema utilizando uma ou mais implementações de `SearchStrategy`.

O novo problema deve ser compatível com as abstrações existentes, sem exigir alterações no núcleo da biblioteca.

## Boas práticas

* Estados utilizados em estruturas de busca devem possuir igualdade e hash consistentes.
* Prefira representações imutáveis para os estados.
* `Action.apply()` deve retornar `None` para ações inválidas.
* Ações não devem modificar diretamente o estado recebido.
* `Problem` não deve controlar estados visitados ou informações específicas da execução da busca.
* `actions(state)` deve ser determinístico para um mesmo estado, quando a natureza do problema permitir.
* A lógica do problema, o algoritmo de busca, as métricas e a visualização devem permanecer separados.
* Novas implementações devem utilizar as abstrações existentes em vez de duplicar funcionalidades do núcleo.

## Extensibilidade

A arquitetura da `search_lib` permite combinar diferentes problemas com diferentes estratégias de busca:

```text
             search_lib
                  │
        ┌─────────┴─────────┐
        │                   │
     Problem          SearchStrategy
        │                   │
   ┌────┴────┐        ┌─────┴─────┐
   │         │        │           │
 State     Action     BFS         A*
                      │           │
                      └─────┬─────┘
                            │
                        SearchNode
```

O objetivo é manter o núcleo da biblioteca independente das implementações específicas, facilitando a criação de novos problemas, algoritmos e experimentos.
