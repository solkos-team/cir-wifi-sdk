import requests

access_token = None
api_url = 'https://cir-wifi-interface-b7agk5thba-uc.a.run.app'


def get_request_method(method: str):
    if method == 'post':
        return requests.post
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


def create_user_by_customer_id(email: str, password: str, customer_id: str):
    return api_request(
        'post',
        f'customers/{customer_id}/users',
        dict(email=email, password=password, customer_id=customer_id)
    )


def delete_user_by_id(user_id: str, customer_id: str):
    return api_request('delete', f'customers/{customer_id}/users/{user_id}')


def find_users_by_customer_id(customer_id):
    return api_request('get', f'customers/{customer_id}/users')


def create_device_by_customer_id(device_id: str, public_key_format: str, customer_id: str):
    return api_request(
        'post',
        f'customers/{customer_id}/devices',
        dict(id=device_id, public_key_format=public_key_format, customer_id=customer_id)
    )


def delete_device_by_id(device_id: str, customer_id: str):
    return api_request('delete', f'customers/{customer_id}/devices/{device_id}')


def find_device_by_id(customer_id: str, device_id: str):
    return api_request('get', f'customers/{customer_id}/devices/{device_id}')


def find_devices_by_customer_id(customer_id):
    return api_request('get', f'customers/{customer_id}/devices')


def create_command_by_device_id(customer_id, device_id, name: str, package: str):
    return api_request(
        'post',
        f'customers/{customer_id}/devices/{device_id}/commands',
        dict(name=name, package=package, device_id=device_id)
    )
