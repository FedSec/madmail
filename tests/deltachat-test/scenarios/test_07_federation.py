"""
Test #7: Federation Test

This test verifies that messages can be sent between accounts on different servers
AND between accounts on the same server.

Steps:
1. Create a third account on server 2
2. Perform secure join between acc2 and acc3 (same server)
3. Test message delivery from acc2 to acc3 (same server, encrypted)
4. Test reply from acc3 to acc2
"""

import time


def run(rpc, dc, acc1, acc2, remote2, timestamp):
    """
    Test #7: Federation Test
    
    Tests same-server message delivery by creating a third account
    on server 2 and doing secure join + messaging with acc2.
    
    Args:
        rpc: RPC instance
        dc: DeltaChat instance
        acc1: Account on server 1
        acc2: Account on server 2 (already established from secure join with acc1)
        remote2: Address of second server
        timestamp: Test run timestamp
    
    Returns:
        acc3: The third account created for use in subsequent tests
    """
    from scenarios import test_01_account_creation, test_03_secure_join
    
    print("\nStep 1: Creating third account on server 2...")
    acc3 = test_01_account_creation.run(dc, remote2)
    acc3_email = acc3.get_config("addr")
    acc2_email = acc2.get_config("addr")
    
    print(f"  Acc2 Email: {acc2_email}")
    print(f"  Acc3 Email: {acc3_email}")
    
    print(f"\nStep 2: Performing secure join between acc2 and acc3 (both on server 2)...")
    
    # Ensure acc2 is active and synchronized
    print(f"  Refreshing acc2 configuration...")
    acc2.configure()
    time.sleep(2)
    
    # test_03_secure_join.run doesn't support event callbacks, so we'll just let it run
    # but maybe we should use a custom run here for better visibility
    try:
        test_03_secure_join.run(rpc, acc2, acc3)
    except Exception as e:
        print(f"  Secure join failed: {e}")
        # Let's check why
        c2 = acc3.get_contact_by_addr(acc2_email)
        if c2:
            print(f"  Acc3 contact for Acc2: {c2.get_snapshot()}")
        c3 = acc2.get_contact_by_addr(acc3_email)
        if c3:
            print(f"  Acc2 contact for Acc3: {c3.get_snapshot()}")
        raise e
    print("  Secure join between acc2 and acc3 completed")
    
    # Test: acc2 sends message to acc3 (same server, encrypted)
    print(f"\nStep 3: Sending encrypted message from acc2 ({acc2_email}) to acc3 ({acc3_email})...")
    
    # Get the contact created by secure join
    acc3_contact = acc2.get_contact_by_addr(acc3_email)
    if acc3_contact is None:
        raise Exception(f"Contact {acc3_email} not found after secure join")
    
    chat_2_to_3 = acc3_contact.create_chat()
    
    test_msg_1 = f"Same-Server Test: acc2 -> acc3 [{timestamp}]"
    chat_2_to_3.send_text(test_msg_1)
    print(f"  Sent: {test_msg_1}")
    
    # Wait for message to be received
    max_wait = 60
    start_time = time.time()
    received_1 = False
    
    print("  Waiting for acc3 to receive the message...")
    while time.time() - start_time < max_wait:
        chatlist = acc3.get_chatlist()
        for chat in chatlist:
            msgs = chat.get_messages()
            for msg in msgs:
                snap = msg.get_snapshot()
                if snap.text == test_msg_1:
                    print(f"  ✓ Message received by acc3: {snap.text}")
                    received_1 = True
                    break
            if received_1:
                break
        if received_1:
            break
        time.sleep(2)
    
    if not received_1:
        raise Exception(f"Federation test failed: Message from acc2 to acc3 not received within {max_wait}s")
    
    # Test: acc3 replies to acc2
    print(f"\nStep 4: Sending reply from acc3 ({acc3_email}) to acc2 ({acc2_email})...")
    
    acc2_contact = acc3.get_contact_by_addr(acc2_email)
    if acc2_contact is None:
        raise Exception(f"Contact {acc2_email} not found on acc3 after secure join")
    
    chat_3_to_2 = acc2_contact.create_chat()
    test_msg_2 = f"Same-Server Reply: acc3 -> acc2 [{timestamp}]"
    chat_3_to_2.send_text(test_msg_2)
    print(f"  Sent: {test_msg_2}")
    
    # Wait for reply
    start_time = time.time()
    received_2 = False
    
    print("  Waiting for acc2 to receive the reply...")
    while time.time() - start_time < max_wait:
        chatlist = acc2.get_chatlist()
        for chat in chatlist:
            msgs = chat.get_messages()
            for msg in msgs:
                snap = msg.get_snapshot()
                if snap.text == test_msg_2:
                    print(f"  ✓ Reply received by acc2: {snap.text}")
                    received_2 = True
                    break
            if received_2:
                break
        if received_2:
            break
        time.sleep(2)
    
    if not received_2:
        raise Exception(f"Federation test failed: Reply from acc3 to acc2 not received within {max_wait}s")
    
    print("\n✓ Federation test complete: Same-server encrypted messaging verified!")
    print("  (Cross-server was already tested by acc1<->acc2 in previous tests)")
    return acc3
