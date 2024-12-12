from datetime import datetime
import json
import os

current_dt = datetime.now().strftime("%Y%m%d.%H%M")
log_folder = "API_logs_folder"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
log_filename = os.path.join(log_folder, f"API_logs_{current_dt}.txt")

with open(log_filename, "w") as file:
    file.write(f"Starting log file for import done at {current_dt}")
print(
    f"Started log file for API actions performed for this import. File name is {log_filename}"
)


def log_entry(
    client_name,
    call,
    url,
    status_code,
    function_name,
    body=None,
    cust_id=None,
    address_or_contpref_id=None,
):
    file = open(log_filename, "a")
    if not (status_code >= 200 and status_code <= 299):
        file.write("\nCALL FAILURE")
    log = (
        str(status_code)
        + " "
        + call
        + " "
        + client_name
        + "\n"
        + url
        + "\n"
        + function_name
    )
    file.write("\n" + log)
    if cust_id:
        file.write("\n" + cust_id)
    if address_or_contpref_id:
        file.write("\n" + address_or_contpref_id)
    if body:
        json_str = json.dumps(body)
        file.write("\n" + json_str)
    file.write("\n")
    file.close()


if __name__ == "__main__":
    print("running test on module API_log_entry :3")
    # redacted for confidentiality
