import time

def run(rpc, inviter, joiner):
    print("Starting Secure Join...")
    
    qr_data = inviter.get_qr_code()
    print(f"Secure Join QR data: {qr_data[:50]}...")
    
    joiner_email = joiner.get_config("addr")
    inviter_email = inviter.get_config("addr")
    
    print(f"Joiner ({joiner_email}) joining Inviter ({inviter_email})...")
    joiner.secure_join(qr_data)
    
    # Wait for success
    print("Waiting for Secure Join handshakes...")
    max_wait = 120
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        # Check if joiner has inviter in contacts and is verified
        contact_on_joiner = joiner.get_contact_by_addr(inviter_email)
        if contact_on_joiner:
            snap = contact_on_joiner.get_snapshot()
            is_verified = snap.is_verified
            is_key_contact = snap.is_key_contact
            print(f"    - [Joiner] contact {inviter_email} status: verified={is_verified}, key_contact={is_key_contact}")
            if is_verified:
                print("SUCCESS: Secure Join complete!")
                return True
        
        # Check if inviter has joiner in contacts and status (optional but helpful)
        contact_on_inviter = inviter.get_contact_by_addr(joiner_email)
        if contact_on_inviter:
            snap = contact_on_inviter.get_snapshot()
            print(f"    - [Inviter] contact {joiner_email} status: verified={snap.is_verified}, key_contact={snap.is_key_contact}")

        # Check messages for joiner to see progress
        chatlist = joiner.get_chatlist()
        for chat in chatlist:
            msgs = chat.get_messages()
            if msgs:
                last_msg = msgs[-1].get_snapshot()
                print(f"    - [Joiner] Last msg in chat '{chat.get_basic_snapshot().name}': {last_msg.text[:50]}...")

        time.sleep(5)
    
    raise Exception("Secure Join failed or timed out")
