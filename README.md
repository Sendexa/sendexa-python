# Sendexa Python SDK

Official Python SDK for the Sendexa communications platform.

Install:

```bash
pip install sendexa
```

Example:

```python
from sendexa import Sendexa

sendexa = Sendexa(api_key="SENDEXA_API_KEY")

sendexa.sms.send(
    to="+233XXXXXXXXX",
    message="Hello from Sendexa"
)
```
