import requests
import base64


class Exotel:
    """
        A class for interacting with Exotel API.

        Attributes:
        - api_key (str): Your Exotel API key.
        - api_secret (str): Your Exotel API secret.
        - sid (str): Your Exotel SID.
        - domain (str): Your Exotel domain, without the "@" part.
        - call_ep (str): The URL endpoint for making calls using Exotel API.
        - campaign_ep (str): The URL endpoint for managing campaigns using Exotel API.
        - auth_token (bytes): The base64-encoded authorization token for accessing Exotel API.

    Methods:
    - __init__(api_key, api_secret, sid, domain)
        Initializes an Exotel instance with the given API key, API secret, SID, and domain.

    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        sid: str,
        domain: str = "ccm-api.exotel.com",
    ):
        """
        Initializes an Exotel instance with the given API key, API secret, SID, and domain.

        Parameters:
        - api_key (str): Your Exotel API key.
        - api_secret (str): Your Exotel API secret.
        - sid (str): Your Exotel SID.
        - domain (str): Your Exotel domain, without the "@" part. If you want to use the user functionality
            -- For Singapore cluster, domain is : ccm-api.exotel.com
            -- For Mumbai cluster, domain is: ccm-api.in.exotel.com
            -- Default domain is: ccm-api.exotel.com
        """

        self.sid = sid
        self.call_ep = f"https://api.exotel.com/v1/Accounts/{sid}/Calls"
        self.users_ep = f"https://{domain}/v2/accounts/{self.sid}/users"

        self.auth_token = base64.b64encode(
            f"{api_key}:{api_secret}".encode("ascii")
        ).decode()
        self.get_header = {"Authorization": f"Basic {self.auth_token}"}
        self.post_header = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth_token}",
        }

    def call(
        self,
        agent_number: str,
        customer_number: str,
        caller_id: str,
        record: bool = True,
        time_limit: int = 14400,
        stream_url="",
    ):
        """
        Makes a phone call from the given agent number to the given customer number.

        Parameters:
        - agent_number (str): The phone number of the agent making the call.
        - customer_number (str): The phone number of the customer receiving the call.
        - caller_id (str): The caller ID that will be displayed to the customer.
        - record (bool, optional): Whether to record the call (defaults to True).
        - time_limit (int, optional): The maximum duration of the call in seconds
            (defaults to 14400 seconds, or 4 hours). Maximum value is 14400.
        - stream_url (str, optional): The URL of a stream to play during the call. Must be a valid websocket URL.

        Returns:
        - JSON object: A JSON object containing the response from the server.
        """

        try:
            data = {
                "From": str(agent_number),
                "To": str(customer_number),
                "CallerId": str(caller_id),
                "TimeLimit": int(time_limit),
                "Record": "true" if record else "false",
            }
            if stream_url:
                data["StreamUrl"] = stream_url

            response = requests.post(
                f"{self.call_ep}/connect.json", data=data, headers=self.get_header
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def connect_flow(
        self,
        customer_number: str,
        caller_id: str,
        flow_id: str,
        time_limit: int = 14400,
    ):
        """
        Connects a customer's call to a specific flow (or applet) using Exotel API.

        Parameters:
        - customer_number (str): The phone number of the customer making the call.
        - caller_id (str): The ExoPhone number to be displayed as the caller ID.
        - flow_id (str): The identifier of the flow (or applet) that you want to connect the customer's call to.
        - time_limit (int, optional): The time limit (in seconds) for the call. The call will be cut after this time
                                    (max. 14400 seconds, i.e. 4 hours). Default is 14400.

        Returns:
        - A JSON object with the response from Exotel API.
        """
        params = {
            "From": str(customer_number),
            "Url": f"http://my.exotel.com/{self.sid}/exoml/start_voice/{flow_id}",
            "CallerId": str(caller_id),
            "TimeLimit": int(time_limit),
        }
        try:

            response = requests.post(
                f"{self.call_ep}/connect.json", data=params, headers=self.get_header
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_call_info(self, call_sid: str):
        """
        Retrieves information about a specific call using Exotel API.

        Parameters:
        - call_sid (str): The Exotel Call Sid for the call.

        Returns:
        - A JSON object with the information about the call from Exotel API.
        """
        try:
            response = requests.get(
                f"{self.call_ep}/{call_sid}.json", headers=self.get_header
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_phone_info(self, phone_number: str):
        """
        Retrieves information about the given phone number, including the telecom circle, name, number type,
        and DND/non-DND status.

        Parameters:
        - phone_number (str): The phone number to retrieve information for.

        Returns:
        - A dictionary containing the following information about the phone number:
            - "PhoneNumber": The phone number.
            - "Circle": The telecom circle code.
            - "CircleName": The name of the telecom circle.
            - "Type": The type of phone number (e.g. "landline", "mobile", "voip").
            - "Operator": The operator code.
            - "OperatorName": The name of the operator.
            - "DND": "Yes" if the phone number is on the Do Not Disturb list, "No" otherwise.

        Raises:
        - ValueError: If the phone number is invalid or not found.
        """
        try:
            response = requests.get(
                f"https://api.exotel.com/v1/Accounts/{self.sid}/Numbers/{phone_number}.json",
                headers=self.get_header,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    # Exotel User Functionality
    def create_user(
        self,
        first_name: str,
        last_name: str,
        user_email: str,
        user_phone: str,
        role: str = "user",
    ):

        """
        Creates a new user on Exotel dashboard.

        Args:
            first_name (str): The first name of the user on Exotel dashboard.
            last_name (str): The last name of the user on Exotel dashboard.
            user_email (str): A unique and valid email ID of the user. If not set,
                              the user will not be able to access Exotel dashboard but calls can be made via CCM APIs.
            user_phone (str): The phone number of the user. It should be in E.164 format.
                              For VOIP users, this is optional (SIP device will be auto created).
            role (str): The role of the user on Exotel dashboard. Possible values are "admin", "supervisor", and "user".
                        Default value is "user" (which has low level of access permissions).

        Returns:
            JSON: The response from the API request, containing the details of the newly created user.

        Raises:
            Exception: If an error occurs while making the API request.
        """
        try:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": user_email,
                "device_contact_uri": str(user_phone),
                "role": role,
            }
            response = requests.post(
                self.users_ep,
                data=data,
                headers=self.post_header,
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_user_details(self, user_id: str):
        """
        Retrieves the details of a single user, including their associated devices.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            JSON: The response from the API request, containing the details of the user.

        Raises:
            Exception: If an error occurs while making the API request.
        """
        url = f"{self.users_ep}/{user_id}"
        try:
            response = requests.get(url, headers=self.get_header)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def update_user(self, user_id: str, data: dict):
        """
        Updates an existing user on Exotel dashboard.

        Args:
            user_id (str): The ID of the user to update.
            data (dict): data: {
             "first_name": First Name Of The User,
             "last_name": Last Name Of The User,
             "email": This is allowed only if email wasn't configured during Create User API.,
         }

        Returns:
            JSON: The response from the API request, containing the updated details of the user.

        Raises:
            Exception: If an error occurs while making the API request.
        """
        try:
            response = requests.put(
                f"{self.users_ep}/{user_id}",
                params=data,
                headers=self.post_header,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def delete_user(self, user_id: str):
        """
        Deletes a user from Exotel dashboard.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            JSON: The response from the API request, containing the details of the deleted user.

        Raises:
            Exception: If an error occurs while making the API request.
        """
        try:
            response = requests.delete(
                f"{self.users_ep}/{user_id}", headers=self.get_header
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def set_user_status(
        self, user_id: str, device_id: str, status: bool, user_phone: str = ""
    ):
        """
        Sets the availability status of a user on Exotel dashboard.

        Args:
            user_id (str): The ID of the user to update.
            device_id (str): The ID of the device associated with the user.
            status (bool): The user's availability status (True for available, False for unavailable).
            user_phone (str): An optional string representing the user's phone number, in E.164 format,
                              to update the device's contact URI.

        Returns:
            JSON: The response from the API request, containing the updated status of the user.

        Raises:
            Exception: If an error occurs while making the API request.
        """
        data = {"available": status}

        if user_phone:
            data["contact_uri"] = user_phone
        print(data)
        try:
            response = requests.put(
                f"{self.users_ep}/{user_id}/devices/{device_id}",
                params=data,
                headers=self.get_header,
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_all_users(self, fields="devices,active_call,last_login"):
        """
        Retrieves a list of all users from the Exotel API.

        Parameters:
        - fields (str, optional): A comma-separated list of fields to include in the response.
            Valid values are: "devices", "active_call", and "last_login".
            Default value is "devices,active_call,last_login".

        Returns:
        - List[Dict[str, Any]]: A list of dictionaries containing information about the users.
        """

        try:
            response = requests.get(
                f"{self.users_ep}?fields={fields}",
                headers=self.get_header,
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    # END Of Exotel User Functionality
