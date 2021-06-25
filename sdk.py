import requests
import os
from dotenv import load_dotenv

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
    token, _ = login(email, password)

    if token:
        global access_token
        access_token = token


def login(email: str, password: str):
    return api_request('post', 'login', dict(email=email, password=password), False)


def create_customer(customer_id: str, name: str):
    return api_request('post', 'customers', dict(id=customer_id, name=name))


def find_customer_by_id(customer_id: str):
    return api_request('get', f'customers/{customer_id}')


def create_user(email: str, password: str):
    return api_request(
        'post',
        f'users',
        dict(email=email, password=password)
    )


def delete_user_by_id(user_id: str):
    return api_request('delete', f'users/{user_id}')


def find_users():
    return api_request('get', f'users')


def adopt_device_by_serial_number(serial_number: str):
    return api_request(
        'put',
        f'devices',
        dict(serial_number=serial_number)
    )


def delete_device_by_id(device_id: str):
    return api_request('delete', f'devices/{device_id}')


def find_device_by_id( device_id: str):
    return api_request('get', f'devices/{device_id}')


def get_devices():
    return api_request('get', f'devices')


def send_command_by_device_id( device_id, name: str, package: str):
    return api_request(
        'post',
        f'devices/{device_id}/commands',
        dict(name=name, package=package, device_id=device_id)
    )

def link_user_with_customer(customer_id:str, user_id: int):
    return api_request(
        'put',
        f'customers/{customer_id}/users/{user_id}'
    )


def find_commands_by_device_id(device_id):
    return api_request(
        'get',
        f'devices/{device_id}/commands',
    )


def update_user_password(old_password, new_password):
    return api_request(
        'put',
        f'users/password',
        dict(old_password=old_password, new_password=new_password)
    )
