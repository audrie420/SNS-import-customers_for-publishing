# group 1 - API interaction handlers
# contains hardcoded sensitive info

from cryptography.fernet import Fernet


def obtain_real_key():
    response = input("Are you trying to access the redacted API? y/n:")
    if response == "y":
        password = input("Input the password to access redacted API:")
        password = password.encode("utf-8")
        encrypted_api_key = b"lisdjfngjelrh redacted=="
        cipher_suite = Fernet(password)
        decrypted_api_key = cipher_suite.decrypt(encrypted_api_key)
        return decrypted_api_key
    return False


sandbox = b"redacted key"
sns = obtain_real_key()
client_name = "redacted"
if not sns:
    sns = sandbox
    client_name = "redacted"


if __name__ == "__main__":
    print("testing")
    print(sns)
