# Ansible HTTPD Role

This Ansible role installs and configures Apache (`httpd`) on a remote host.

## Prerequisites

Before running the playbook, ensure the following:

1. **Edit sudoers for Passwordless SSH**
   - Run `visudo` and add the following line:
     ```
     your_user ALL=(ALL) NOPASSWD: ALL
     ```

2. **Copy Your SSH Key to the Remote Host**
   - Run the following command to enable passwordless authentication:
     ```
     ssh-copy-id your_user@your_remote_host
     ```
   - Verify that you can log in without a password:
     ```
     ssh your_user@your_remote_host
     ```

## Usage

1. **Ensure you have Ansible installed**
   ```
   ansible --version
   ```

2. **Run the playbook**
   ```
   ansible-playbook -i inventory httpd.yml
   ```

   - Replace `inventory` with your inventory file.
   - Replace `httpd.yml` with your playbook file.

## Variables

The following variables can be modified in `vars/main.yml`:

```yaml
apache_package:
  RedHat: httpd
  Debian: apache2
  Suse: apache2

vhosts_root:
  RedHat: /var/www/html
  Debian: /var/www/html
  Suse: /srv/www/htdocs
```

## Troubleshooting

- If SSH authentication fails, ensure `sshd_config` allows `PubkeyAuthentication`:
  ```
  sudo nano /etc/ssh/sshd_config
  ```
  Set:
  ```
  PubkeyAuthentication yes
  PasswordAuthentication no
  ```
  Restart SSH:
  ```
  sudo systemctl restart sshd
  ```

- If `sudo` prompts for a password, double-check your `visudo` configuration.