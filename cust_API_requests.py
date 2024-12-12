# group 1 - API interaction handlers
# contains hardcoded sensitive info

import header_gen
import requests
from pprint import pprint as pp
import API_log_entry as ale


def __find_login_name(client_name: str):
    # redacted for confidentiality
    return ""


def __is_test(client_name: str):
    # redacted for confidentiality
    return True


# cannot make new cust without email
# email undergoes validation check, must be (thing)@(thing).(thing)
def make_new_cust(body: dict, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers"
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
        function_name="make_new_cust",
        body=body,
    )
    response.close()
    return response


def lookup_cust_email(cust_email: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = (
        f"https://system.spektrix.com/{client_name}/api/v3/customers?email={cust_email}"
    )
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response  # dict type


def lookup_cust_id(cust_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


def lookup_cust_order_hist(cust_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/orders"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response  # dict type


def expanded_lookup_cust_id(cust_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}?$expand=1"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# this function works to overwrite the following fields
# firstname lastname phone mobile email "AVID" "Alternate Email" "Duplicate Email" "Invalid Email"
def overwrite_fields(
    body: dict, cust_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}"
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
        "overwrite_fields",
        body=body,
        cust_id=cust_id,
    )
    response.close()
    return response


# consider manipulating json to show only the cont prefs
def lookup_cont_pref(cust_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}?$expand=AllStatements"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# works even if cont pref already on
def turn_on_printmail_cont_pref(
    cust_id: str, client_name: str
) -> requests.models.Response:
    body = [{"id": "401ANPJQJQPQMRSBDNMVNLSPGTRBVQVRH"}]
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/agreed-statements"
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
        function_name="turn_on_printmail_cont_pref",
        body=body,
        cust_id=cust_id,
    )
    response.close()
    return response


def turn_on_email_cont_pref(cust_id: str, client_name: str) -> requests.models.Response:
    body = [{"id": "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL"}]
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/agreed-statements"
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
        function_name="turn_on_email_cont_pref",
        body=body,
        cust_id=cust_id,
    )
    response.close()
    return response


# works even if cont pref already off
# junk body {"lol": "lel"} required to make API authentication work
def turn_off_printmail_cont_pref(
    cust_id: str, client_name: str
) -> requests.models.Response:
    body = {"lol": "lel"}
    cont_pref_id = "401ANPJQJQPQMRSBDNMVNLSPGTRBVQVRH"
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/agreed-statements/{cont_pref_id}"
    call = "DELETE"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.delete(url=url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="turn_off_printmail_cont_pref",
        cust_id=cust_id,
        address_or_contpref_id=cont_pref_id,
    )
    response.close()
    return response


def turn_off_email_cont_pref(
    cust_id: str, client_name: str
) -> requests.models.Response:
    cont_pref_id = "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL"
    body = {"lol": "lel"}
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/agreed-statements/{cont_pref_id}"
    call = "DELETE"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.delete(url=url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="turn_off_email_cont_pref",
        cust_id=cust_id,
        address_or_contpref_id=cont_pref_id,
    )
    response.close()
    return response


def lookup_cust_addresses(cust_id: str, client_name: str) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/addresses"
    headers = header_gen.build_headers(
        "GET", login_name, url, None, __is_test(client_name)
    )
    response = requests.get(url, headers=headers)
    response.close()
    return response


# if cust record has no addresses yet and you're adding the first one,
# even if you set the billing and delivery as False, it will default to True
# if cust record has other address set to billing or delivery, new addition of address wont change anything
def add_new_address(
    body: dict, cust_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/addresses"
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
        function_name="add_new_address",
        cust_id=cust_id,
    )
    response.close()
    return response


# junk body {"lol": "lel"} required to make API authentication work
def delete_address(
    address_id: str, cust_id: str, client_name: str
) -> requests.models.Response:
    body = {"lol": "lel"}
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/addresses/{address_id}"
    call = "DELETE"
    headers = header_gen.build_headers(
        call, login_name, url, body, __is_test(client_name)
    )
    response = requests.delete(url=url, headers=headers, json=body)
    ale.log_entry(
        client_name,
        call,
        url,
        response.status_code,
        function_name="delete_address",
        cust_id=cust_id,
        address_or_contpref_id=address_id,
    )
    response.close()
    return response


# cannot change country or state/province, must make new address
# cannot change billing/delivery status
def edit_address(
    body: dict, address_id: str, cust_id: str, client_name: str
) -> requests.models.Response:
    login_name = __find_login_name(client_name)
    url = f"https://system.spektrix.com/{client_name}/api/v3/customers/{cust_id}/addresses/{address_id}"
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
        function_name="edit_address",
        cust_id=cust_id,
        address_or_contpref_id=address_id,
    )
    response.close()
    return response


if __name__ == "__main__":
    print("running test on module API_requests :3")

    # redacted for confidentiality