import random
import string
import time

def random_string(length=9):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run(dc, domain):
    print(f"Creating account on {domain}...")
    account = dc.add_account()
    username = random_string(8)
    password = random_string(16)
    # If domain is an IP address, it must be bracketed in the email part
    is_ip = all(c.isdigit() or c == '.' for c in domain)
    email_domain = f"[{domain}]" if is_ip else domain
    email = f"{username}@{email_domain}"
    
    # Using dclogin format to explicitly set hosts and bypass DNS lookups for imap.<ip>
    # The email part must have brackets for IP domains, but ih/sh must not.
    login_uri = f"dclogin:{username}@{email_domain}/?p={password}&v=1&ih={domain}&ip=993&sh={domain}&sp=465&ic=3&ss=default"
    
    account.set_config_from_qr(login_uri)
    account.set_config("displayname", f"Test User {username}")
    
    account.start_io()
    account.configure()
    
    # Wait for configuration to finish
    # In some versions of core, we should wait for the event
    max_wait = 30
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if account.is_configured():
            print(f"Account {email} configured successfully.")
            return account
        time.sleep(1)
    
    raise Exception(f"Failed to configure account {email} within {max_wait}s")
