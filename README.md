## PyExotel

Welcome to PyExotel, an unofficial Python package for interacting with Exotel's API. With PyExotel, you can easily make phone calls, manage campaigns, and gather information about calls and phone numbers using your Exotel API credentials.

## Installation

To install pyexotel, use `pip`:

```python
pip install pyexotel
```

## Exotel Class - Call Methods

To use PyExotel, you will first need to create an instance of the Exotel class with your Exotel API key, API secret, SID, and domain. You can find these credentials in the Exotel Dashboard.

```python
from pyexotel import Exotel

dialer = Exotel(api_key="exotel_api_key", api_secret="exotel_api_secret", sid='exotel_sid', domain="exotel_domain")
```
**Parameters**
* api_key (str): Your Exotel `API key`.
* api_secret (str): Your Exotel `API secret`.
* sid (str): Your Exotel `SID`.
* domain (str): Your Exotel domain, without the "`@`" part. If you want to use the user functionality
* For Singapore cluster, domain is : `ccm-api.exotel.com`
* For Mumbai cluster, domain is: `ccm-api.in.exotel.com`
* Default domain is: `ccm-api.exotel.com`

For `Exotel` instance, you can now use the various methods available to interact with the Exotel API. Some of the things you can do include:

### Place a Call

To place a call from one phone number (agent\_number) to another (customer\_number), use the call method:

```python
response = dialer.call(agent_number="NumberA", customer_number="numberB", caller_id="exotel_callerID")
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
response = dialer.get_phone_info(phone_number)
```

Each of these methods returns a JSON object containing the response from the Exotel server.

## Exotel Class - User Methods

The Exotel class provides several methods for managing users on Exotel's dashboard.

---

### _create\_user_

Creates a new user on Exotel's dashboard.  
**Parameters**

> *   first\_name (str): The first name of the user on Exotel's dashboard.
> *   last\_name (str): The last name of the user on Exotel's dashboard.
> *   user\_email (str): A unique and valid email ID of the user. If not set, the user will not be able to access Exotel's dashboard, but calls can be made via CCM APIs.
> *   user\_phone (str): The phone number of the user. It should be in E.164 format. For VOIP users, this is optional (SIP device will be auto-created).
> *   role (str): The role of the user on Exotel's dashboard. Possible values are "admin", "supervisor", and "user". The default value is "user" (which is an agent with the lowest level of access permissions).

---

### _**get\_user\_details**_

Retrieves the details of a single user, including their associated devices.

**Parameters**

> *   user\_id (str): The ID of the user to retrieve.

**Returns**

> *   (JSON): The response from the API request, containing the details of the user.

**Raises**

> *   (Exception): If an error occurs while making the API request.

---

### _**update\_user**_

Updates an existing user on Exotel's dashboard.

**Parameters**

> *   **user\_id** (str): The ID of the user to update.
> *   **data** (dict): A dictionary containing the following fields to update:

```python
data = {
         "first_name": First Name Of The User,
         "last_name": Last Name Of The User,
         "email": This is allowed only if email wasn't configured during Create User API.,
       }
```

**Returns**

> *   (JSON): The response from the API request, containing the updated details of the user.

**Raises**

> *   (Exception): If an error occurs while making the API request.

---

### _**set\_user\_status**_

Sets the availability status of a user on Exotel's dashboard.

**Parameters**

> *   **user\_id** (str): The ID of the user to update.
> *   **device\_id** (str): The ID of the device associated with the user.
> *   **status** (bool): The user's availability status (True for available, False for unavailable).
> *   **user\_phone** (str): An optional string representing the user's phone number, in E.164 format, to update the device's contact URI.

**Returns**

> *   (JSON): The response from the API request, containing the updated status of the user.

**Raises**

> *   (Exception): If an error occurs while making the API request.

---

### _**delete\_user**_

Deletes a user from Exotel's dashboard.

**Parameters**

> *   **user\_id** (str): The ID of the user to delete.

**Returns**

> *   (JSON): The response from the API request, containing the details of the deleted user.

**Raises**

> *   (Exception): If an error occurs while making the API request.

---

### _**get_all_users**_

Get All Users from Exotel's dashboard'

**Parameters**

>*   **fields (str, optional)**: A comma-separated list of fields to include in the response.
           Valid values are: "devices", "active_call", and "last_login".
           Default value is "devices,active_call,last_login"
**Returns**

> *   (JSON): A list of dictionaries containing information about the users.

**Raises**

> *   (Exception): If an error occurs while making the API request.

---


## Note

Exotel's V3 API is currently in beta testing and is not yet supported by this SDK.

## Support

If you have any questions or issues with PyExotel, please feel free to open an issue on the [GitHub repository](https://github.com/devbijay/pyexotel). I will do my best to assist you.

## Contribution

If you would like to contribute to PyExotel, please feel free to open a pull request on the [GitHub repository](https://github.com/devbijay/pyexotel). Your contributions are always welcome.