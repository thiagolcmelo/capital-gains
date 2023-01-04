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
$ ./setup.sh
```

Agora deve ser possível utilizar a CLI da seguinte forma:

```

```

## Extendendo a aplicação

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
