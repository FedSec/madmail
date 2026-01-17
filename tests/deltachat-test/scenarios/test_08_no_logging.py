"""
Test #8: No Logging Test

This test verifies that when logging is disabled on the server,
no logs are generated during message sending operations.

Steps:
1. Disable debug/logging on server via SSH
2. Restart maddy service
3. Record current journal position
4. Send 10 P2P messages
5. Send 10 group messages
6. Send 10 federation messages (cross-server)
7. Check that no new logs were generated
8. Re-enable logging for subsequent tests
"""

import subprocess
import time


def run_ssh_command(remote, command):
    """Run a command on remote server via SSH"""
    result = subprocess.run(
        ["ssh", f"root@{remote}", command],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.returncode, result.stdout, result.stderr


def disable_logging(remote):
    """Disable logging in maddy.conf"""
    print(f"  Disabling logging on {remote}...")
    
    # Update maddy.conf to disable logging
    commands = [
        # Ensure log is set to off
        "sed -i 's/^log .*/log off/' /etc/maddy/maddy.conf",
        # Set all debug options to false/no
        "sed -i 's/debug yes/debug no/g' /etc/maddy/maddy.conf",
        "sed -i 's/debug true/debug false/g' /etc/maddy/maddy.conf",
    ]
    
    for cmd in commands:
        returncode, stdout, stderr = run_ssh_command(remote, cmd)
        if returncode != 0:
            print(f"    Warning: {cmd} returned {returncode}: {stderr}")
    
    # Restart maddy service
    print(f"  Restarting maddy on {remote}...")
    returncode, stdout, stderr = run_ssh_command(remote, "systemctl restart maddy")
    if returncode != 0:
        raise Exception(f"Failed to restart maddy on {remote}: {stderr}")
    
    # Wait for service to start
    time.sleep(3)
    print(f"  Logging disabled on {remote}")


def enable_logging(remote):
    """Re-enable logging in maddy.conf (for subsequent tests)"""
    print(f"  Re-enabling logging on {remote}...")
    
    # These are safe defaults - the user may have different preferences
    # Just ensure debug is available for debugging
    commands = [
        "sed -i 's/^log off/log syslog/' /etc/maddy/maddy.conf",
    ]
    
    for cmd in commands:
        run_ssh_command(remote, cmd)
    
    # Restart maddy service
    returncode, stdout, stderr = run_ssh_command(remote, "systemctl restart maddy")
    if returncode != 0:
        print(f"    Warning: Failed to restart maddy on {remote}: {stderr}")
    
    time.sleep(3)
    print(f"  Logging re-enabled on {remote}")


def get_journal_cursor(remote):
    """Get current journal cursor position"""
    returncode, stdout, stderr = run_ssh_command(
        remote,
        "journalctl -u maddy.service -n 1 --output=json | jq -r '.__CURSOR'"
    )
    if returncode == 0 and stdout.strip():
        return stdout.strip()
    return None


def count_new_logs(remote, cursor):
    """Count new log entries since cursor"""
    if cursor:
        cmd = f"journalctl -u maddy.service --after-cursor='{cursor}' --no-pager 2>/dev/null | wc -l"
    else:
        # If no cursor, count logs from the last minute
        cmd = "journalctl -u maddy.service --since='1 minute ago' --no-pager 2>/dev/null | wc -l"
    
    returncode, stdout, stderr = run_ssh_command(remote, cmd)
    if returncode == 0:
        try:
            # Subtract 1 for the header line if present
            count = int(stdout.strip())
            return max(0, count - 1)  # Subtract header line
        except ValueError:
            return -1
    return -1


def run(acc1, acc2, acc3, group_chat, remotes):
    """
    Test #8: No Logging Test
    
    Verifies that with logging disabled, message operations produce no logs.
    
    Args:
        acc1: First account (server 1)
        acc2: Second account (server 2)
        acc3: Third account (server 2) - for federation testing
        group_chat: Existing group chat from previous test
        remotes: Tuple of (REMOTE1, REMOTE2) server addresses
    """
    REMOTE1, REMOTE2 = remotes
    
    print("\n" + "="*50)
    print("TEST #8: No Logging Test")
    print("="*50)
    
    try:
        # Step 1: Disable logging on both servers
        print("\nStep 1: Disabling logging on servers...")
        disable_logging(REMOTE1)
        disable_logging(REMOTE2)
        
        # Step 2: Record current journal positions
        print("\nStep 2: Recording journal positions...")
        cursor1 = get_journal_cursor(REMOTE1)
        cursor2 = get_journal_cursor(REMOTE2)
        print(f"  Server 1 cursor: {cursor1[:20] if cursor1 else 'None'}...")
        print(f"  Server 2 cursor: {cursor2[:20] if cursor2 else 'None'}...")
        
        # Wait a moment for things to settle
        time.sleep(2)
        
        # Step 3: Send 10 P2P messages (acc1 to acc2 - cross-server)
        print("\nStep 3: Sending 10 P2P encrypted messages (Server1 -> Server2)...")
        acc2_email = acc2.get_config("addr")
        acc2_contact = acc1.get_contact_by_addr(acc2_email)
        if acc2_contact:
            p2p_chat = acc2_contact.create_chat()
        else:
            p2p_chat = acc1.create_chat(acc2)
        for i in range(10):
            msg = f"NoLog P2P Test Message {i+1}/10"
            p2p_chat.send_text(msg)
            print(f"  Sent P2P message {i+1}/10")
            time.sleep(0.5)  # Small delay between messages
        
        # Wait for messages to be processed
        print("  Waiting for P2P messages to be processed...")
        time.sleep(10)
        
        # Step 4: Send 10 group messages
        print("\nStep 4: Sending 10 group messages...")
        for i in range(10):
            msg = f"NoLog Group Test Message {i+1}/10"
            group_chat.send_text(msg)
            print(f"  Sent group message {i+1}/10")
            time.sleep(0.5)  # Small delay between messages
        
        # Wait for messages to be processed
        print("  Waiting for group messages to be processed...")
        time.sleep(10)
        
        # Step 5: Send 10 federation messages (acc1 to acc3)
        if acc3:
            print("\nStep 5: Sending 10 federation messages (Server1 -> Server2 acc3)...")
            acc3_email = acc3.get_config("addr")
            acc3_contact = acc1.get_contact_by_addr(acc3_email)
            if acc3_contact:
                fed_chat = acc3_contact.create_chat()
            else:
                acc3_contact = acc1.create_contact(acc3_email, "Federation User")
                fed_chat = acc3_contact.create_chat()
            for i in range(10):
                msg = f"NoLog Federation Test Message {i+1}/10"
                fed_chat.send_text(msg)
                print(f"  Sent federation message {i+1}/10")
                time.sleep(0.5)
            
            print("  Waiting for federation messages to be processed...")
            time.sleep(10)
        else:
            print("\nStep 5: Skipping federation messages (no acc3 provided)")
        
        # Step 6: Check for new logs
        print("\nStep 6: Checking for new logs...")
        new_logs1 = count_new_logs(REMOTE1, cursor1)
        new_logs2 = count_new_logs(REMOTE2, cursor2)
        
        print(f"  Server 1 new log entries: {new_logs1}")
        print(f"  Server 2 new log entries: {new_logs2}")
        
        # Step 7: Verify no logs (or minimal system logs only)
        # Allow for a small number of system messages (service health checks etc)
        MAX_ALLOWED_LOGS = 2  # Allow a tiny bit of tolerance for system messages
        
        if new_logs1 <= MAX_ALLOWED_LOGS and new_logs2 <= MAX_ALLOWED_LOGS:
            print(f"\n✓ SUCCESS: No significant logs generated!")
            print(f"  Server 1: {new_logs1} entries (max allowed: {MAX_ALLOWED_LOGS})")
            print(f"  Server 2: {new_logs2} entries (max allowed: {MAX_ALLOWED_LOGS})")
            return True
        else:
            print(f"\n✗ FAILED: Unexpected logs were generated!")
            print(f"  Server 1: {new_logs1} entries")
            print(f"  Server 2: {new_logs2} entries")
            
            # Show what logs were generated
            print("\n  Recent logs from Server 1:")
            _, logs1, _ = run_ssh_command(REMOTE1, 
                f"journalctl -u maddy.service --after-cursor='{cursor1}' --no-pager 2>/dev/null | head -20")
            print(logs1)
            
            raise Exception(f"Logs were generated when logging was disabled. Server1: {new_logs1}, Server2: {new_logs2}")
            
    finally:
        # Always re-enable logging for future tests
        print("\nStep 7: Re-enabling logging on servers...")
        try:
            enable_logging(REMOTE1)
        except Exception as e:
            print(f"  Warning: Failed to re-enable logging on {REMOTE1}: {e}")
        try:
            enable_logging(REMOTE2)
        except Exception as e:
            print(f"  Warning: Failed to re-enable logging on {REMOTE2}: {e}")
