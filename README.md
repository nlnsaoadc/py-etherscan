# [Etherscan REST API](https://etherscan.io/) wrapper

[![py-etherscan-client-pypi](https://img.shields.io/pypi/v/py-etherscan-client.svg)](https://pypi.python.org/pypi/py-etherscan-client)

Etherscan REST API Doc: https://docs.etherscan.io/

## Install

```bash
pip install py-etherscan-client
```

## Usage

```python
from etherscan import Etherscan

es = Etherscan(key="<your-key-here>")
es.get_gas_oracle()
```

## Testing

```bash
virtualenv venv
source ./venv/bin/activate
pip install -r dev_requirements.txt
deactivate
source ./venv/bin/activate
pytest
```
