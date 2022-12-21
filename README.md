[![Upload Python Package](https://github.com/devbijay/exotelsdk/actions/workflows/python-publish.yml/badge.svg)](https://github.com/devbijay/exotelsdk/actions/workflows/python-publish.yml)

## Exotel SDK (Unofficial): Using V1 API
This is an unofficial sdk of exotel api that enables placing calls and other functionalities using your exotel api credentials
## How To Use
* Install The Package
```python
pip install exotelsdk
```

* Create A Exotel Call Instance
```python
from exotelsdk import Exotel
dialer = Exotel(sid='exotel_sid', api="exotel_api_key", secret="exotel_api_secret", domain="exotel_domain")
```

* Place a Call from numberA to numberB
```python
call = dialer.call(agent_number="NumberA", customer_number="numberB", called_id="exotel_callerID")
```

* Connect A Call To Existing Flow
```python
call = dialer.connect_flow(customer_number, called_id, flow_id)
```
* Get Information About A Call Such As Timing & Recording Url etc
```python
call = dialer.get_call_info(call_sid)
```
* Get Information About A Phone Number Such As Operator Name, DND Status Etc
```python
call = dialer.get_phone_info(phone_number)
```
Every Method returns a json response from exotel server.
Exotel V3 API is still in beta testing.
