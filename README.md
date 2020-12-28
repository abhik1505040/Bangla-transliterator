# Bangla-transliterator

A rule based bengali romanization module.

## Details

Based on the `dakshina` dataset and custom rules added on top of `aksharamukha`.

**Exact details will be added soon.**

## Installation
```bash
python setup.py install
```

## Usage

```python
from romanizer import Transliterator
t = Transliterator() 
t.process_line('সে লাল গোলাপ পছন্দ করে।')

>>> 'se lal golap pochondo kore.'
```