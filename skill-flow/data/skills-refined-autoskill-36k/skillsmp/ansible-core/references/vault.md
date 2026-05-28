# Ansible-Core - Vault

**Pages:** 4

---

## Using encrypted variables and files — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/vault_guide/vault_using_encrypted_content.html

**Contents:**
- Using encrypted variables and files
- Passing a single password
- Passing vault IDs
- Passing multiple vault passwords
- Using --vault-id without a vault ID
- Configuring defaults for using encrypted content
- Setting a default vault ID
- Setting a default password source
- When are encrypted files made visible?
- Format of files encrypted with Ansible Vault

When you run a task or playbook that uses encrypted variables or files, you must provide the passwords to decrypt the variables or files. You can do this at the command line or by setting a default password source in a config option or an environment variable.

If all the encrypted variables and files in your task or playbook need to use a single password, you can use the --ask-vault-pass or --vault-password-file cli options.

To prompt for the password:

To retrieve the password from the /path/to/my/vault-password-file file:

To get the password from the vault password client script my-vault-password-client.py:

You can also use the --vault-id option to pass a single password with its vault label. This approach is clearer when multiple vaults are used within a single inventory.

To prompt for the password for the ‘dev’ vault ID:

To retrieve the password for the ‘dev’ vault ID from the dev-password file:

To get the password for the ‘dev’ vault ID from the vault password client script my-vault-password-client.py:

If your task or playbook requires multiple encrypted variables or files that you encrypted with different vault IDs, you must use the --vault-id option, passing multiple --vault-id options to specify the vault IDs (‘dev’, ‘prod’, ‘cloud’, ‘db’) and sources for the passwords (prompt, file, script). For example, to use a ‘dev’ password read from a file and to be prompted for the ‘prod’ password:

By default, the vault ID labels (dev, prod and so on) are only hints. Ansible attempts to decrypt vault content with each password. The password with the same label as the encrypted data will be tried first, after that, each vault secret will be tried in the order they were provided on the command line.

Where the encrypted data has no label, or the label does not match any of the provided labels, the passwords will be tried in the order they are specified. In the example above, the ‘dev’ password will be tried first, then the ‘prod’ password for cases where Ansible doesn’t know which vault ID is used to encrypt something.

The --vault-id option can also be used without specifying a vault-id. This behavior is equivalent to --ask-vault-pass or --vault-password-file so is rarely used.

For example, to use a password file dev-password:

To prompt for the password:

To get the password from an executable script my-vault-password-client.py:

If you use one vault ID more frequently than any other, you can set the config option DEFAULT_VAULT_IDENTITY_LIST to specify a default vault ID and password source. Ansible will use the default vault ID and source any time you do not specify --vault-id. You can set multiple values for this option. Setting multiple values is equivalent to passing multiple --vault-id cli options.

If you don’t want to provide the password file on the command line or if you use one vault password file more frequently than any other, you can set the DEFAULT_VAULT_PASSWORD_FILE config option or the ANSIBLE_VAULT_PASSWORD_FILE environment variable to specify a default file to use. For example, if you set ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt, Ansible will automatically search for the password in that file. This is useful if, for example, you use Ansible from a continuous integration system such as Jenkins.

The file that you reference can be either a file containing the password (in plain text), or it can be a script (with executable permissions set) that returns the password.

In general, the content you encrypt with Ansible Vault remains encrypted after execution. However, there is one exception. If you pass an encrypted file as the src argument to the copy, template, unarchive, script or assemble module, the file will not be encrypted on the target host (assuming you supply the correct vault password when you run the play). This behavior is intended and useful. You can encrypt a configuration file or template to avoid sharing the details of your configuration, but when you copy that configuration to servers in your environment, you want it to be decrypted so local users and processes can access it.

Ansible Vault creates UTF-8 encoded txt files. The file format includes a newline terminated header. For example:

The header contains up to four elements, separated by semi-colons (;).

The format ID ($ANSIBLE_VAULT). Currently $ANSIBLE_VAULT is the only valid format ID. The format ID identifies content that is encrypted with Ansible Vault (with vault.is_encrypted_file()).

The vault format version (1.X). All supported versions of Ansible will currently default to ‘1.1’ or ‘1.2’ if a labeled vault ID is supplied. The ‘1.0’ format is supported for reading only (and will be converted automatically to the ‘1.1’ format on write). The format version is currently used as an exact string compare only (version numbers are not currently ‘compared’).

The cipher algorithm used to encrypt the data (AES256). Currently AES256 is the only supported cipher algorithm. Vault format 1.0 used ‘AES’, but the current code always uses ‘AES256’.

The vault ID label used to encrypt the data (optional, vault-id-label) For example, if you encrypt a file with --vault-id dev@prompt, the vault-id-label is dev.

Note: In the future, the header could change. Fields after the format ID and format version depend on the format version. Future vault format versions may add more cipher algorithm options and/or additional fields.

The rest of the content of the file is the ‘vaulttext’. The vaulttext is a text-armored version of the encrypted ciphertext. Each line is 80 characters wide, except for the last line which may be shorter.

The vaulttext is a concatenation of the ciphertext and a SHA256 digest with the result ‘hexlifyied’.

‘hexlify’ refers to the hexlify() method of the Python Standard Library’s binascii module.

hexlify()’ed result of:

hexlify()’ed string of the salt, followed by a newline (0x0a)

hexlify()’ed string of the encrypted HMAC, followed by a newline. The HMAC is:

The AES256 encrypted ciphertext

A PBKDF2 key. This key, the cipher key, and the cipher IV are generated from:

the first 32 bytes are the cipher key

the second 32 bytes are the HMAC key

the remaining 16 bytes are the cipher IV

hexlify()’ed string of the ciphertext. The ciphertext is:

AES256 encrypted data. The data is encrypted using:

AES-CTR stream cipher

a 128-bit counter block seeded from an integer IV

the original plaintext

padding up to the AES256 blocksize. (The data used for padding is based on RFC5652)

**Examples:**

Example 1 (unknown):
```unknown
ansible-playbook --ask-vault-pass site.yml
```

Example 2 (unknown):
```unknown
ansible-playbook --vault-password-file /path/to/my/vault-password-file site.yml
```

Example 3 (unknown):
```unknown
ansible-playbook --vault-password-file my-vault-password-client.py
```

Example 4 (unknown):
```unknown
ansible-playbook --vault-id dev@prompt site.yml
```

---

## Managing vault passwords — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/vault_guide/vault_managing_passwords.html

**Contents:**
- Managing vault passwords
- Choosing between a single password and multiple passwords
- Managing multiple passwords with vault IDs
  - Limitations of vault IDs
  - Enforcing vault ID matching
- Storing and accessing vault passwords
  - Storing passwords in files
  - Storing passwords in third-party tools with vault password client scripts

Managing your encrypted content is easier if you develop a strategy for managing your vault passwords. A vault password can be any string you choose. There is no special command to create a vault password. However, you need to keep track of your vault passwords. Each time you encrypt a variable or file with Ansible Vault, you must provide a password. When you use an encrypted variable or file in a command or playbook, you must provide the same password that was used to encrypt it. To develop a strategy for managing vault passwords, start with two questions:

Do you want to encrypt all your content with the same password, or use different passwords for different needs?

Where do you want to store your password or passwords?

If you have a small team or few sensitive values, you can use a single password for everything you encrypt with Ansible Vault. Store your vault password securely in a file or a secret manager as described below.

If you have a larger team or many sensitive values, you can use multiple passwords. For example, you can use different passwords for different users or different levels of access. Depending on your needs, you might want a different password for each encrypted file, for each directory, or each environment. You might have a playbook that includes two vars files, one for the dev environment and one for the production environment, encrypted with two different passwords. When you run the playbook, you can select the correct vault password for the environment you are targeting using a vault ID.

If you use multiple vault passwords, you can differentiate one password from another with vault IDs. You use the vault ID in three ways:

Pass it with --vault-id to the ansible-vault command when you create encrypted content

Include it wherever you store the password for that vault ID (see Storing and accessing vault passwords)

Pass it with --vault-id to the ansible-playbook command when you run a playbook that uses content you encrypted with that vault ID

When you pass a vault ID as an option to the ansible-vault command, you add a label (a hint or nickname) to the encrypted content. This label documents which password you used to encrypt it. The encrypted variable or file includes the vault ID label in plain text in the header. The vault ID is the last element before the encrypted content. For example:

In addition to the label, you must provide a source for the related password. The source can be a prompt, a file, or a script, depending on how you are storing your vault passwords. The pattern looks like this:

If your playbook uses multiple encrypted variables or files that you encrypted with different passwords, you must pass the vault IDs when you run that playbook. You can use --vault-id by itself, with --vault-password-file, or with --ask-vault-pass. The pattern is the same as when you create encrypted content: include the label and the source for the matching password.

See below for examples of encrypting content with vault IDs and using content encrypted with vault IDs. The --vault-id option works with any Ansible command that interacts with vaults, including ansible-vault, ansible-playbook, and so on.

Ansible does not enforce using the same password every time you use a particular vault ID label. You can encrypt different variables or files with the same vault ID label but different passwords. This usually happens when you type the password at a prompt and make a mistake. It is possible to use different passwords with the same vault ID label on purpose. For example, you could use each label as a reference to a class of passwords, rather than a single password. In this scenario, you must always know which specific password or file to use in context. However, you are more likely to encrypt two files with the same vault ID label and different passwords by mistake. If you encrypt two files with the same label but different passwords by accident, you can rekey one file to fix the issue.

By default, the vault ID label is only a hint to remind you which password you used to encrypt a variable or file. Ansible does not check that the vault ID in the header of the encrypted content matches the vault ID you provide when you use the content. Ansible decrypts all files and variables called by your command or playbook that are encrypted with the password you provide. To check the encrypted content and decrypt it only when the vault ID it contains matches the one you provide with --vault-id, set the config option DEFAULT_VAULT_ID_MATCH. When you set DEFAULT_VAULT_ID_MATCH, each password is only used to decrypt data that was encrypted with the same label. This is efficient and predictable and can reduce errors when different values are encrypted with different passwords.

Even with the DEFAULT_VAULT_ID_MATCH setting enabled, Ansible does not enforce using the same password every time you use a particular vault ID label.

You can memorize your vault password or manually copy vault passwords from any source and paste them at a command-line prompt, but most users store them securely and access them as needed from within Ansible. You have two options for storing vault passwords that work from within Ansible: in files or a third-party tool, such as the system keyring or a secret manager. If you store your passwords in a third-party tool, you need a vault password client script to retrieve them from within Ansible.

To store a vault password in a file, enter the password as a string on a single line in the file. Make sure the permissions on the file are appropriate. Do not add password files to source control.

When you run a playbook that uses a vault password stored in a file, specify the file within the --vault-password-file flag. For example:

You can store your vault passwords on the system keyring, in a database, or in a secret manager and retrieve them from within Ansible using a vault password client script. Enter the password as a string on a single line. If your password has a vault ID, store it in a way that works with your password storage tool.

To create a vault password client script:

Create a file with a name ending in either -client or -client.EXTENSION

Make the file executable

Print the passwords to standard output

Accept a --vault-id option

If the script prompts for data (for example, a database password), display the prompts to the TTY.

When you run a playbook that uses vault passwords stored in a third-party tool, specify the script as the source within the --vault-id flag. For example:

Ansible executes the client script with a --vault-id option so the script knows which vault ID label you specified. For example, a script loading passwords from a secret manager can use the vault ID label to pick either the ‘dev’ or ‘prod’ password. The example command above results in the following execution of the client script:

For an example of a client script that loads passwords from the system keyring, see the vault-keyring-client script.

**Examples:**

Example 1 (unknown):
```unknown
my_encrypted_var: !vault |
          $ANSIBLE_VAULT;1.2;AES256;dev
          30613233633461343837653833666333643061636561303338373661313838333565653635353162
          3263363434623733343538653462613064333634333464660a663633623939393439316636633863
          61636237636537333938306331383339353265363239643939666639386530626330633337633833
          6664656334373166630a363736393262666465663432613932613036303963343263623137386239
          6330
```

Example 2 (unknown):
```unknown
--vault-id label@source
```

Example 3 (unknown):
```unknown
ansible-playbook --extra-vars @secrets.enc --vault-password-file secrets.pass
```

Example 4 (unknown):
```unknown
ansible-playbook --vault-id dev@contrib-scripts/vault/vault-keyring-client.py
```

---

## Encrypting content with Ansible Vault — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/vault_guide/vault_encrypting_content.html

**Contents:**
- Encrypting content with Ansible Vault
- Encrypting individual variables with Ansible Vault
  - Advantages and disadvantages of encrypting variables
  - Creating encrypted variables
  - Viewing encrypted variables
- Encrypting files with Ansible Vault
  - Advantages and disadvantages of encrypting files
  - Creating encrypted files
  - Encrypting existing files
  - Viewing encrypted files

Once you have a strategy for managing and storing vault passwords, you can start encrypting content. You can encrypt two types of content with Ansible Vault: variables and files. Encrypted content always includes the !vault tag, which tells Ansible and YAML that the content needs to be decrypted, and a | character, which allows multi-line strings. Encrypted content created with --vault-id also contains the vault ID label. For more details about the encryption process and the format of content encrypted with Ansible Vault, see Format of files encrypted with Ansible Vault. This table shows the main differences between encrypted variables and encrypted files:

How much is encrypted?

Variables within a plaintext file

When is it decrypted?

On demand, only when needed

Whenever loaded or referenced [1]

What can be encrypted?

Any structured data file

Ansible cannot know if it needs content from an encrypted file unless it decrypts the file, so it decrypts all encrypted files referenced in your playbooks and roles.

You can encrypt single values inside a YAML file using the ansible-vault encrypt_string command. For one way to keep your vaulted variables safely visible, see Keep vaulted variables safely visible.

With variable-level encryption, your files are still easily legible. You can mix plaintext and encrypted variables, even inline in a play or role. However, password rotation is not as simple as with file-level encryption. You cannot rekey encrypted variables. Also, variable-level encryption only works on variables. If you want to encrypt tasks or other content, you must encrypt the entire file.

The ansible-vault encrypt_string command encrypts and formats any string you type (or copy or generate) into a format that can be included in a playbook, role, or variables file. To create a basic encrypted variable, pass three options to the ansible-vault encrypt_string command:

a source for the vault password (prompt, file, or script, with or without a vault ID)

the string to encrypt

the string name (the name of the variable)

The pattern looks like this:

For example, to encrypt the string ‘foobar’ using the only password stored in ‘a_password_file’ and name the variable ‘the_secret’:

The command above creates this content:

To encrypt the string ‘foooodev’, add the vault ID label ‘dev’ with the ‘dev’ vault password stored in ‘a_password_file’, and call the encrypted variable ‘the_dev_secret’:

The command above creates this content:

To encrypt the string ‘letmein’ read from stdin, add the vault ID ‘dev’ using the ‘dev’ vault password stored in a_password_file, and name the variable ‘db_password’:

Typing secret content directly at the command line (without a prompt) leaves the secret string in your shell history. Do not do this outside of testing.

The command above creates this output:

To be prompted for a string to encrypt, encrypt it with the ‘dev’ vault password from ‘a_password_file’, name the variable ‘new_user_password’ and give it the vault ID label ‘dev’:

The command above triggers this prompt:

Type the string to encrypt (for example, ‘hunter2’), hit ctrl-d, and wait.

Do not press Enter after supplying the string to encrypt. That will add a newline to the encrypted value.

The sequence above creates this output:

You can add the output from any of the examples above to any playbook, variables file, or role for future use. Encrypted variables are larger than plain-text variables, but they protect your sensitive content while leaving the rest of the playbook, variables file, or role in plain text so you can easily read it.

You can view the original value of an encrypted variable using the debug module. You must pass the password that was used to encrypt the variable. For example, if you stored the variable created by the last example above in a file called ‘vars.yml’, you could view the unencrypted value of that variable like this:

Ansible Vault can encrypt any structured data file used by Ansible, including:

group variables files from inventory

host variables files from inventory

variables files passed to ansible-playbook with -e @file.yml or -e @file.json

variables files loaded by include_vars or vars_files

variables files in roles

defaults files in roles

binary files or other arbitrary files

The full file is encrypted in the vault.

Ansible Vault uses an editor to create or modify encrypted files. See Steps to secure your editor for some guidance on securing the editor.

File-level encryption is easy to use. Password rotation for encrypted files is straightforward with the rekey command. Encrypting files can hide not only sensitive values but the names of the variables you use. However, with file-level encryption, the contents of files are no longer easy to access and read. This may be a problem with encrypted tasks files. When encrypting a variables file, see Keep vaulted variables safely visible for one way to keep references to these variables in a non-encrypted file. Ansible always decrypts the entire encrypted file when it is loaded or referenced because Ansible cannot know if it needs the content unless it decrypts it.

To create a new encrypted data file called ‘foo.yml’ with the ‘test’ vault password from ‘multi_password_file’:

The tool launches an editor (whatever editor you have defined with $EDITOR, the default editor is vi). Add the content. When you close the editor session, the file is saved as encrypted data. The file header reflects the vault ID used to create it:

To create a new encrypted data file with the vault ID ‘my_new_password’ assigned to it and be prompted for the password:

Again, add content to the file in the editor and save. Be sure to store the new password you created at the prompt, so you can find it when you want to decrypt that file.

To encrypt an existing file, use the ansible-vault encrypt command. This command can operate on multiple files at once. For example:

To encrypt existing files with the ‘project’ ID and be prompted for the password:

To view the contents of an encrypted file without editing it, you can use the ansible-vault view command:

To edit an encrypted file in place, use the ansible-vault edit command. This command decrypts the file to a temporary file, allows you to edit the content, then saves and re-encrypts the content and removes the temporary file when you close the editor. For example:

To edit a file encrypted with the vault2 password file and assigned the vault ID pass2:

To change the password on an encrypted file or files, use the rekey command:

This command can rekey multiple data files at once and will ask for the original password and also the new password. To set a different ID for the rekeyed files, pass the new ID to --new-vault-id. For example, to rekey a list of files encrypted with the ‘preprod1’ vault ID from the ‘ppold’ file to the ‘preprod2’ vault ID and be prompted for the new password:

If you have an encrypted file that you no longer want to keep encrypted, you can permanently decrypt it by running the ansible-vault decrypt command. This command will save the file unencrypted to the disk, so be sure you do not want to edit it instead.

If you just want to check the content of an encrypted string you can also view it by passing it via stdin:

Alternatively you can use the following command to have Ansible prompt you for input (use Ctrl+D twice to end the input), just like when using encrypt_string:

Ansible Vault relies on your configured editor, which can be a source of disclosures. Most editors have ways to prevent loss of data, but these normally rely on extra plain text files that can have a clear text copy of your secrets. Consult your editor documentation to configure the editor to avoid disclosing secure data. The following sections provide some guidance on common editors but should not be taken as a complete guide to securing your editor.

You can set the following vim options in command mode to avoid cases of disclosure. There may be more settings you need to modify to ensure security, especially when using plugins, so consult the vim documentation.

Disable swapfiles that act like an autosave in case of crash or interruption.

Disable the creation of backup files.

Disable the viminfo file from copying data from your current session.

Disable copying to the system clipboard.

You can optionally add these settings in .vimrc for all files, or just specific paths or extensions. See the vim manual for details.

You can set the following Emacs options to avoid cases of disclosure. There may be more settings you need to modify to ensure security, especially when using plugins, so consult the Emacs documentation.

Do not copy data to the system clipboard.

Disable the creation of backup files.

Disable autosave files.

**Examples:**

Example 1 (unknown):
```unknown
ansible-vault encrypt_string <password_source> '<string_to_encrypt>' --name '<string_name_of_variable>'
```

Example 2 (unknown):
```unknown
ansible-vault encrypt_string --vault-password-file a_password_file 'foobar' --name 'the_secret'
```

Example 3 (unknown):
```unknown
the_secret: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      62313365396662343061393464336163383764373764613633653634306231386433626436623361
      6134333665353966363534333632666535333761666131620a663537646436643839616531643561
      63396265333966386166373632626539326166353965363262633030333630313338646335303630
      3438626666666137650a353638643435666633633964366338633066623234616432373231333331
      6564
```

Example 4 (unknown):
```unknown
ansible-vault encrypt_string --vault-id dev@a_password_file 'foooodev' --name 'the_dev_secret'
```

---

## ansible-vault — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/cli/ansible-vault.html

**Contents:**
- ansible-vault
- Synopsis
- Description
- Common Options
- Actions
  - create
  - decrypt
  - edit
  - view
  - encrypt

encryption/decryption utility for Ansible data files

can encrypt any structured data file used by Ansible. This can include group_vars/ or host_vars/ inventory variables, variables loaded by include_vars or vars_files, or variable files passed on the ansible-playbook command line with -e @file.yml or -e @file.json. Role variables and defaults are also included!

Because Ansible tasks, handlers, and other objects are data, these can also be encrypted with vault. If you’d like to not expose what variables you are using, you can keep an individual task file entirely encrypted.

show program’s version number, config file location, configured module search path, module location, executable location and exit

show this help message and exit

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity, the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv. This argument may be specified multiple times.

create and open a file in an editor that will be encrypted with the provided vault secret when closed

the vault id used to encrypt (required if more than one vault-id is provided)

allows editor to be opened when no tty attached

the vault identity to use. This argument may be specified multiple times.

ask for vault password

decrypt the supplied file using the provided vault secret

output file name for encrypt or decrypt; use - for stdout

the vault identity to use. This argument may be specified multiple times.

ask for vault password

open and decrypt an existing vaulted file in an editor, that will be encrypted again when closed

the vault id used to encrypt (required if more than one vault-id is provided)

the vault identity to use. This argument may be specified multiple times.

ask for vault password

open, decrypt and view an existing vaulted file using a pager using the supplied vault secret

the vault identity to use. This argument may be specified multiple times.

ask for vault password

encrypt the supplied file using the provided vault secret

the vault id used to encrypt (required if more than one vault-id is provided)

output file name for encrypt or decrypt; use - for stdout

the vault identity to use. This argument may be specified multiple times.

ask for vault password

encrypt the supplied string using the provided vault secret

the vault id used to encrypt (required if more than one vault-id is provided)

output file name for encrypt or decrypt; use - for stdout

Do not hide input when prompted for the string to encrypt

Specify the variable name for stdin

the vault identity to use. This argument may be specified multiple times.

ask for vault password

Specify the variable name. This argument may be specified multiple times.

Prompt for the string to encrypt

re-encrypt a vaulted file with a new secret, the previous secret is required

the vault id used to encrypt (required if more than one vault-id is provided)

the new vault identity to use for rekey

new vault password file for rekey

the vault identity to use. This argument may be specified multiple times.

ask for vault password

The following environment variables may be specified.

ANSIBLE_CONFIG – Override the default ansible config file

Many more are available for most options in ansible.cfg

/etc/ansible/ansible.cfg – Config file, used if present

~/.ansible.cfg – User config file, overrides the default config if present

Ansible was originally written by Michael DeHaan.

See the AUTHORS file for a complete list of contributors.

Ansible is released under the terms of the GPLv3+ License.

ansible(1), ansible-config(1), ansible-console(1), ansible-doc(1), ansible-galaxy(1), ansible-inventory(1), ansible-playbook(1), ansible-pull(1),

**Examples:**

Example 1 (unknown):
```unknown
usage: ansible-vault [-h] [--version] [-v]
                  {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
                  ...
```

---
