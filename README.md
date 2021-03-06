# CIR Wifi SDK v1.0

## Menu
1. [Steps to run tests](#steps-to-run-tests)
2. [Sdk functions](#sdk-functions)
    1. Authorization
        1. [set_access_token](#set_access_token)
        2. [login](#login)
    2. Customers
        1. [find_customer_by_id](#find_customer_by_id)
    3. Users
        1. [find_users](#find_users)
        2. [update_user_password](#update_user_password)
    4. Devices
        1. [adopt_device_by_serial_number](#adopt_device_by_serial_number)
        2. [delete_device_by_id](#delete_device_by_id)
        3. [adopt_by_device_list](#adopt_by_device_list)
        4. [find_device_by_id](#find_device_by_id)
        5. [get_devices](#get_devices)
        6. [get_door_status_by_device](#get_door_status_by_device)
        7. [get_lock_status_by_device](#get_lock_status_by_device)
    5. Commands
        1. [send_command_by_device_id](#send_command_by_device_id)
        2. [find_commands_by_device_id](#find_commands_by_device_id)
    6. Webhook
        1. [subscribe_webhook](#subscribe_webhook)
        2. [unsubscribe_webhook](#unsubscribe_webhook)
    7. Data
        1. [get_catalog_of_variables](#get_catalog_of_variables)
        2. [get_event_data](#get_event_data)
        3. [get_measures_data](#get_measures_data)
    
3. [Command list](#Command-list-that-the-device-supports)

## Steps to run tests
1. Requesting Imbera team to create customer/user/password credentials
2. Create virtual env: https://docs.python.org/3/library/venv.html
3. Install dependencies: pip install -r /path/to/requirements.txt
4. Create an .env file on root directory similar to:
```
CUSTOMER_ID=food_service
USER_EMAIL=user@foodservice.com
USER_PASSWORD=*****
```
5. Run test cases on test/test_sdk.py

## Sdk Functions

Api call schema sample: `response, error = function(params)`.  
The error will be empty if there is no problem in the request(look at test/test_sdk.py to get a better idea about the schema).

<br>

### Authorization

<br>

### **set_access_token**
    Set the access token for given credentials to allow use of sdk functions

params
- email: str -> user email
- password: str -> user password

returns
- None

<br>

### **login**
    Login with user credentials and returns the access token

params
- email: str -> user email
- password: str -> user password

returns
- str: access token 


<br>

### Customers

<br>

### **find_customer_by_id**
    Find customer by given id, only if user is linked to them

params
- customer_id :str -> customer id

returns
- dict: customer data

<br>

### Users

### **find_users**
    find users of linked company

returns
- List[dict]: list of users

<br>

### **update_user_password**
    Update current user password to a new one

params
- old_password :str -> user old password
- new_password :str -> user new password

returns
- dict: user data

<br>

### Devices

<br>

### **adopt_device_by_serial_number**
    Adopt devices by the given serial number, if the current user doesn't have a linked company, the user won't be able to send commands to those devices until the user gets a company linked.

params
- serial_number :str -> cooler serial number

returns
- dict: cooler data

<br>

### **delete_device_by_id**
    detach user from cooler by device_id

params
- device_id :str -> device id with format "cir-wifi-dev-{mac}"

returns
- dict: detached device

<br>

### **adopt_by_device_list**
    Adopts a list of devices

params
- serial_numbers :List\[str] -> List of serial numbers

returns.
- dict: Structure with two List, one of adopted devices and other of errors.

<br>

### **find_device_by_id**
    find device by the given device id

params
- device_id :str -> device id with format "cir-wifi-dev-{mac}"

returns
- dict: device data

<br>

### **get_devices**
    Get all adopted devices, if user has already a company, 
    then will be displayed all devices from that company, 
    if user don't have a company then just return their adopted devices.

params:
- page_size Optional int -> Page size of the data, defaults to 100.
- page_number Optional, int -> Page number of the data, defaults to 1.

returns
- List\[dict]: List of devices

<br>

### **get_door_status_by_device**
    Get current door opening status

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"

returns
- dict: Status of door, if data is 0 is closed, otherwise is open

<br>

### **get_lock_status_by_device**
    Get current Lock status by device (currently just work if it wasn't a bluetooth command)

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"

returns
- dict: Status of Lock, door:locked for locked and door: unlocked in data field.

<br>

### Commands

<br>

### **send_command_by_device_id**
    find device by the given device id

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"
- name :str -> Command name identifier (like "Open door")
- package :str -> Package to be sent 

returns
- dict: Response command data

<br>

### **find_commands_by_device_id**
    find all commands sent by this user to the given device

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"
- page_size :Optional int -> Page size of the data, defaults to 100.
- page_number :Optional, int -> Page number of the data, defaults to 1.

returns
- dict: list of commands

<br>

### Webhook

<br>

### **subscribe_webhook**
    Subscribe to the webhook to receive event changes by the 
    device.
    If Auth is active, this will make a request with 
    Authorization header with the format 'Bearer {auth_value}', 
    example: 'Bearer 12345'.

    This will send a request to the webhook every time that a 
    device detects a change in their values.

    The request will have a body with the following.
    {
        "device_id": "str",
        "event_type": "str",
        "event_data": "str",
        "event_date": "datetime"
    }
    Currently just is possible to subscribe one webhook by customer.

params
- callback: str -> url of the webhook
- auth_required: bool, optional -> Set to false (work in progress).
- auth_value: str, optional -> Set to "" (work in progress).

returns
- dict: callback data.

<br>

### **unsubscribe_webhook**
    Unsuscribe the webhook, this process is required if events are no longer needed
returns
- dict : callback data

<br>

### Data

<br>

### **get_catalog_of_variables**
    Fetch the catalog of variables.

returns
- List\[dict]: List of variables.

<br>

### **get_event_data**
    Fetch data from start date until interval count, max 1000
    records per request.

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"
- variable_id :str -> The data variable to extract like "v24"
- start_at :str -> Start at date in ISO 8601 format, YYYY-MM-DDTHH:MM:SS\[.mmmmmm]\[+HH:MM]
- interval : Optional int -> Number of records to retrieve. Defaults to 100.

returns
- List\[dict]: List of event records.

<br>

### **get_measures_data**
    Fetch data of measures in intervals of 30 minutes, max 1000
    records per request

params
- device_id :str -> Device id with format "cir-wifi-dev-{mac}"
- variable_id :str -> Variable of the measure, like "32"
- start_at :str -> Start at date in ISO 8601 format, YYYY-MM-DDTHH:MM:SS\[.mmmmmm]\[+HH:MM]
- interval : Optional int -> Number of records to retrieve. Defaults to 100.

returns
- List\[dict]: List of measure records.

<br>

## Command list that the device supports
1. Lock:
```python
command, error = send_command_by_device_id(
    device_id,
    name='Lock',
    package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b0'
)
```
2. Unlock:
```python
command, error = send_command_by_device_id(
    device_id,
    name='Unlock',
    package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b1'
)
```
