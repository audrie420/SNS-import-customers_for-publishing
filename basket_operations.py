import cust_API_requests as car
import old_ticket_API_requests as tar
from pprint import pprint as pp

# you get the customer ID and the AV performance code of that instance.
# instance IDs will have to be manually searched up, put in a csv, and entered, prior to running ticket update program
# because instances are not searchable by AVID
# give them a ticket. that's it


def create_fill_confirm_basket(customer_id, instance_id, client_name):
    # from instance ID, find first ticketID with 0 price
    res = tar.instance_price_list(instance_id, client_name)
    tickettype_id = ""
    for price in res.json()["prices"]:
        if price["amount"] == 0.0:
            tickettype_id = price["ticketType"]["id"]
            break

    # from instance ID, find seating plan and whether its reserved or unreserved. build ticketsbody
    ticketsbody = [{"instance": instance_id, "type": tickettype_id}]
    res = tar.lookup_instance_id(instance_id, client_name)
    seatplan_id = res.json()["planId"]
    res = tar.lookup_seating_plan_id(seatplan_id, client_name)
    seatplan_type = res.json()["type"]
    if seatplan_type == "Reserved":
        res = tar.get_seat_ids(instance_id, client_name, 1)
        seat_id = res.json()[0]["id"]
        ticketsbody[0]["seat"] = seat_id
    elif seatplan_type == "Unreserved":
        ticketsbody[0]["seatingPlan"] = seatplan_id

    # create a basket with customer and ticket attached

    body = {
        "customer": customer_id,
        "tickets": ticketsbody,
        "ticketDelivery": {"type": "1"},
    }
    res = tar.make_new_basket(body, client_name)

    # confirm basket
    basket_id = res.json()["id"]
    confirm_basket_body = {"sendConfirmationEmail": False, "paymentChannel": "Web"}
    res = tar.confirm_basket(confirm_basket_body, basket_id, client_name)

    return res


if __name__ == "__main__":
    print("running test on module ticket_API_requests :3")

    # redacted for confidentiality
