# Ganho de Capital

CLI para calcular o imposto a ser pago sobre lucros ou prejuízos de operações no mercado financeiro de ações.

## Mode de operação

Se instalada, a aplicação pode ser usada na linha de comando como demonstrado a seguir:

```
$ capital-gains < tests/data/case_01/input.txt
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]
```

```
$ capital-gains < tests/data/case_02/input.txt
[{"tax": 0.0}, {"tax": 10000.0}, {"tax": 0.0}]
```

```
capital-gains < tests/data/case_03/input.txt
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 1000.0}]
```

## Instalando a aplicação

Para somente instalar a aplicação, por favor, proceda da seguinte forma:

```
$ make test
$ make build
$ make install
```

Após a execução dos comandos acima, o comando `capital-gains` ficará acessível na linha de comando.

## Utilizando a aplicação com Docker

Existe um arquivo `setup.sh` na raiz do projeto que constrói uma imagem Docker e adiciona um alias no shell atual para que seja possível utilizar a CLI de dentro de um container baseado nesta imagem.

Para utilizar esta opção, procesa da seguinte forma:

```
$ source ./setup.sh
```

Agora é possível utilizar a CLI da seguinte forma:

```
$ capital-gains < tests/data/case_10/input.txt
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 1000.0}]
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 10000.0}]
[{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 3000.0}]
```

## Testando e extendendo a aplicação

Para extender a aplicação, por favor, crie um virtual environment e o ative:

```
$ python3 -m venv env
$ source env/bin/activate
```

Instale as bibliotecas utilizadas para desenvolvimento:

```
(env) $ pip install --upgrade pip
(env) $ pip install -r requirements-dev.txt
```

Execute os testes unitário e instale da seguinte forma:

```
(env) $ make test
(env) $ make build
(env) $ make install
```

Alternativamente:

```
(env) $ pytest
(env) $ python setup.py build
(env) $ python setup.py install
```

## Comentários

A aplicação utiliza o arquivo `src/cli.py` como ponto de entrada. Após capturar e interpretar a `stdin`, a classe `TaxCalculator` é utilizada para calcular os impostos que são impressos na `stdout` sequencialmente para cada linha contendo uma simulação independente.

Como buscava-se uma solução simples, a aplicação não recebe outros parâmetros.

A classe `TaxCalculator` possui apenas um método estático no momento (`calculate`) que cria uma objeto da classe `Simulation` para manter o estado de uma simulação. As operações são aplicadas sequencialmente ao estado (`Simulation`) utilizando seus métodos `buy` ou `sell`, sempre capturando a taxa correspondente a cada operação.

Uma opção funcional da forma `impostos = F(operacoes)` é totalmente factível, pois o resultado esperado é completamente determinado pela entrada. Entretanto, o número de regras sobre como aplicar o imposto e o carregamento de estados resulta em um código um pouco complexo.

Por esta razão acima, optou-se pela classe `Simulation` por permitir uma interface simples e um código um pouco mais limpo e fácil de entender:
- A classe é instanciada `simulation = Simulation()`, opcionalmente com valores iniciais de `total_stocks`, `weighted_average` e `loss`.
- A taxa sobre cada operação seguinte é obtida através dos métodos:
  - `tax = simulation.buy(operation)` (sempre zero).
  - `tax = simulation.sell(operation)` (dependendo da operação e do estado prévio).



Observações:

- Para desenvolvimento foram utilizadas as seguintes bibliotecas:
    - `black` para formatar o código.
    - `pytest` é um framework de testes que proporciona algumas facilidades e maior simplicidade quando comparado ao `unittest` dispível na biblioteca padrão o Python.
    - `coverage` para facilitar a visualização da cobertura de testes de forma sistemática.
- Seria interessante paralelizar o processamento das linhas. Uma ideia seria utilizar `ArgumentParser` para receber o número de processos paralelos desejado, algo como: `$ capital-gains -n 10 < arquivo.txt` para executar 10 linhas em paralelo por vez.
  - Mesmo paralelizando simulações, uma única lista de operações muito longa irá resultar em um longo tempo de processamento. Algumas otimizações são possíveis como agrupar operações de compra, mas um caso com operações do tipo `buy, sell, buy, sell, buy, ...` ainda será problemático.
- Os testes estão mais complexos do que o necessário e um pouco redundantes. O objetivo é cobrir a aplicação com testes da forma mais abrangente possível.
- O arquivo `setup.sh` apenas sugere como facilitar o uso da CLI diretamente a partir de dentro de um container, mas ele precisa ser aperfeiçoado para uso. Talvez a forma mais direta seria adicionar o alias diretamente ao arquivo `.bashrc` (ou análogo) do usuário.
- A classe `Simulation` não armazena as taxas todas, mas poderia case fosse necessário.
- Como a entrada é garantidamente livre de errors, não houve muito esforço para validação. Outros pequenos defeitos relacionados a isso são algumas strings "buy" e "sell" espalhadas pelo códico ao invés de utilizar uma enumeration como `OperationType.BUY` e `OperationType.SELL`.