# Capital Gains

CLI tool for calculating tax over stock market operations.


## Usage

These are a few examples:

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



## Building and Installing

For development, please create a virtual environment and activate it:

```
$ python3 -m venv env
$ source env/bin/activate
```

Install the required external libraries:

```
(env) $ pip install --upgrade pip
(env) $ pip install -r requirements-dev.txt
```

Please run the tests, build, and install as follows:

```
(env) $ pytest
(env) $ python setup.py build
(env) $ python setup.py install
```

Alternatively, using make, the tests can be triggered by:

```
(env) $ make test
```

The new distribution can be built and installed by:

```
(env) $ make build
(env) $ make install
```
