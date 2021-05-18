from sdk import (
    create_user_by_customer_id,
    find_users_by_customer_id,
    adopt_device_by_customer_id,
    find_device_by_id,
    find_devices_by_customer_id,
    create_command_by_device_id,
    find_commands_by_device_id,
    set_access_token,
    login
)
import uuid


CUSTOMER_ID = 'super_food'
USER_EMAIL = 'user@superfood.com'
USER_PASSWORD = '123abc'


def test_login():
    token, _ = login(USER_EMAIL, USER_PASSWORD)

    assert token is not None

    print(token)


def test_create_user_by_customer_id():
    user_id = str(uuid.uuid4()).replace('-', '_')
    set_access_token(USER_EMAIL, USER_PASSWORD)
    new_email = f'{user_id}@superfood.com'
    user, _ = create_user_by_customer_id(email=new_email, password=USER_PASSWORD, customer_id=CUSTOMER_ID)

    assert user is not None
    assert user['email'] == new_email

    print(user)


def test_find_users_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    users, _ = find_users_by_customer_id(customer_id)

    assert users is not None
    assert len(users)

    for user in users:
        print(user)


def test_adopt_device_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    device_id = 'cir-wifi-dev-b4a2eb41eb4b'
    device, _ = adopt_device_by_customer_id(device_id=device_id, customer_id=customer_id)

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
    device_id = f'cir-wifi-dev-b4a2eb41eb4b'

    command, _ = create_command_by_device_id(
        customer_id,
        device_id,
        name='Estado de Cerradura',
        package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b1'
    )

    assert command is not None
    assert command['code'] == 200
    assert command['sent']
    assert command['message'] == 'Command sent'

    print(command)


def test_find_commands_by_device_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    customer_id = CUSTOMER_ID
    device_id = f'cir-wifi-dev-b4a2eb41eb4b'

    commands, _ = find_commands_by_device_id(customer_id, device_id)

    assert commands is not None
    assert len(commands) > 0
