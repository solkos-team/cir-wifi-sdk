from sdk import (
    create_customer,
    find_customer_by_id,
    create_user_by_customer_id,
    delete_user_by_id,
    find_users_by_customer_id,
    create_device_by_customer_id,
    delete_device_by_id,
    find_device_by_id,
    find_devices_by_customer_id,
    create_command_by_device_id,
    set_access_token,
    login
)
import uuid
from dotenv import load_dotenv
import os

load_dotenv('../.env')

ROOT_EMAIL = os.getenv('ROOT_EMAIL')
ROOT_PASSWORD = os.getenv('ROOT_PASSWORD')
CUSTOMER_ID = 'test'
CUSTOMER_NAME = 'Test'
USER_EMAIL = 'user@test.com'
USER_PASSWORD = '12abc'


def test_create_test_customer():
    set_access_token(ROOT_EMAIL, ROOT_PASSWORD)
    customer, _ = create_customer(customer_id=CUSTOMER_ID, name=CUSTOMER_NAME)

    assert customer is not None

    print(customer)


def test_create_customer():
    set_access_token(ROOT_EMAIL, ROOT_PASSWORD)
    customer, _ = create_customer(customer_id=str(uuid.uuid4()), name=str(uuid.uuid4()))

    assert customer is not None

    print(customer)


def test_find_customer_by_id():
    set_access_token(ROOT_EMAIL, ROOT_PASSWORD)
    customer_id = CUSTOMER_ID
    customer, _ = find_customer_by_id(customer_id=customer_id)

    assert customer is not None

    print(customer)


def test_create_user_by_customer_id():
    set_access_token(ROOT_EMAIL, ROOT_PASSWORD)
    user, _ = create_user_by_customer_id(email=USER_EMAIL, password=USER_PASSWORD, customer_id=CUSTOMER_ID)

    assert user is not None

    print(user)


def test_delete_user_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    email = f'{str(uuid.uuid4())}@{customer_id}.com'
    password = USER_PASSWORD
    user, _ = create_user_by_customer_id(email=email, password=password, customer_id=CUSTOMER_ID)

    assert user is not None

    user, _ = delete_user_by_id(user['id'], customer_id)

    assert user is not None

    print(user)


def test_login():
    token, _ = login(USER_EMAIL, USER_PASSWORD)

    assert token is not None

    print(token)


def test_find_users_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    users, _ = find_users_by_customer_id(customer_id)

    assert users is not None
    assert len(users)

    for user in users:
        print(user)


def test_create_device_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    device_id = f'test-cir-wifi-{customer_id}-{str(uuid.uuid4())}'
    device, _ = create_device_by_customer_id(
        device_id=device_id,
        public_key_format='RSA_PEM',
        customer_id=customer_id
    )

    assert device is not None

    print(device)

    device, _ = find_device_by_id(customer_id, device_id)

    assert device is not None

    print(device)


def test_find_devices_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    devices, _ = find_devices_by_customer_id(customer_id)

    assert devices is not None
    assert len(devices)

    for device in devices:
        print(device)


def test_create_command_by_device_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    device_id = f'test-cir-wifi-{customer_id}-{str(uuid.uuid4())}'
    device, _ = create_device_by_customer_id(
        device_id=device_id,
        public_key_format='RSA_PEM',
        customer_id=customer_id
    )

    assert device

    command, _ = create_command_by_device_id(
        customer_id,
        device.id,
        name='Estado de Cerradura',
        package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b1'
    )

    assert command is not None
    assert command['code'] == 400

    device, _ = delete_device_by_id(device_id, customer_id)

    assert device is not None

    _, error = find_device_by_id(customer_id, device_id)

    print(command)


def test_delete_device_by_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    device, _ = create_device_by_customer_id(
        device_id=f'test-cir-wifi-{customer_id}-{str(uuid.uuid4())}',
        public_key_format='RSA_PEM',
        customer_id=customer_id
    )

    assert device is not None

    device_id = device['id']
    device, _ = find_device_by_id(customer_id, device_id)

    assert device is not None

    device, _ = delete_device_by_id(device['id'], customer_id)

    assert device is not None

    _, error = find_device_by_id(customer_id, device_id)

    assert error is not None

    print(device)
