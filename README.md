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

## Command list that the device supports
1. Lock:
```python
command, error = send_command_by_device_id(
    customer_id,
    device_id,
    name='Lock',
    package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b0'
)
```
2. Unlock:
```python
command, error = send_command_by_device_id(
    customer_id,
    device_id,
    name='Unlock',
    package='a013a17efe9e7a3f69ec4a4a53b749cd7a60b1'
)
```
