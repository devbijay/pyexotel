# PyExotel

Welcome to PyExotel, an unofficial Python package for interacting with Exotel's API. With PyExotel, you can easily make phone calls, manage campaigns, and gather information about calls and phone numbers using your Exotel API credentials.

## Installation
To install pyexotel, use `pip`:
```shell
pip install pyexotel
```
## Usage
To use PyExotel, you will first need to create an instance of the Exotel class with your Exotel API key, API secret, SID, and domain. You can find these credentials in the Exotel Dashboard.

```python
from pyexotel import Exotel

dialer = Exotel(api_key="exotel_api_key", api_secret="exotel_api_secret", sid='exotel_sid', domain="exotel_domain")
```
With the `Exotel` instance, you can now use the various methods available to interact with the Exotel API. Some of the things you can do include:

### Place a Call
To place a call from one phone number (agent_number) to another (customer_number), use the call method:

```python
response = dialer.call(agent_number="NumberA", customer_number="numberB", called_id="exotel_callerID")
```

### Connect a Call to a Flow
To connect a call from a customer (`customer_number`) to a specific flow (or applet) using Exotel's API, use the `connect_flow` method:

```python
response = dialer.connect_flow(customer_number, called_id, flow_id)
```
### Get Call Information
To get information about a call, such as its timing and recording URL, use the `get_call_info` method:


```python
exotel.get_call_info(call_sid="call_sid")
```
### Get Phone Information
To get information about a phone number, such as its operator name and DND status, use the `get_phone_info` method:

```python
response = dialer.get_call_info(call_sid)
```

Each of these methods returns a JSON object containing the response from the Exotel server.

## Error Handling
In case of any errors, the Exotel methods will raise an exception. It is recommended to handle these exceptions in your code to gracefully handle any errors that may occur.

For example:

```python
try:
    response = exotel.call(agent_number="agent_number", customer_number="customer_number", caller_id="caller_id")
except Exception as e:
    print(f"An error occurred: {e}")
```

## Note
Exotel's V3 API is currently in beta testing and is not yet supported by this SDK.

## Support
If you have any questions or issues with PyExotel, please feel free to open an issue on the [GitHub repository](https://github.com/devbijay/pyexotel). I will do my best to assist you.

## Contribution
If you would like to contribute to PyExotel, please feel free to open a pull request on the [GitHub repository](https://github.com/devbijay/pyexotel). Your contributions are always welcome.