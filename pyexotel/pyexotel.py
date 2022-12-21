import requests, base64, json


class Exotel:
    """
        A class for interacting with Exotel's API.

        Attributes:
        - api_key (str): Your Exotel API key.
        - api_secret (str): Your Exotel API secret.
        - sid (str): Your Exotel SID.
        - domain (str): Your Exotel domain, without the "@" part.
        - call_ep (str): The URL endpoint for making calls using Exotel's API.
        - campaign_ep (str): The URL endpoint for managing campaigns using Exotel's API.
        - auth_token (bytes): The base64-encoded authorization token for accessing Exotel's API.

    Methods:
    - __init__(api_key, api_secret, sid, domain)
        Initializes an Exotel instance with the given API key, API secret, SID, and domain.

    """

    def __init__(self, api_key: str, api_secret: str, sid: str, domain: str):
        """
            Initializes an Exotel instance with the given API key, API secret, SID, and domain.

            Parameters:
            - api_key (str): Your Exotel API key.
            - api_secret (str): Your Exotel API secret.
            - sid (str): Your Exotel SID.
            - domain (str): Your Exotel domain, without the "@" part.
        """

        self.api_key = api_key
        self.api_secret = api_secret
        self.sid = sid
        self.domain = domain
        self.call_ep = f"https://{self.api_key}:{self.api_secret}@{self.domain}/v1/Accounts/{self.sid}/Calls"
        self.campaign_ep = f"https://{self.api_key}:{self.api_secret}@{self.domain}/v2/accounts/{self.sid}/campaigns"
        self.auth_token = base64.b64encode(f"{api_key}:{api_secret}".encode('ascii'))

    def call(self, agent_number: str, customer_number: str, caller_id: str, record: bool = True,
             time_limit: int = 14400,
             stream_url=""):
        """
        Makes a phone call from the given agent number to the given customer number.

        Parameters:
        - agent_number (str): The phone number of the agent making the call.
        - customer_number (str): The phone number of the customer receiving the call.
        - caller_id (str): The caller ID that will be displayed to the customer.
        - record (bool, optional): Whether to record the call (defaults to True).
        - time_limit (int, optional): The maximum duration of the call in seconds (defaults to 14400 seconds, or 4 hours). Maximum value is 14400.
        - stream_url (str, optional): The URL of a stream to play during the call. Must be a valid websocket URL.

        Returns:
        - JSON object: A JSON object containing the response from the server.
        """

        try:
            data = {
                'From': str(agent_number),
                'To': str(customer_number),
                'CallerId': str(caller_id),
                "TimeLimit": int(time_limit),
                'Record': "true" if record else "false",
            }
            if stream_url:
                data["StreamUrl"] = stream_url

            response = requests.post(f"{self.call_ep}/connect.json", data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def connect_flow(self, customer_number: str, caller_id: str, flow_id: str, time_limit: int = 14400):
        """
            Connects a customer's call to a specific flow (or applet) using Exotel's API.

            Parameters:
            - customer_number (str): The phone number of the customer making the call.
            - caller_id (str): The ExoPhone number to be displayed as the caller ID.
            - flow_id (str): The identifier of the flow (or applet) that you want to connect the customer's call to.
            - time_limit (int, optional): The time limit (in seconds) for the call. The call will be cut after this time (max. 14400 seconds, i.e. 4 hours). Default is 14400.

            Returns:
            - A JSON object with the response from Exotel's API.
        """
        try:
            params = {
                'From': str(customer_number),
                'Url': f"http://my.exotel.com/{self.sid}/exoml/start_voice/{flow_id}",
                'CallerId': str(caller_id),
                "TimeLimit": int(time_limit),
            }
            response = requests.post(f"{self.call_ep}/connect.json", params)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_call_info(self, call_sid: str):
        """
            Retrieves information about a specific call using Exotel's API.

            Parameters:
            - call_sid (str): The Exotel Call Sid for the call.

            Returns:
            - A JSON object with the information about the call from Exotel's API.
        """
        try:
            response = requests.get(f"{self.call_ep}/{call_sid}.json")
            response.raise_for_status()
            return response.json()

        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")

    def get_phone_info(self, phone_number: str):
        """
        Retrieves information about the given phone number, including the telecom circle, name, number type, and DND/non-DND status.

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
                f"https://{self.api_key}:{self.api_secret}@{self.domain}/v1/Accounts/{self.sid}/Numbers/{phone_number}.json")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # handle the exception here
            print(f"An error occurred: {e}")
