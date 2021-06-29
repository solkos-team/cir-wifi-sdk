# CIR Wifi SDK v1.0
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

### **find_customer_by_id**
    Find customer by given id, only if user is linked to them

params
- customer_id :str -> customer id

returns
- dict: customer data

<br>

### **find_users**
    find users of linked company

returns
- List[dict]: list of users

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

### **find_device_by_id**
    find device by the given device id

params
- device_id :str -> device id with format "cir-wifi-dev-{mac}"

returns
- dict: device data

<br>

### **get_devices**
    Get all adopted devices, if user has already a company, then 
    will be displayed all devices from that company, if user don't 
    have a company then just return their adopted devices.

returns
- List[dict]: List of devices

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

returns
- dict: list of commands

<br>

### **update_user_password**
    Update current user password to a new one

params
- old_password :str -> user old password
- new_password :str -> user new password

returns
- dict: user data

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
