from sdk import (
    create_user,
    find_users,
    adopt_device_by_serial_number,
    find_device_by_id,
    get_devices,
    send_command_by_device_id,
    find_commands_by_device_id,
    set_access_token,
    login,
    update_user_password
)
import uuid
import os


CUSTOMER_ID = os.getenv('CUSTOMER_ID')
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')


def test_login():
    token, _ = login(USER_EMAIL, USER_PASSWORD)

    assert token is not None

    print(token)


def test_create_user():
    user_id = str(uuid.uuid4()).replace('-', '_')
    set_access_token(USER_EMAIL, USER_PASSWORD)
    new_email = f'{user_id}@{CUSTOMER_ID.replace(" ", "")}.com'
    user, _ = create_user(email=new_email, password=USER_PASSWORD)

    assert user is not None
    assert user['email'] == new_email

    print(user)


def test_find_users_by_customer_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    users, _ = find_users()

    assert users is not None
    assert len(users)

    for user in users:
        print(user)


def test_update_user_password():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    
    old_password = USER_PASSWORD
    new_password = '123abc'
    result = update_user_password(old_password, new_password)

    assert result

    result = update_user_password(new_password, old_password)

    assert result


def test_adopt_device_by_serial_number():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    serial_number = '000000789210300053'
    device, _ = adopt_device_by_serial_number(serial_number=serial_number)

    assert device is not None

    print(device)

    device, _ = find_device_by_id( device["id"])

    assert device is not None

    print(device)


def test_find_devices():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    devices, _ = get_devices()

    assert devices is not None
    assert len(devices)

    for device in devices:
        print(device)


def test_create_command_by_device_id():
    set_access_token(USER_EMAIL, USER_PASSWORD)
    
    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    command, _ = send_command_by_device_id(
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
    
    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    commands, _ = find_commands_by_device_id(device_id)

    assert commands is not None
    assert len(commands) > 0
