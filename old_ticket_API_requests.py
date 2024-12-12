# group 1 - API interaction handlers
# contains hardcoded sensitive info
# the old version is sufficient for this program. for new version see sns import tickets

import header_gen
import requests
from pprint import pprint as pp
import API_log_entry as ale
import inspect
from datetime import datetime
from urllib.parse import quote


def __find_login_name(client_name: str):
    # redacted for confidentiality
    pass


def __is_test(client_name: str):
    # redacted for confidentiality
    pass


# makes a new basket
# POST call returns basket details
def make_new_basket(body: dict, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/baskets"
    call = "POST"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.post(url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="make_new_basket",
        body=body,
    )
    response.close()
    return response


# To add additional information to a basket, such as redacted
# PATCH call returns basket details
def add_info_to_basket(
    body: dict, basket_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}"
    call = "PATCH"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.patch(url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="add_info_to_basket",
        body=body,
    )
    response.close()
    return response


# Confirms an order. For system-owners, this can only be used for zero-value orders.
# what does it return? read documentation
def confirm_basket(
    body: dict, basket_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}/confirm"
    )
    call = "POST"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.post(url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="confirm_basket",
        body=body,
    )
    response.close()
    return response


def add_ticket_to_basket(
    body: dict, basket_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}/tickets"
    )
    call = "POST"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.post(url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="add_ticket_to_basket",
        body=body,
    )
    response.close()
    return response


# POST call returns basket details
# junk body {"lol": "lel"} required to make API authentication work
def clear_items_in_basket(basket_id: str, client_name: str) -> requests.models.Response:
    body = {"lol": "lel"}
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}/clear"
    call = "POST"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.post(url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="clear_items_in_basket",
        body=body,
    )
    response.close()
    return response


def get_all_live_events(client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/events/"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def instance_price_list(instance_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/instances/{instance_id}/price-list"
    headers = header_gen.build_headers(
        "GET", login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_event_id(event_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/events/{event_id}"
    headers = header_gen.build_headers(
        "GET", login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_instance_id(instance_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/instances/{instance_id}"
    headers = header_gen.build_headers(
        "GET", login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_event_search(
    event_onSale: bool,
    name_search: str,
    client_name: str,
    from_year: int = 2022,
    from_month: int = 1,
    from_day: int = 1,
    to_year: int = 9999,
    to_month: int = 12,
    to_day: int = 31,
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    instanceStart_from = datetime(from_year, from_month, from_day).strftime("%Y-%m-%d")
    instanceStart_to = datetime(to_year, to_month, to_day).strftime("%Y-%m-%d")
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/events?"
        f"instanceStart_from={instanceStart_from}&"
        f"instanceStart_to={instanceStart_to}&"
        f"instanceInterface=All&"
        f"onSale={event_onSale}&"
        f"name={quote(name_search)}"
    )
    call = "GET"
    headers = header_gen.build_headers(
        call, login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# res.json()["id"] for instance id
# doesnt show AV performance code. field name should be "attribute_AV Performance Code"
def return_instances_for_event(
    event_id: str,
    client_name: str,
    from_year: int = 2022,
    from_month: int = 1,
    from_day: int = 1,
    to_year: int = 9999,
    to_month: int = 12,
    to_day: int = 31,
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    start_from = datetime(from_year, from_month, from_day).strftime("%Y-%m-%d")
    start_to = datetime(to_year, to_month, to_day).strftime("%Y-%m-%d")
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/events/{event_id}/"
        f"instances?start_from={start_from}&"
        f"start_to={start_to}&"
        f"interface=All"
    )
    call = "GET"
    headers = header_gen.build_headers(
        call, login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# baskets have non-out-of-box attributes too, it seems. might have to go turn those on
def check_basket_details(basket_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def check_tickets_in_basket(
    basket_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/baskets/{basket_id}/tickets"
    )
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# GET v3/instances/{id}/best-available?quantity={quantity}
# Returns the current best available seats for an instance for the number specified
def get_seat_ids(
    instance_id: str, client_name: str, quantity: int = 1
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/instances/{instance_id}/best-available?quantity={quantity}"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_all_seating_plans(client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/plans"
    headers = header_gen.build_headers(
        "GET", login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_seating_plan_id(
    seatplan_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/plans/{seatplan_id}"
    headers = header_gen.build_headers(
        "GET", login_name, url, body=None, test=__is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


if __name__ == "__main__":
    print("running test on module ticket_API_requests :3")

    cust_email_apitesting = "magiclamp@gmail.cactus"
    customer_id_apitesting = "I-F922-HDWC"
    customer_id_sns = "I-GV23-CCKK"
    client_apitesting = "apitesting"
    client_sns = "symphonynovascotia"
    # res = get_all_live_events(client_apitesting)
    # pp(res.status_code)
    # for event in res.json():
    #     if (
    #         event["firstInstanceDateTime"]
    #         and event["firstInstanceDateTime"] != event["lastInstanceDateTime"]
    #         and event["isOnSale"] is True
    #     ):
    #         pp(event["name"])
    #         pp(event["id"])
    #         pp(event["firstInstanceDateTime"])
    #         pp(event["lastInstanceDateTime"])
    #         pp(event["isOnSale"])
    res = lookup_instance_id("72854AQBJRHKRDLQGVJPKBSRGHGQTMMBJ", client_apitesting)
    pp(res.status_code)
    pp(res.json())
