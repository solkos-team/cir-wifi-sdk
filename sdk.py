from typing import List, Optional
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

access_token = None
api_url = os.getenv('API_URL', default='https://cir-wifi-interface-b7agk5thba-uc.a.run.app')


def get_request_method(method: str):
    if method == 'post':
        return requests.post
    elif method == 'put':
        return requests.put
    elif method == 'get':
        return requests.get
    elif method == 'delete':
        return requests.delete

    return requests.get


def api_request(method: str, path, data: dict = None, add_token=True):
    req = get_request_method(method)

    if add_token:
        global access_token
        assert access_token is not None
        response = req(
            f'{api_url}/{path}',
            json=data,
            headers={'Authorization': f'Bearer {access_token}'}
        )
    else:
        response = req(
            f'{api_url}/{path}',
            json=data
        )

    error, obj = None, None

    if response.ok:
        obj = response.json()
    else:
        error = response

    return obj, error


def set_access_token(email: str, password: str):
    """Set the access token for given credentials 
    to allow use of sdk functions

    Args:
        email (str): user email
        password (str): user password
    """
    token, _ = login(email, password)

    if token:
        global access_token
        access_token = token


def login(email: str, password: str):
    """Login with user credentials and 
    returns the access token

    Args:
        email (str): user email
        password (str): user password

    Returns:
        str: access token 
    """
    return api_request('post', 'login', dict(email=email, password=password), False)


def create_customer(customer_id: str, name: str):
    """Root Only, create a customer

    Args:
        customer_id (str): id value for the customer
        name (str): customer name

    Returns:
        dict: customer data
    """
    return api_request('post', 'customers', dict(id=customer_id, name=name))


def find_customer_by_id(customer_id: str):
    """Find customer by given id, only if user is linked to them

    Args:
        customer_id (str): customer id

    Returns:
        dict: customer data
    """
    return api_request('get', f'customers/{customer_id}')


def create_user(email: str, password: str):
    """Create a user with the given credentials

    Args:
        email (str): new user email
        password (str): new user password

    Returns:
        dict: user data
    """
    return api_request(
        'post',
        f'users',
        dict(email=email, password=password)
    )


def delete_user_by_id(user_id: str):
    """Delete a user by id, if customer credentials are used
    then your user will be deleted. if root credentials are used
    you can delete given user_id.

    Args:
        user_id (str): user id to delete

    Returns:
        dict: deleted user
    """
    return api_request('delete', f'users/{user_id}')


def find_users():
    """find users of linked company

    Returns:
        List[dict]: list of users
    """
    return api_request('get', f'users')


def adopt_device_by_serial_number(serial_number: str):
    """Adopt devices by the given serial number, if the current user
    doesn't have a linked company, the user won't be able to send commands 
    to those devices until the user gets a company linked.

    Args:
        serial_number (str): cooler serial number

    Returns:
        dict: cooler data
    """
    return api_request(
        'put',
        f'devices',
        dict(serial_number=serial_number)
    )


def delete_device_by_id(device_id: str):
    """detach user from cooler by device_id

    Args:
        device_id (str): device id with format "cir-wifi-dev-{mac}"

    Returns:
        dict: detached device
    """
    return api_request('delete', f'devices/{device_id}')


def find_device_by_id( device_id: str):
    """find device by the given device id

    Args:
        device_id (str): device id with format "cir-wifi-dev-{mac}"

    Returns:
        dict: device data
    """
    return api_request('get', f'devices/{device_id}')


def get_devices(
        page_size: Optional[int]=None, 
        page_number: Optional[int]=None):
    """Get all adopted devices, if user has already a company, then 
    will be displayed all devices from that company, if user don't 
    have a company then just return their adopted devices.

    Args:
        page_size (Optional, int): Page size of the data, defaults to 100.
        page_number (Optional, int): Page number of the data, defaults to 1.
    
    Returns:
        List[dict]: List of devices

    """
    
    if page_size and page_number:
        query = urlencode({"page_size": page_size, "page_number": page_number})
        path = f'devices?{query}'
    else:
        path = f'devices'
    return api_request('get', path)


def send_command_by_device_id( device_id: str, name: str, package: str):
    """Sends a command to the given device with a name and package data

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}"
        name (str): Command name identifier(like Open door)
        package (str): Package to be sent 

    Returns:
        dict: Response command data
    """
    return api_request(
        'post',
        f'devices/{device_id}/commands',
        dict(name=name, package=package, device_id=device_id)
    )


def link_user_with_customer(customer_id:str, user_id: int):
    """Root only. Links user with customer to allow access to commands

    Args:
        customer_id (str): customer id
        user_id (int): user id

    Returns:
        dict: user data
    """
    return api_request(
        'put',
        f'customers/{customer_id}/users/{user_id}'
    )


def find_commands_by_device_id(
        device_id: str,
        page_size: Optional[int]=None, 
        page_number: Optional[int]=None):
    """find all commands sent by this user to the given device

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}"
        page_size (Optional, int): Page size of the data, defaults to 100.
        page_number (Optional, int): Page number of the data, defaults to 1.

    Returns:
        List[dict]: list of commands
    """
    
    if page_size and page_number:
        query = urlencode({"page_size": page_size, "page_number": page_number})
        path = f'devices/{device_id}/commands?{query}'
    else:
        path = f'devices/{device_id}/commands'
    return api_request('get', path)


def update_user_password(old_password, new_password):
    """Update current user password to a new one

    Args:
        old_password (str): user old password
        new_password (str): user new password

    Returns:
        dict: user data
    """
    return api_request(
        'put',
        f'users/password',
        dict(old_password=old_password, new_password=new_password)
    )


def get_door_status_by_device(device_id: str):
    """Get current door opening status

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}"

    Returns:
        dict: Status of door, if data is 0 is closed, otherwise is open
    """
    return api_request('get', f'devices/{device_id}/door')


def get_lock_status_by_device(device_id: str):
    """Get current Lock status by device (currently just work if it wasn't a bluetooth command)

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}"

    Returns:
        dict: Status of Lock, door:locked for locked and door: unlocked in data field.
    """
    return api_request('get', f'devices/{device_id}/lock')


def subscribe_webhook(callback: str, auth_required: bool = False, auth_value: str = ""):
    """Subscribe to webhook to receive event changes by device

    Args:
        callback (str): url of the webhook
        auth_required (bool, optional): not implemented. Defaults to False.
        auth_value (str, optional): not implemented. Defaults to "".

    Returns:
        dict: callback data
    """
    return api_request(
        'post',
        f'devices/events/suscribe',
        dict(callback=callback, auth_required=auth_required, auth_value=auth_value)
    )

def unsubscribe_webhook():
    """Unsubscribe the webhook, this process is required if events are no longer needed

    Returns:
        dict: callback data
    """
    return api_request(
        'delete',
        f'devices/events/unsuscribe'
    )


def get_event_data(
        device_id: str, 
        variable_id: str, 
        start_at: str, 
        interval: int=100):
    """Fetch data from start date until interval count, max 1000
    records per request

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}"
        variable_id (str): The data variable to extract like "v24"
        start_at (str): Start at date in ISO  ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]
        interval (int, optional): Number of records to retrieve. Defaults to 100.

    Returns:
        List[dict]: List of event records.
    """
    return api_request(
        'post',
        f'devices/{device_id}/events/data',
        {
            "variable_id": variable_id,
            "start_at": start_at,
            "interval": interval
        }
    )


def get_measures_data(
        device_id: str, 
        variable_id: str, 
        start_at: str, 
        interval: int=100):
    """Fetch data of measures in intervals of 30 minutes, max 1000
    records per request

    Args:
        device_id (str): Device id with format "cir-wifi-dev-{mac}" 
        variable_id (str): Variable of the measure, like "32"
        start_at (str): Start at date in ISO  ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]
        interval (int, optional): Number of records to retrieve. Defaults to 100.

    Returns:
        List[dict]: List of measure records
    """
    return api_request(
        'post',
        f'devices/{device_id}/measures/data',
        {
            "variable_id": variable_id,
            "start_at": start_at,
            "interval": interval
        }
    )

def adopt_by_device_list(serial_numbers : List[str]):
    """Adopts a list of devices

    Args:
        serial_numbers (List[str]): List of serial numbers

    Returns:
        dict: Structure with two List, one of adopted devices and other of errors
    """
    return api_request(
        'put',
        f'devices/list',
        {
            "serie": serial_numbers
        }
    )