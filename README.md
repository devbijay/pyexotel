# PyExotel ()

Welcome to PyExotel, an unofficial Python package for interacting with Exotel's API. With PyExotel, you can easily make phone calls, manage campaigns, and gather information about calls and phone numbers using your Exotel API credentials.

## Installation
To install pyexotel, use `pip`:
``` terminal
pip install pyexotel
```
## Usage
To use PyExotel, you will first need to create an instance of the Exotel class with your Exotel API key, API secret, SID, and domain. You can find these credentials in the Exotel Dashboard.

```python
from pyexotel import Exotel

exotel = Exotel(api_key="your_api_key", api_secret="your_api_secret", sid="your_sid", domain="your_domain")
```
With the `Exotel` instance, you can now use the various methods available to interact with the Exotel API. Some of the things you can do include:

* Place a phone call from one number to another:
```python
exotel.call(agent_number="agent_number", customer_number="customer_number", caller_id="caller_id")
```

* Connect a customer's call to a specific flow (or applet):

```python
exotel.connect_flow(customer_number="customer_number", caller_id="caller_id", flow_id="flow_id")
```
* Get information about a specific call, such as its timing and recording URL:
```python
exotel.get_call_info(call_sid="call_sid")
```
*Get information about a phone number, such as its operator name and DND status:
```python
exotel.get_phone_info(phone_number="phone_number")
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