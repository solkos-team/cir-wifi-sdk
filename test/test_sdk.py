from sdk import (
    adopt_by_device_list,
    create_user,
    delete_device_by_id,
    find_users,
    adopt_device_by_serial_number,
    find_device_by_id,
    get_devices,
    get_event_data,
    get_measures_data,
    send_command_by_device_id,
    find_commands_by_device_id,
    set_access_token,
    login,
    update_user_password,
    get_door_status_by_device,
    get_lock_status_by_device,
    subscribe_webhook,
    unsubscribe_webhook
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


def test_get_door_status():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    status, _ = get_door_status_by_device(device_id)

    print(status)
    assert status is not None


def test_get_lock_status():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    status, _ = get_lock_status_by_device(device_id)

    print(status)
    assert status is not None


def test_subscribe_and_unsubscribe_webhook():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    # This could be your url or exposed service.
    callback, _ = subscribe_webhook("https://cir-wifi-interface-b7agk5thba-uc.a.run.app/devices/events/suscribe/test")

    print(callback)
    # Ready to receive events
    assert callback

    callback, _ = unsubscribe_webhook()

    # Events will no longer received
    assert callback


def test_subscribe_and_unsubscribe_webhook_with_auth():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    # Unsubscribe if a callback exists
    callback, _ = unsubscribe_webhook()

    # This could be your url or exposed service.
    callback, _ = subscribe_webhook(
        "https://cir-wifi-interface-b7agk5thba-uc.a.run.app/devices/events/suscribe/test"
        ,True,
        '0123456789'
        )

    print(callback)
    # Ready to receive events
    assert callback

    callback, _ = unsubscribe_webhook()

    # Events will no longer received
    assert callback


def test_get_data_measures():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    result, _ = get_event_data(device_id, 'v24', '2021-07-10T10:33:19.196Z')

    print(result)
    assert result == []


def test_get_data_events():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    result, _ = get_measures_data(device_id, '32', '2021-07-10T10:33:19.196Z')

    print(result)
    assert result == []
    

def test_adoption_by_list_and_detach():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    for device in devices:
        delete_device_by_id(device["id"])

    devices, error = adopt_by_device_list(['000000789210300053', '000000789210300054'])

    print(error)
    assert devices["results"]

    devices, _ = get_devices()

    for device in devices:
        delete_device_by_id(device["id"])



def test_devices_pagination():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices(10, 1)

    assert devices is not None
    
    devices, _ = get_devices(10, 20)

    assert not devices


def test_commands_pagination():
    set_access_token(USER_EMAIL, USER_PASSWORD)

    devices, _ = get_devices()

    assert devices is not None
    
    device_id = devices[0]["id"]

    commands, _ = find_commands_by_device_id(device_id, 10, 1)

    assert commands is not None

    commands, _ = find_commands_by_device_id(device_id, 100, 20)

    assert not commands