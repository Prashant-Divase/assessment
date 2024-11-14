# tests/test_example.py
import json

import pytest
from methods.api_methods import ApiMethods
from utils.helper_functions import check_response,validate_booking_response,generate_random_booking_data,compare_json_ignore_keys,compare_json_should_not_same
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@pytest.fixture
def api(config):
    return ApiMethods(config)

@pytest.mark.sanity
def test_get_all_booking_ids(api):
    response = api.get("/booking")
    log.info(f"Status Code: {response.status_code}")
    assert response.status_code == 200 , "Expected status code 200, got {response.status_code}"
    validate_booking_response(response.json())


@pytest.mark.sanity
def test_create_booking(api):
    # Do not include token for this request
    # Generate random booking data
    global booking_id,booking_response,first_name,lastname,totalprice,depositpaid,checkin,checkout,additionalneeds,data
    data = generate_random_booking_data()
    response = api.post("/booking",data=data)
    booking_id =  response.json()['bookingid']
    #below i am storing the all values of the reponse in single variable to validate the results in next testcases
    booking_response = json.loads(response.text)
    first_name = booking_response['booking']['firstname']
    lastname = booking_response['booking']['lastname']
    totalprice = booking_response['booking']['totalprice']
    depositpaid = booking_response['booking']['depositpaid']
    checkin = booking_response['booking']['bookingdates']['checkin']
    checkout = booking_response['booking']['bookingdates']['checkout']
    additionalneeds = booking_response['booking']['additionalneeds']
    log.info(f"Status Code: {response.status_code}")
    log.info(f"booking_response: {booking_response}")
    log.info(f"booking_id: {booking_id}")
    log.info(f"first_name: {first_name}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

@pytest.mark.sanity
def test_validate_created_booking_able_to_fetch_with_get_call(api):
    global booking_id,booking_response
    response = api.get(f"/booking/{booking_id}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"


@pytest.mark.sanity
def test_validate_get_id_response_of_the_booking(api):
    global booking_id,booking_response
    response = api.get(f"/booking/{booking_id}")
    booking_id_response =  response.json()
    log.info(f"actual_response: {booking_id_response}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    keys_to_ignore = ['bookingid']
    compare_json_ignore_keys(booking_response['booking'], booking_id_response, keys_to_ignore)

@pytest.mark.sanity
def test_get_booking_filter_with_first_name_should_return_correct_booking_id(api):
    global booking_id, booking_response,first_name
    response = api.get(f"/booking/?firstname={first_name}")
    filter_first_name_response = response.json()
    log.info(f"actual_response: {filter_first_name_response}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert filter_first_name_response[0]['bookingid'] == 256545


@pytest.mark.sanity
def test_get_booking_filter_with_lastname_name_should_return_correct_booking_id(api):
    global booking_id, booking_response,lastname
    response = api.get(f"/booking/?lastname={lastname}")
    filter_last_name_response = response.json()
    log.info(f"actual_response: {filter_last_name_response}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert filter_last_name_response[0]['bookingid'] == booking_id


@pytest.mark.sanity
def test_get_booking_filter_with_first_name_last_nameid(api):
    global booking_id, booking_response,lastname,first_name
    response = api.get(f"/booking/?firstname={first_name}&lastname={lastname}")
    filter_first_last_name_response = response.json()
    log.info(f"actual_response: {filter_first_last_name_response}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert filter_first_last_name_response[0]['bookingid'] == booking_id

@pytest.mark.sanity
def test_update_booking(api,config):
    global booking_id, booking_response,lastname,first_name
    data= generate_random_booking_data()
    token = config.get("token")
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie' : f"token={token}"
        }
    response = api.put(f"/booking/{booking_id}",data=data,custom_headers=headers)
    update_response = response.json()
    log.info(f"updated response is : {update_response}")
    log.info(f"Original response is : {update_response}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

@pytest.mark.sanity
def test_delete_booking(api,config):
    global booking_id, booking_response,lastname,first_name
    token = config.get("token")
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie' : f"token={token}"
        }
    response = api.delete(f"/booking/{booking_id}",custom_headers=headers)
    update_response = response.text
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    assert response.text == 'Created'

@pytest.mark.sanity
def test_booking_id_after_deleting_booking_id(api):
    global booking_id
    response = api.get(f"/booking/{booking_id}")
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
    assert response.text == "Not Found"


