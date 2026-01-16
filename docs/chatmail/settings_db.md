# Madmail Settings Database

Madmail uses dedicated SQL tables to store dynamic configuration and user metadata. This allows the server to change its behavior (e.g., opening registration, disabling logs) without requiring a restart or configuration file modification.

## Settings Table (`settings`)

The `settings` table is a simple key-value store used for server-wide flags. In `maddy.conf`, it is typically configured via the `settings_table` directive in both `auth.pass_table` and `storage.imapsql`.

| Key | Value Type | Description |
| :--- | :--- | :--- |
| `__REGISTRATION_OPEN__` | Boolean (`true`/`false`) | Controls whether new accounts are auto-provisioned during SMTP delivery or via the chatmail registration endpoint. |
| `__TURN_ENABLED__` | Boolean (`true`/`false`) | Controls whether the TURN server functionality is active for users. |
| `__LOG_DISABLED__` | Boolean (`true`/`false`) | When set to `true`, the server dynamically disables logging to standard error/files (uses `log.NopOutput`). |

## Quota Table (`quota`)

The `quota` table manages storage limits for users and global defaults.

| Username | Description |
| :--- | :--- |
| `__GLOBAL_DEFAULT__` | A special entry that sets the default quota for all users on the server if no specific quota is defined for them. |
| *[username]* | Stores the `MaxStorage` limit (in bytes) for a specific user. |

## Other Tables

- **`contacts`**: Stores DeltaChat contact sharing links (slug, URL, name).
- **`passwords`**: Stores user credentials and hashed passwords.
- **`msgs` / `mboxes` / `users`**: Core IMAP tables managed by the storage engine.
