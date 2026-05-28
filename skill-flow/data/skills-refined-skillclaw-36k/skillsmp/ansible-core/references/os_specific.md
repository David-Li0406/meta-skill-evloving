# Ansible-Core - Os Specific

**Pages:** 12

---

## Managing Windows hosts with Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/intro_windows.html

**Contents:**
- Managing Windows hosts with Ansible
- Bootstrapping Windows
- Connecting to Windows nodes
  - PSRP and WinRM
  - SSH
- Which modules are available?
- Using Windows as the control node
- Windows facts
- Common Windows problems
  - Command works locally but not under Ansible

Managing Windows hosts is different from managing POSIX hosts. If you have managed nodes running Windows, review these topics.

Bootstrapping Windows

Connecting to Windows nodes

Which modules are available?

Using Windows as the control node

Common Windows problems

Command works locally but not under Ansible

Credentials are rejected

This is an index of all the topics covered in this guide.

Windows nodes must be running Windows Server 2016 or Windows 10 or newer. As these versions of Windows ship with PowerShell 5.1 by default there are no additional requirements to bootstrap a Windows node.

Support for each Windows version is tied to the extended support lifecycle of each operating system, which is typically 10 years from the date of release. Ansible is tested against the server variants of Windows but should still be compatible with the desktop variants like Windows 10 and 11.

Ansible connects to POSIX managed nodes using OpenSSH by default. Windows nodes can also use SSH but historically they use WinRM as the connection transport. The supported connection plugins that can be used with Windows nodes are:

PowerShell Remoting over WinRM - psrp

Windows Remote Management - winrm

Historically Ansible used Windows Remote Management (WinRM) as the connection protocol to manage Windows nodes. The psrp and winrm connection plugins both operate over WinRM and can be used as the connection plugin for Windows nodes. The psrp connection plugin is a newer connection plugin that offers a few benefits over the winrm connection plugin, for example:

Can be slightly faster

Less susceptible to timeout issues when the Windows node is under load

Better support for proxy servers

See Windows Remote Management for more information on how WinRM is configured and how to use the psrp and winrm connection plugins in Ansible.

SSH is the traditional connection plugin used with POSIX nodes but it can also be used to manage Windows nodes instead of the traditional psrp or winrm connection plugins.

While Ansible has supported using the SSH connection plugin with Windows nodes since Ansible 2.8, official support was only added in version 2.18.

Some of the benefits of using SSH over the WinRM based transports are:

SSH can be easier to configure in non-domain environments

SSH supports key based authentication which is simpler to manage than certificates

SSH file transfers are faster than WinRM

See Windows SSH for more information on how to configure SSH for Windows nodes.

The majority of the core Ansible modules are written for a combination of Unix-like machines and other generic services. As these modules are written in Python and use APIs not present on Windows they will not work.

There are dedicated Windows modules that are written in PowerShell and are meant to be run on Windows hosts. A list of these modules can be in the Ansible.Windows, Community.Windows, Microsoft.Ad, Chocolatey.Chocolatey, and other collections.

In addition, the following Ansible Core modules/action-plugins work with Windows:

template (also: win_template)

Ansible cannot run on Windows as the control node due to API limitations on the platform. However, you can run Ansible on Windows using the Windows Subsystem for Linux (WSL) or in a container.

The Windows Subsystem for Linux is not supported by Ansible and should not be used for production systems.

Ansible gathers facts from Windows in a similar manner to other POSIX hosts but with some differences. Some facts may be in a different format for backwards compatibility or may not be available at all.

To see the facts that Ansible gathers from Windows hosts, run the setup module.

Ansible executes commands through a network logon which can change how Windows authorizes actions. This can cause commands that work locally to fail under Ansible. Some examples of these failures are:

the process cannot delegate the user’s credentials to a network resource, causing Access is Denied or Resource Unavailable errors

applications that require an interactive session will not work

some Windows APIs are restricted when running through a network logon

some tasks require access to the DPAPI secrets store which is typically not available on a network logon

The common way is to use Understanding privilege escalation: become to run a command with explicit credentials. Using become on Windows will change the network logon to an interactive one and, if explicit credentials are provided to the become identity, the command will be able to access network resources and unlock the DPAPI store.

Another option is to use an authentication option on the connection plugin that allows for credential delegation. For SSH this can be done with an explicit username and password or through a Kerberos/GSSAPI logon with delegation enabled. For WinRM based connections, the CredSSP or Kerberos with delegation can be used. See the connection specific documentation for more information.

There are a few reasons why credentials might be rejected when connecting to the Windows host. Some common reasons are:

the username or password is incorrect

the user account is locked out, disabled, not allowed to log onto that server

the user account is not allowed to log on through the network

the user account is not a member of the local Administrators group

the user account is a local user and the LocalAccountTokenFilterPolicy is not set

To verify whether the credentials are correct or the user is allowed to log onto the host you can run the below PowerShell command on the Windows host to see the last failed logon attempt. This will output event details including the Status and Sub Status error code indicating why the logon failed.

While not all connection plugins require the connection user to be a member of the local Administrators group, this is typically the default configuration. If the user is not a member of the local Administrators group or is a local user without LocalAccountTokenFilterPolicy set, the authentication will fail.

Examples of basic commands

Learning Ansible’s configuration management language

Using Ansible with Windows App Control managed hosts

Using Ansible with Windows Desired State Configuration

Performance considerations for managing Windows hosts

Questions? Help? Ideas? Stop by the list on Google Groups

How to join Ansible chat channels

**Examples:**

Example 1 (unknown):
```unknown
ansible windows -m setup
```

Example 2 (unknown):
```unknown
Get-WinEvent -FilterHashtable @{LogName = 'Security'; Id = 4625} |
    Select-Object -First 1 -ExpandProperty Message
```

---

## WinRM Certificate Authentication — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_winrm_certificate.html

**Contents:**
- WinRM Certificate Authentication
- Ansible Configuration
- Certificate Generation
- Windows Configuration
  - Import Certificate to the Certificate Store
  - Mapping Certificate to a Local Account
  - Using Ansible

WinRM certificate authentication is a method of authenticating to a Windows host using X.509 certificates instead of a username and password.

Ansible Configuration

Certificate Generation

Windows Configuration

Import Certificate to the Certificate Store

Mapping Certificate to a Local Account

Certificate authentication does have some disadvantages compared to SSH key based authentication such as:

it can only be mapped to a local Windows user, no domain accounts

the username and password must be mapped to the certificate, if the password changes, the cert will need to be re-mapped

an administrator on the Windows host can retrieve the local user password through the certificate mapping

Ansible cannot use encrypted private keys, they must be stored without encryption

Ansible cannot use the certs and private keys stored as a var, they must be a file

Certificate authentication uses certificates as keys similar to SSH key pairs. The public and private key is stored on the Ansible control node to use for authentication. The following example shows the hostvars configured for certificate authentication:

Certificate authentication is not enabled by default on a Windows host but can be enabled by running the following in PowerShell:

The private key cannot be encrypted due to a limitation of the underlying Python library used by Ansible.

For enabling certificate authentication with a TLS 1.3 connection, Python 3.8+, 3.7.1, or 3.6.7 and Python package urllib3>=2.0.7 or newer are required.

The first step of using certificate authentication is to generate a certificate and private key. The certificate must be generated with the following properties:

Extended Key Usage must include clientAuth (1.3.6.1.5.5.7.3.2)

Subject Alternative Name must include otherName entry for userPrincipalName (1.3.6.1.4.1.311.20.2.3)

The userPrincipalName value can be anything but in this guide we will use the value $USERNAME@localhost where $USERNAME is the name of the user that the certificate will be mapped to.

This can be done through a variety of methods, such as OpenSSL, PowerShell, or Active Directory Certificate Services. The following example shows how to generate a certificate using OpenSSL:

The following example shows how to generate a certificate using PowerShell:

As PowerShell cannot generate a PKCS8 PEM private key, we need to use OpenSSL to convert the cert.pfx file to a PEM private key:

The cert.pem is the public key and the cert.key is the plaintext private key. These files must be accessible by the Ansible control node to use for authentication. The private key does not need to be present on the Windows node.

Once the public and private key has been generated we need to import and trust the public key and configure the user mapping on the Windows host. The Windows host does not need access to the private key, only the public key cert.pem needs to be accessible to configure the certificate authentication.

For Windows to trust the certificate it must be imported into the LocalMachine\TrustedPeople certificate store. You can do this by running the following:

If the cert is self-signed, or issued by a CA that is not trusted by the host, you will need to import the CA certificate into the trusted root store. As our example uses a self-signed cert, we will import that certificate as a trusted CA but in a production environment you would import the CA that signed the certificate.

Once the certificate has been imported into the LocalMachine\TrustedPeople store, the WinRM service can create the mapping between the certificate and a local account. This is done by running the following:

The Subject is the value of the userPrincipalName in the certificate SAN entry. The Issuer is the thumbprint of the CA certificate that issued our certificate. The Credential is the username and password of the local user we are mapping the certificate to.

The following Ansible playbook can be used to create a local user and map the certificate provided to use for certificate authentication. It needs to be called username and cert_pem variable set to the name of the user to create and the path to the public key PEM file that was generated. This playbook expects cert_pem to be a self signed certificate, if using a certificate issued by a CA, you will have to edit it so it copies that across and imports it to the LocalMachine\Root store instead.

**Examples:**

Example 1 (unknown):
```unknown
# psrp
ansible_connection: psrp
ansible_psrp_auth: certificate
ansible_psrp_certificate_pem: /path/to/certificate/public_key.pem
ansible_psrp_certificate_key_pem: /path/to/certificate/private_key.pem

# winrm
ansible_connection: winrm
ansible_winrm_transport: certificate
ansible_winrm_cert_pem: /path/to/certificate/public_key.pem
ansible_winrm_cert_key_pem: /path/to/certificate/private_key.pem
```

Example 2 (unknown):
```unknown
Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true
```

Example 3 (unknown):
```unknown
# Set the username to the name of the user the certificate will be mapped to
USERNAME="local-user"

cat > openssl.conf << EOL
distinguished_name = req_distinguished_name

[req_distinguished_name]
[v3_req_client]
extendedKeyUsage = clientAuth
subjectAltName = otherName:1.3.6.1.4.1.311.20.2.3;UTF8:${USERNAME}@localhost
EOL

openssl req \
    -new \
    -sha256 \
    -subj "/CN=${USERNAME}" \
    -newkey rsa:2048 \
    -nodes \
    -keyout cert.key \
    -out cert.csr \
    -config openssl.conf \
    -reqexts v3_req_client

openssl x509 \
    -req \
    -in cert.csr \
    -sha256 \
    -out cert.pem \
    -days 365 \
    -extfile openssl.conf \
    -extensions v3_req_client \
    -key cert.key

rm openssl.conf cert.csr
```

Example 4 (unknown):
```unknown
# Set the username to the name of the user the certificate will be mapped to
$username = 'local-user'

$clientParams = @{
    CertStoreLocation = 'Cert:\CurrentUser\My'
    NotAfter          = (Get-Date).AddYears(1)
    Provider          = 'Microsoft Software Key Storage Provider'
    Subject           = "CN=$username"
    TextExtension     = @("2.5.29.37={text}1.3.6.1.5.5.7.3.2","2.5.29.17={text}upn=$username@localhost")
    Type              = 'Custom'
}
$cert = New-SelfSignedCertificate @clientParams
$certKeyName = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey(
    $cert).Key.UniqueName

# Exports the public cert.pem and key cert.pfx
Set-Content -Path "cert.pem" -Value @(
    "-----BEGIN CERTIFICATE-----"
    [Convert]::ToBase64String($cert.RawData) -replace ".{64}", "$&`n"
    "-----END CERTIFICATE-----"
)
$certPfxBytes = $cert.Export('Pfx', '')
[System.IO.File]::WriteAllBytes("$pwd\cert.pfx", $certPfxBytes)

# Removes the private key and cert from the store after exporting
$keyPath = [System.IO.Path]::Combine($env:AppData, 'Microsoft', 'Crypto', 'Keys', $certKeyName)
Remove-Item -LiteralPath "Cert:\CurrentUser\My\$($cert.Thumbprint)" -Force
Remove-Item -LiteralPath $keyPath -Force
```

---

## Red Hat Ansible Automation Platform — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/reference_appendices/tower.html

**Contents:**
- Red Hat Ansible Automation Platform

Red Hat Ansible Automation Platform is available on multiple cloud platforms. See Ansible on Clouds for details.

Red Hat Ansible Automation Platform (RHAAP) is an integrated solution for operationalizing Ansible across your team, organization, and enterprise. The platform includes a controller with a web console and REST API, analytics, Execution Environments, and much more.

RHAAP gives you role-based access control, including control over the use of securely stored credentials for SSH and other services. You can sync your inventory with a wide variety of cloud sources, and powerful multi-playbook workflows allow you to model complex processes.

RHAAP logs all of your jobs, integrates well with LDAP, SAML, and other authentication sources, and has an amazing browsable REST API. Command line tools are available for easy integration with Jenkins as well.

RHAAP incorporates the downstream Red Hat supported product version of Ansible AWX, the downstream Red Hat supported product version of Ansible Galaxy, and multiple SaaS offerings. Find out more about RHAAP features and on the Red Hat Ansible Automation Platform webpage. A Red Hat Ansible Automation Platform subscription includes support from Red Hat, Inc.

---

## Windows App Control — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_app_control.html

**Contents:**
- Windows App Control
- Requirements for Ansible to work with App Control
- How to Sign Ansible Content
- Known Module Differences

Windows App Control, formerly known as Windows Defender Application Control (WDAC), is a security feature of Windows that can be used to restrict what executables and scripts can be run on a Windows host. In the past, enabling WDAC will cause Ansible to fail when running on the Windows host. Starting with Ansible 2.19 and the ansible.windows collection at 3.1.0, Ansible can now run on Windows hosts with WDAC enabled.

Experimental functionality

The App Control implementation is considered an experimental feature and can change in future releases. It is not possible to ensure all PowerShell modules will work with App Control enabled and that a module might enable arbitrary code to run in a way not typically allowed by App Control. It is recommended to test all modules with WDAC enabled before using them in production.

Requirements for Ansible to work with App Control

How to Sign Ansible Content

Known Module Differences

Ansible requires the target Windows version to be Windows Server 2019 or Windows 10 Build 1803 or later. This is because the Dynamic Code Security feature added in that Windows version is required to allow Ansible to run tasks on the Windows host.

The first step towards enabling App Control is to create a code signing certificate that will be used to sign the scripts used by Ansible. While this certificate can be self signed, it is recommended that it is issued by a trusted certificate authority used in your organization. How to generate this certificate is outside the scope of this documentation. Once the certificate is setup, the policy file must be generated and applied to the Windows host.

Setting up App Control and configuring policies is not covered under the documentation here. Please read through the Microsoft documentation for Application Control for Windows or Application Control with PowerShell to understand how to configure App Control and set up policies. The App Control for Business Wizard is a tool that can simplify policy generation through a more user friendly GUI.

When setting up a policy it is recommended to configure Ansible as a supplemental policy so it can be easily modified and applied where Ansible will be used. Whether you use a supplemental or just a base policy for trusting the certificate used by Ansible, the base policy must have the following options set:

User Mode Code Integrity (0 Enabled:UMCI) is enabled

Disable Script Enforcement (11 Disabled:Script Enforcement) is not enabled

Dynamic Code Security (19 Enabled:Dynamic Code Security) is enabled

The policy then should then add the certificate as a trusted publisher to the User Mode Signing Scenario, for example this is an example policy configuration that contains a trusted publisher:

Once the policy is created and the certificate that will be used to sign the Ansible content is trusted by the Windows host, the policy can be applied.

As Ansible typically runs tasks as an Administrator, it is important that the policy is signed and is applied so that Ansible cannot unset the policy through a task like win_file or win_regedit.

Once the code signing certificate has been generated and trusted by the Windows host, it can be used to sign the scripts that Ansible will run. The PowerShell script New-AnsiblePowerShellSignature.ps1 can be used to sign both the execution wrapper used by Ansible to invoke modules and any PowerShell modules inside an Ansible collection. It requires the following to run:

PowerShell 7.4 or later

The OpenAuthenticode PowerShell module

Python with Ansible and the required collections installed

Access to the certificate and private key trusted by the App Control policy, typically as a PFX file

The New-AnsiblePowerShellSignature function is not officially supported and is marked as a tech preview.

To sign the Ansible PowerShell wrapper scripts, and modules in a collection, the following PowerShell script can be used with the loaded function from above:

The ansible.builtin collection refers to the builtin execution scripts used in Ansible. Any other collection with PowerShell modules used in the playbook should be added to the -Collection parameter. The script will generate the powershell_signatures.psd1 script signed by the certificate and contains the hashes of all the modules in the collection that should be trusted to run. It will also generate the signature for Ansible’s execution wrapper script in the Ansible installation directory so that Ansible can automatically run the script trusted by the App Control policy. The current behavior of New-AnsiblePowerShellSignature is to sign all the modules in the collection and the Ansible execution wrapper script even if they could include an escape hatch. It is recommended to skip any modules using the -Skip parameter that are not needed in the playbook, for example:

Any PowerShell content that is not part of a collection, like custom scripts or code used in ansible.windows.win_powershell, must be signed manually using the Set-AuthenticodeSignature cmdlet on Windows or Set-OpenAuthenticodeSignature through OpenAuthenticode module on Linux. It is important that these signed scripts are used in a way that will not modify the contents of the script or else the signature will be invalidated. For example the ansible.builtin.script module will copy the script file to the target host as is leaving the signature intact but using the ansible.builtin.file lookup will strip any remaining newline characters unless the rstrip=False option is used.

When App Control is enabled, some modules may not work, or behave differently, even if signed. Some of the known differences are:

ansible.windows.win_command can only execute executables trusted by the App Control policy. If the executable is not trusted, the module will fail

ansible.windows.win_shell will run all code in Constrained Language Mode (CLM) which is highly restricted and may cause some scripts to fail

ansible.windows.win_powershell will run in CLM by default unless the provided script is signed

ansible.builtin.script will run in CLM by default unless the provided script is signed

ansible.windows.win_package can only run executables trusted by the App Control policy so may or may not work depending on the executable

ansible.windows.win_updates is currently not supported and will not work

Other modules that start sub-processes or rely on unsigned PowerShell content will most likely not work with App Control enabled.

If trying to run a PowerShell script with ansible.windows.win_powershell or ansible.builtin.script, the script itself must be signed or else it will be run in CLM.

It is important that when referencing a signed script that the script is not modified in any way. This means the line endings and whitespace that were present when it was signed must be the same when Ansible uses the signed script.

Ansible will always load the script with the UTF-8 encoding even if no Byte Order Mark (BOM) is present. It is important that the script was encoded with UTF-8 without a BOM when it was signed so that the signature stays valid. If the script was signed with a different encoding, the signature could be invalidated or PowerShell may interpret it with different characters.

When referencing a signed script in Ansible, it is important that it is used in a way that does not modify the contents of the script which would break the signature. For example you should have the signed script in the local files directory associated with the playbook/tasks and reference in one of the following ways:

**Examples:**

Example 1 (unknown):
```unknown
<SiPolicy>
   ...
   <Signers>
      <Signer Name="Some Signer" ID="ID_SIGNER_S_0">
         <CertRoot Type="TBS" Value="1DBF60AFC6313593EDB09B6C6239BE493FF3461D4BD6D0A8C6E1723A12C06438F471BB7F6BAA73BD142D0698CEFF9DBB" />
         <CertPublisher Value="Some Publisher" />
      </Signer>
   </Signers>
   <SigningScenarios>
      <SigningScenario ID="ID_SIGNINGSCENARIO_KMCI" FriendlyName="Kernel Mode Signing Scenario" Value="131">
         <ProductSigners />
      </SigningScenario>
      <SigningScenario ID="ID_SIGNINGSCENARIO_UMCI" FriendlyName="User Mode Signing Scenario" Value="12">
         <ProductSigners>
         <AllowedSigners>
            <AllowedSigner SignerId="ID_SIGNER_S_0" />
         </AllowedSigners>
         </ProductSigners>
      </SigningScenario>
   </SigningScenarios>
   ...
</SiPolicy>
```

Example 2 (unknown):
```unknown
$certPassword = Read-Host "Enter the password for the certificate" -AsSecureString
$cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
   "wdac-cert.pfx"
   $certPassword)

$signingParams = @{
   Certificate = $cert

   Collection = @(
      # Includes all the builtin execution wrappers and scripts needed for Ansible
      'ansible.builtin'

      # Add any remaining collections used in the playbook like microsoft.ad, community.windows, etc.
      'ansible.windows'
      'microsoft.ad'
      'microsoft.iis'
      'community.windows'
   )

   # The URL of the Authenticode timestamp server to use for timestamping
   # the signature.
   # https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures
   TimeStampServer = '...'
}
New-AnsiblePowerShellSignature @signingParams -Verbose
```

Example 3 (unknown):
```unknown
New-AnsiblePowerShellSignature ... -Skip @(
    'ansible.windows.win_dsc'
    'ansible.windows.win_timezone'
)
```

Example 4 (unknown):
```unknown
- name: Test out LanguageMode
  ansible.windows.win_powershell:
    script: $ExecutionContext.SessionState.LanguageMode
```

---

## Desired State Configuration — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_dsc.html

**Contents:**
- Desired State Configuration
- What is Desired State Configuration?
- Host Requirements
- Why Use DSC?
- How to Use DSC?
  - Property Types
    - PSCredential
    - CimInstance Type
    - HashTable Type
    - Arrays

What is Desired State Configuration?

Finding Custom DSC Resources

Installing a Custom Resource

Desired State Configuration, or DSC, is a tool built into PowerShell that can be used to define a Windows host setup through code. The overall purpose of DSC is the same as Ansible, it is just executed differently. Since Ansible 2.4, the win_dsc module has been added and can be used to take advantage of existing DSC resources when interacting with a Windows host.

More details on DSC can be viewed at DSC Overview.

To use the win_dsc module, a Windows host must have PowerShell v5.0 or newer installed. All supported hosts can be upgraded to PowerShell v5.

Once the PowerShell requirements have been met, using DSC is as simple as creating a task with the win_dsc module.

DSC and Ansible modules have a common goal which is to define and ensure the state of a resource. Because of this, resources like the DSC File resource and Ansible win_file can be used to achieve the same result. Deciding which to use depends on the scenario.

Reasons for using an Ansible module over a DSC resource:

The host does not support PowerShell v5.0, or it cannot easily be upgraded

The DSC resource does not offer a feature present in an Ansible module. For example, win_regedit can manage the REG_NONE property type, while the DSC Registry resource cannot

DSC resources have limited check mode support, while some Ansible modules have better checks

DSC resources do not support diff mode, while some Ansible modules do

Custom resources require further installation steps to be run on the host beforehand, while Ansible modules are built-in to Ansible

There are bugs in a DSC resource where an Ansible module works

Reasons for using a DSC resource over an Ansible module:

The Ansible module does not support a feature present in a DSC resource

There is no Ansible module available

There are bugs in an existing Ansible module

In the end, it doesn’t matter whether the task is performed with DSC or an Ansible module; what matters is that the task is performed correctly and the playbooks are still readable. If you have more experience with DSC over Ansible and it does the job, just use DSC for that task.

The win_dsc module takes in a free-form of options so that it changes according to the resource it is managing. A list of built-in resources can be found at resources.

Using the Registry resource as an example, this is the DSC definition as documented by Microsoft:

When defining the task, resource_name must be set to the DSC resource being used - in this case, the resource_name should be set to Registry. The module_version can refer to a specific version of the DSC resource installed; if left blank it will default to the latest version. The other options are parameters that are used to define the resource, such as Key and ValueName. While the options in the task are not case sensitive, keeping the case as-is is recommended because it makes it easier to distinguish DSC resource options from Ansible’s win_dsc options.

This is what the Ansible task version of the above DSC Registry resource would look like:

Starting in Ansible 2.8, the win_dsc module automatically validates the input options from Ansible with the DSC definition. This means Ansible will fail if the option name is incorrect, a mandatory option is not set, or the value is not a valid choice. When running Ansible with a verbosity level of 3 or more (-vvv), the return value will contain the possible invocation options based on the resource_name specified. Here is an example of the invocation output for the above Registry task:

The invocation.module_args key shows the actual values that were set as well as other possible values that were not set. Unfortunately, this will not show the default value for a DSC property, only what was set from the Ansible task. Any *_password option will be masked in the output for security reasons; if there are any other sensitive module options, set no_log: True on the task to stop all task output from being logged.

Each DSC resource property has a type that is associated with it. Ansible will try to convert the defined options to the correct type during execution. For simple types like [string] and [bool], this is a simple operation, but complex types like [PSCredential] or arrays (like [string[]]) require certain rules.

A [PSCredential] object is used to store credentials in a secure way, but Ansible has no way to serialize this over JSON. To set a DSC PSCredential property, the definition of that parameter should have two entries that are suffixed with _username and _password for the username and password, respectively. For example:

On versions of Ansible older than 2.8, you should set no_log: true on the task definition in Ansible to ensure any credentials used are not stored in any log file or console output.

A [PSCredential] is defined with EmbeddedInstance("MSFT_Credential") in a DSC resource MOF definition.

A [CimInstance] object is used by DSC to store a dictionary object based on a custom class defined by that resource. Defining a value that takes in a [CimInstance] in YAML is the same as defining a dictionary in YAML. For example, to define a [CimInstance] value in Ansible:

In the above example, the CIM instance is a representation of the class DSC_WebAuthenticationInformation. This class accepts four boolean variables, Anonymous, Basic, Digest, and Windows. The keys to use in a [CimInstance] depend on the class it represents. Please read through the documentation of the resource to determine the keys that can be used and the types of each key value. The class definition is typically located in the <resource name>.schema.mof.

A [HashTable] object is also a dictionary but does not have a strict set of keys that can/need to be defined. Like a [CimInstance], define it as a normal dictionary value in YAML. A [HashTable]] is defined with EmbeddedInstance("MSFT_KeyValuePair") in a DSC resource MOF definition.

Simple type arrays like [string[]] or [UInt32[]] are defined as a list or as a comma-separated string which is then cast to their type. Using a list is recommended because the values are not manually parsed by the win_dsc module before being passed to the DSC engine. For example, to define a simple type array in Ansible:

Complex type arrays like [CimInstance[]] (array of dicts), can be defined like this example:

The above example is an array with two values of the class DSC_WebBindingInformation. When defining a [CimInstance[]], be sure to read the resource documentation to find out what keys to use in the definition.

A [DateTime] object is a DateTime string representing the date and time in the ISO 8601 date time format. The value for a [DateTime] field should be quoted in YAML to ensure the string is properly serialized to the Windows host. Here is an example of how to define a [DateTime] value in Ansible:

All the values above are equal to a UTC date time of February 22nd 2019 at 1:57pm with 31 seconds and 2311892 milliseconds.

By default, DSC runs each resource as the SYSTEM account and not the account that Ansible uses to run the module. This means that resources that are dynamically loaded based on a user profile, like the HKEY_CURRENT_USER registry hive, will be loaded under the SYSTEM profile. The parameter PsDscRunAsCredential is a parameter that can be set for every DSC resource, and force the DSC engine to run under a different account. As PsDscRunAsCredential has a type of PSCredential, it is defined with the _username and _password suffix.

Using the Registry resource type as an example, this is how to define a task to access the HKEY_CURRENT_USER hive of the Ansible user:

DSC resources are not limited to the built-in options from Microsoft. Custom modules can be installed to manage other resources that are not usually available.

You can use the PSGallery to find custom resources, along with documentation on how to install them on a Windows host.

The Find-DscResource cmdlet can also be used to find custom resources. For example:

DSC resources developed by Microsoft that start with x means the resource is experimental and comes with no support.

There are three ways that a DSC resource can be installed on a host:

Manually with the Install-Module cmdlet

Using the win_psmodule Ansible module

Saving the module manually and copying it to another host

The following is an example of installing the xWebAdministration resources using win_psmodule:

Once installed, the win_dsc module will be able to use the resource by referencing it with the resource_name option.

The first two methods above only work when the host has access to the internet. When a host does not have internet access, the module must first be installed using the methods above on another host with internet access and then copied across. To save a module to a local file path, the following PowerShell cmdlet can be run:

This will create a folder called xWebAdministration in C:\temp, which can be copied to any host. For PowerShell to see this offline resource, it must be copied to a directory set in the PSModulePath environment variable. In most cases, the path C:\Program Files\WindowsPowerShell\Module is set through this variable, but the win_path module can be used to add different paths.

An introduction to playbooks

Tips and tricks for playbooks

Windows-specific module list, all implemented in PowerShell

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
Registry [string] #ResourceName
{
    Key = [string]
    ValueName = [string]
    [ Ensure = [string] { Enable | Disable }  ]
    [ Force =  [bool]   ]
    [ Hex = [bool] ]
    [ DependsOn = [string[]] ]
    [ ValueData = [string[]] ]
    [ ValueType = [string] { Binary | Dword | ExpandString | MultiString | Qword | String }  ]
}
```

Example 2 (unknown):
```unknown
- name: Use win_dsc module with the Registry DSC resource
  win_dsc:
    resource_name: Registry
    Ensure: Present
    Key: HKEY_LOCAL_MACHINE\SOFTWARE\ExampleKey
    ValueName: TestValue
    ValueData: TestData
```

Example 3 (javascript):
```javascript
changed: [2016] => {
    "changed": true,
    "invocation": {
        "module_args": {
            "DependsOn": null,
            "Ensure": "Present",
            "Force": null,
            "Hex": null,
            "Key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\ExampleKey",
            "PsDscRunAsCredential_password": null,
            "PsDscRunAsCredential_username": null,
            "ValueData": [
                "TestData"
            ],
            "ValueName": "TestValue",
            "ValueType": null,
            "module_version": "latest",
            "resource_name": "Registry"
        }
    },
    "module_version": "1.1",
    "reboot_required": false,
    "verbose_set": [
        "Perform operation 'Invoke CimMethod' with following parameters, ''methodName' = ResourceSet,'className' = MSFT_DSCLocalConfigurationManager,'namespaceName' = root/Microsoft/Windows/DesiredStateConfiguration'.",
        "An LCM method call arrived from computer SERVER2016 with user sid S-1-5-21-3088887838-4058132883-1884671576-1105.",
        "[SERVER2016]: LCM:  [ Start  Set      ]  [[Registry]DirectResourceAccess]",
        "[SERVER2016]:                            [[Registry]DirectResourceAccess] (SET) Create registry key 'HKLM:\\SOFTWARE\\ExampleKey'",
        "[SERVER2016]:                            [[Registry]DirectResourceAccess] (SET) Set registry key value 'HKLM:\\SOFTWARE\\ExampleKey\\TestValue' to 'TestData' of type 'String'",
        "[SERVER2016]: LCM:  [ End    Set      ]  [[Registry]DirectResourceAccess]  in 0.1930 seconds.",
        "[SERVER2016]: LCM:  [ End    Set      ]    in  0.2720 seconds.",
        "Operation 'Invoke CimMethod' complete.",
        "Time taken for configuration job to complete is 0.402 seconds"
    ],
    "verbose_test": [
        "Perform operation 'Invoke CimMethod' with following parameters, ''methodName' = ResourceTest,'className' = MSFT_DSCLocalConfigurationManager,'namespaceName' = root/Microsoft/Windows/DesiredStateConfiguration'.",
        "An LCM method call arrived from computer SERVER2016 with user sid S-1-5-21-3088887838-4058132883-1884671576-1105.",
        "[SERVER2016]: LCM:  [ Start  Test     ]  [[Registry]DirectResourceAccess]",
        "[SERVER2016]:                            [[Registry]DirectResourceAccess] Registry key 'HKLM:\\SOFTWARE\\ExampleKey' does not exist",
        "[SERVER2016]: LCM:  [ End    Test     ]  [[Registry]DirectResourceAccess] False in 0.2510 seconds.",
        "[SERVER2016]: LCM:  [ End    Set      ]    in  0.3310 seconds.",
        "Operation 'Invoke CimMethod' complete.",
        "Time taken for configuration job to complete is 0.475 seconds"
    ]
}
```

Example 4 (unknown):
```unknown
PsDscRunAsCredential_username: '{{ ansible_user }}'
PsDscRunAsCredential_password: '{{ ansible_password }}'

SourceCredential_username: AdminUser
SourceCredential_password: PasswordForAdminUser
```

---

## Windows SSH — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_ssh.html

**Contents:**
- Windows SSH
- SSH Setup
  - Default Shell Configuration
- Ansible Configuration
- SSH Authentication
  - Key Authentication
  - GSSAPI Authentication
  - Password Authentication

On newer Windows versions, you can use SSH to connect to a Windows host. This is an alternative connection option to WinRM.

While Ansible could use the SSH connection plugin with Windows nodes since Ansible 2.8, official support was only added in version 2.18.

Default Shell Configuration

Ansible Configuration

GSSAPI Authentication

Password Authentication

Microsoft provides an OpenSSH implementation with Windows since Windows Server 2019 as a Windows capability. It can also be installed through an upstream package under Win32-OpenSSH. Ansible officially only supports the OpenSSH implementation shipped with Windows, not the upstream package. The OpenSSH version must be version 7.9.0.0 at a minimum. This effectively means official support starts with Windows Server 2022 because Server 2019 ships with version 7.7.2.1. Using older Windows versions or the upstream package might work but is not supported.

To install the OpenSSH feature on Windows Server 2022 and later, use the following PowerShell command:

By default, OpenSSH on Windows uses cmd.exe as the default shell. While Ansible can work with this default shell it is recommended to change this to powershell.exe as it is better tested and should be faster than having cmd.exe as the default. To change the default shell you can use the following PowerShell script:

The new default shell setting will apply to the next SSH connection, there is no need to restart the sshd service. You can also use Ansible to configure the default shell:

The meta: reset_connection is important to ensure the subsequent tasks will use the new default shell.

To configure Ansible to use SSH for Windows hosts, you must set two connection variables:

set ansible_connection to ssh

set ansible_shell_type to powershell or cmd

The ansible_shell_type variable should reflect the DefaultShell configured on the Windows host. Other SSH options as documented under the ssh can also be set for the Windows host.

Win32-OpenSSH authentication with Windows is similar to SSH authentication on Unix/Linux hosts. While there are many authentication methods that can be used there are typically three used on Windows:

Active Directory Accounts

Credential Delegation

In most cases it is recommended to use key or GSSAPI authentication over password authentication.

SSH key authentication on Windows works in the same way as SSH key authentication for POSIX nodes. You can generate a key pair using the ssh-keygen command and add the public key to the authorized_keys file in the user’s profile directory. The private key should be kept secure and not shared.

One difference is that the authorized_keys file for admin users is not located in the .ssh folder in the user’s profile directory but in C:\ProgramData\ssh\administrators_authorized_keys. It is possible to change the location of the authorized_keys file for admin users back to the user profile directory by removing, or commenting, the lines in C:\ProgramData\ssh\sshd_config and restarting the sshd service.

SSH keys work with both local and domain accounts but suffer from the double-hop issue. This means that when using SSH key authentication with Ansible, the remote session will not have access to user credentials and will fail when attempting to access a network resource. To work around this problem, you can use become on the task with the credentials of the user that needs access to the remote resource.

GSSAPI authentication will use Kerberos to authenticate the user with the Windows host. To use GSSAPI authentication with Ansible, the Windows server must be configured to allow GSSAPI authentication by editing the C:\ProgramData\ssh\sshd_config file. Either add in the following line or edit the existing line:

Once edited restart the sshd service with Restart-Service -Name sshd.

On the Ansible control node, you need to have Kerberos installed and configured with the domain the Windows host is a member of. How to set this up and configure is outside the scope of this document. Once the Kerberos realm is configured you can use the kinit command to get a ticket for the user you are connecting with and klist to verify what tickets are available:

Once you have a valid ticket you can use the ansible_user hostvar to specify the UPN username and Ansible will automatically use the Kerberos ticket for that user when using SSH.

It is also possible to enable unconstrained delegation through GSSAPI authentication to have the Windows node access network resources. For GSSAPI delegation to work the ticket retrieved by kinit must be forwardable and ssh must be called with the -o GSSAPIDelegateCredentials=yes option. To retrieve a forwardable ticket either use the -f flag with kinit or add forwardable = true under [libdefaults] in the /etc/krb5.conf file.

The GSSAPIDelegateCredentials=yes option can either be set in the ~/.ssh/config file or as a hostvar variable in the inventory:

Unlike the psrp or winrm connection plugins, the SSH connection plugin cannot get a Kerberos TGT ticket when provided with an explicit username and password. This means that the user must have a valid Kerberos ticket before running the playbook.

See Kerberos Authentication for more information on how to configure, use, and troubleshoot Kerberos authentication.

Password authentication is the least secure method of authentication and is not recommended. However, it is possible to use password authentication with Windows SSH. To use password authentication with Ansible, set the ansible_password variable in the inventory file or in the playbook. Using password authentication requires the sshpass package to be installed on the Ansible control node.

Password authentication works like WinRM CredSSP authentication where the username and password is given to the Windows host and it will perform unconstrained delegation to access network resources.

**Examples:**

Example 1 (unknown):
```unknown
Get-WindowsCapability -Name OpenSSH.Server* -Online |
    Add-WindowsCapability -Online
Set-Service -Name sshd -StartupType Automatic -Status Running

$firewallParams = @{
    Name        = 'sshd-Server-In-TCP'
    DisplayName = 'Inbound rule for OpenSSH Server (sshd) on TCP port 22'
    Action      = 'Allow'
    Direction   = 'Inbound'
    Enabled     = 'True'  # This is not a boolean but an enum
    Profile     = 'Any'
    Protocol    = 'TCP'
    LocalPort   = 22
}
New-NetFirewallRule @firewallParams

$shellParams = @{
    Path         = 'HKLM:\SOFTWARE\OpenSSH'
    Name         = 'DefaultShell'
    Value        = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
    PropertyType = 'String'
    Force        = $true
}
New-ItemProperty @shellParams
```

Example 2 (unknown):
```unknown
# Set default to powershell.exe
$shellParams = @{
    Path         = 'HKLM:\SOFTWARE\OpenSSH'
    Name         = 'DefaultShell'
    Value        = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
    PropertyType = 'String'
    Force        = $true
}
New-ItemProperty @shellParams

# Set default back to cmd.exe
Remove-ItemProperty -Path HKLM:\SOFTWARE\OpenSSH -Name DefaultShell
```

Example 3 (unknown):
```unknown
- name: set the default shell to PowerShell
  ansible.windows.win_regedit:
    path: HKLM:\SOFTWARE\OpenSSH
    name: DefaultShell
    data: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
    type: string
    state: present

- name: reset SSH connection after shell change
  ansible.builtin.meta: reset_connection

- name: set the default shell to cmd
  ansible.windows.win_regedit:
    path: HKLM:\SOFTWARE\OpenSSH
    name: DefaultShell
    state: absent

- name: reset SSH connection after shell change
  ansible.builtin.meta: reset_connection
```

Example 4 (unknown):
```unknown
Match Group administrators
    AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
```

---

## Kerberos Authentication — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_winrm_kerberos.html

**Contents:**
- Kerberos Authentication
- Installing Kerberos
- Configuring Host Kerberos
- Verifying Kerberos Configuration
- Ticket Management
- Delegation
- Troubleshooting Kerberos

Kerberos authentication is a modern method used in Windows environments for authentication. It allows both the client and server to verify each others identities and supports modern encryption methods like AES.

Configuring Host Kerberos

Verifying Kerberos Configuration

Troubleshooting Kerberos

Kerberos is provided through a GSSAPI library which is part of a system package. Some distributions install the Kerberos packages by default but others may require manual installation.

To install the Kerberos libraries on a RHEL/Fedora based system:

For a Debian/Ubuntu based system:

For an Arch Linux based system:

For a FreeBSD based system:

The python3-devel / python3-dev packages can be ignored if using Kerberos with the ssh connection plugin. They are only needed if using a WinRM based connection with Kerberos authentication.

Once installed the kinit, klist, and krb5-config packages will be available. You can test them out with the following command:

The psrp and winrm connection plugins require extra Python libraries for Kerberos authentication. The following step can be skipped if using Kerberos with the ssh connection.

If you chose the pipx install instructions for Ansible, you can install those requirements by running the following:

Or, if you chose the pip install instructions:

Once the dependencies have been installed, Kerberos needs to be configured so that it can communicate with a domain. Most Kerberos implementations can either find a domain using DNS or through manual configuration in the /etc/krb5.conf file. For details on what can be set in the /etc/krb5.conf file see krb5.conf for more details. A simple krb5.conf file that uses DNS to lookup the KDC would be:

With the above configuration when a Kerberos ticket is requested for the server server.my.domain.com the Kerberos library will do an SRV lookup for _kerberos._udp.my.domain.com and _kerberos._tcp.my.domain.com to find the KDC. If you wish to manually set the KDC realms you can use the following configuration:

With this configuration any request for a ticket with the DNS suffix .my.domain.com and my.domain.com itself will be sent to the KDC domain-controller1.my.domain.com with a fallback to domain-controller2.my.domain.com.

More information on how the Kerberos library attempts to find the KDC can be found in the MIT Kerberos Documentation.

The information in this section assumes you are using the MIT Kerberos implementation which is typically the default on most Linux distributions. Some platforms like FreeBSD or macOS use a different GSSAPI implementation called Heimdal which acts in a similar way to MIT Kerberos but some behaviors may be different.

To verify that Kerberos is working correctly, you can use the kinit command to obtain a ticket for a user in the domain. The following command will request a ticket for the user username in the domain MY.DOMAIN.COM:

If the password is correct, the command will return without any output. To verify that the ticket has been obtained, you can use the klist command:

If successful, this validates that the Kerberos configuration is correct and that the user can obtain a Ticket Granting Ticket (TGT) from the KDC. If kinit is unable to find the KDC for the requested realm, verify your Kerberos configuration by ensuring DNS can locate the KDC using the SRV records or that the KDC is manually mapped in the krb5.conf.

On MIT Kerberos based systems, you can use the kvno command to verify that you are able to retrieve a service ticket for a particular service. For example, if you are using a WinRM based connection to authenticate with server.my.domain.com you can use the following command to verify that your TGT is able to get a service ticket for the target server:

The klist command can also be used to verify the ticket was stored in the Kerberos cache:

In the above example we have the TGT stored under the krbtgt service principal and our http/server.my.domain.com under its own service principal.

The kdestroy command can be used to remove the ticket cache.

For Kerberos authentication to work with Ansible, a Kerberos TGT for a user must be present so that Ansible can request a service ticket for the target server. Some connection plugins like ssh require the TGT to already be present and accessible to the Ansible control process. Other connection plugins, like psrp and winrm, can automatically obtain a TGT for the user if the user’s password is provided in the inventory.

To retrieve a TGT manually for a user, run the kinit command with the user’s username and domain as shown in Verifying Kerberos Configuration. This TGT will be used automatically when Kerberos authentication is requested by the connection plugin in Ansible.

If you are using the psrp or winrm connection plugin and the user’s password is provided in the inventory, the connection plugin will automatically obtain a TGT for the user. This is done by running the kinit command with the user’s username and password. The TGT will be stored in a temporary credential cache and will be used for the task.

Kerberos delegation allows the credentials to traverse multiple hops. This is useful when you need to authenticate to a server and then have that server authenticate to another server on your behalf. To enable delegation, you must:

request a forwardable TGT when obtaining a ticket with kinit

request the connection plugin to allow delegation to the server

the AD user is not marked as sensitive and cannot be delegated and is not a member of the Protected Users group

depending on the krb5.conf configuration, the target server may need to allow unconstrained delegation through its AD object delegation settings

the target resource to delegate to must be accessible with Kerberos authentication

To request a forwardable TGT, either add the -f flag to the kinit command or set the forwardable = true option in the [libdefaults] section of the krb5.conf file. If you are using the psrp or winrm connection plugin to retrieve the TGT from the user’s password in the inventory, it will automatically request a forwardable TGT if the connection plugin is configured to use delegation.

To have the connection plugin delegate the credentials it will need to set the following hostvar in the inventory:

It is also possible to set GSSAPIDelegateCredentials yes in the ~/.ssh/config file to allow delegation for all SSH connections.

To verify if a user is allowed to delegate their credentials, you can run the following PowerShell script on a Windows host in the same domain:

Newer versions of MIT Kerberos have added a configuration option enforce_ok_as_delegate in the [libdefaults] section of the krb5.conf file. If this option is set to true delegation will only work if the target server account allows unconstrained delegation. To check or set unconstrained delegation on a Windows computer host, you can use the following PowerShell script:

To verify that delegation is working, you can use the klist.exe command on the Windows node to verify that the ticket has been forwarded. The output should show the ticket server is for krbtgt/MY.DOMAIN.COM @ MY.CDOMAIN.COM and the ticket flags contained forwarded.

If anything goes wrong, the output for klist.exe will not have the forwarded flag and the server will be for the target server principal and not krbtgt.

It is also important to ensure that the target resource to delegate to will work with Kerberos authentication. This means that the target server must have a Service Principal Name (SPN) registered in Active Directory (AD) and that the outbound authentication attempt on Windows uses the hostname and not an IP address/alias. For example, you should access a fileshare using the path \\server.fqdn.com\share and not \\192.168.1.2\share. To verify that an SPN is registered and the session Ansible runs under can delegate using Kerberos, you can use the following klist.exe command to request a service ticket for the target server.

The SPN prefix for the target server depends on the service you are trying to access. The cifs service if used for file shares, http for web services, and so on. Make sure to use the correct prefix for testing our Kerberos delegation.

Kerberos is reliant on a properly configured environment to work. Some common issues that can cause Kerberos authentication to fail are:

The hostname set for the Windows host is an alias or an IP address

The time on the Ansible control node is not synchronized with the AD domain controller

The KDC realm is not set correctly in the krb5.conf file or cannot be resolved through DNS

If using the MIT Kerberos implementation, you can set the environment variable KRB5_TRACE=/dev/stdout to get more detailed information on what the Kerberos library is doing. This can be useful for debugging issues with the Kerberos library such as the KDC lookup behavior, time sync issues, and server name lookup failures.

**Examples:**

Example 1 (unknown):
```unknown
$ sudo dnf install krb5-devel krb5-libs krb5-workstation python3-devel
```

Example 2 (unknown):
```unknown
$ sudo apt-get install krb5-user libkrb5-dev python3-dev
```

Example 3 (unknown):
```unknown
$ sudo pacman -S krb5
```

Example 4 (unknown):
```unknown
$ sudo pkg install heimdal
```

---

## Managing z/OS UNIX hosts with Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/intro_zos.html

**Contents:**
- Managing z/OS UNIX hosts with Ansible
- Ansible and z/OS UNIX System Services
- The z/OS landscape
- Using ansible.builtin modules with z/OS UNIX
- Configure the remote environment
- Configure the remote Python interpreter
- Configure the remote shell
- Enable Ansible pipelining
- Unreadable characters
- Using z/OS as a control node

Ansible can connect to IBM z/OS UNIX System Services to bring your Ansible Automation strategy to IBM z/OS. This enables development and operations automation on IBM Z through a seamless, unified workflow orchestration with configuration management, provisioning, and application deployment with Ansible.

UNIX System Services can support the required dependencies for an Ansible managed node including running Python and spawning interactive shell processes through SSH connections. Ansible can target UNIX System Services nodes to modify files, directories, and so on, through ansible.builtin modules. Further, anything that one can do by typing command(s) into the UNIX System Services shell can be captured and automated in an Ansible playbook.

While most systems process files in two modes - binary or text encoded in UTF-8, IBM z/OS including UNIX System Services features an additional third mode - text encoded in EBCDIC. Ansible has provisions to handle binary data and UTF-8 encoded textual data, but not EBCDIC encoded data. This is not necessarily a limitation, it simply requires additional tasks that convert files to and from their original encodings. It is up to the Ansible user managing z/OS UNIX nodes to understand the nature of the files in their automation.

The type (binary or text) and encoding of files can be stored in file “tags”. File tags is a z/OS UNIX System Services concept (part of Enhanced ASCII) designed to distinguish binary files from UTF-8 encoded text files and EBCDIC-encoded text files.

Default behavior for an un-tagged file or stream is determined by the program, for example, IBM Open Enterprise SDK for Python defaults to the UTF-8 encoding.

Ansible modules will not read or recognize file tags. It is up to the user to determine the nature of remote data and tag it appropriately. Data sent to remote z/OS UNIX hosts through Ansible is, by default, encoded in UTF-8 and not tagged. Tagging a file is achievable with an additional task using the ansible.builtin.command module.

The z/OS shell available on z/OS UNIX System Services defaults to an EBCDIC encoding for un-tagged data streams. Ansible sends untagged UTF-8 encoded textual data to the z/OS shell which expects untagged data to be encoded in EBCDIC. This mismatch in data encodings can be resolved by setting the PYTHONSTDINENCODING environment variable, which causes the pipe used by Python to be tagged with the specified encoding. File and pipe tags can be used with automatic conversion between ASCII and EBCDIC, but only programs on z/OS UNIX which are aware of tags will use them.

The ansible.builtin modules operate under the assumption that all textual data (files and pipes/streams) is UTF-8 encoded. On z/OS, since textual data (file or stream) is sometimes encoded in EBCDIC and sometimes in UTF-8, special care must be taken to identify the correct encoding of target data.

Here are some notes / pro-tips when using the ansible.builtin modules with z/OS UNIX. This is by no means a comprehensive list. Before using any Ansible modules, you must first Configure the remote environment.

The command and shell modules are excellent for automating tasks for which command line solutions already exist. The thing to keep in mind when using these modules is that depending on the system configuration, the z/OS shell (/bin/sh) may return output in EBCDIC. The LE environment variable configurations will correctly convert streams if they are tagged and return readable output to Ansible. However, some command line programs may return output in UTF-8 and not tag the pipe. In this case, the autoconversion may incorrectly assume output is in EBCDIC and attempt to convert it and yield unreadable data. If the source encoding is known, you can use the ansible.builtin.shell module’s capability to chain commands together through pipes, and pipe the output to iconv. In this example, you may need to select other encodings for the ‘to’ and ‘from’ that represent your file encodings.

The raw module, by design, ignores all remote environment settings. However, z/OS UNIX System Services managed nodes require some base configurations. To use this module with UNIX System Services, configure the minimum environment variables as a chain of export statements before the desired command.

Alternatively, consider using the ansible.builtin.command or ansible.builtin.shell modules mentioned above, which set up the configured remote environment for each task.

The ansible.builtin modules will NOT automatically tag files, nor will existing file tags be honored nor preserved. You can treat files as binaries when running copy/fetch operations, there is no issue in terms of data integrity, but remember to restore the file tag once the file is returned to z/OS UNIX, as tags are not preserved. Use the command module to set the file tag:

These modules process all data in UTF-8. Ensure target files are UTF-8 encoded beforehand and re-tag the files afterwards.

The built in script module copies a local script file to a temp file on the remote target and runs it. The issue that z/OS UNIX System Services targets run into is that when the underlying z/OS shell attempts to read the script file, since the file does not get tagged as UTF-8 text, the shell assumes that the file is encoded in EBCDIC, and fails to correctly read or run the script. One work-around is to manually copy local files to managed nodes (ansible.builtin.copy ) and convert or tag files (with the ansible.builtin.command module). With this work-around, some of the conveniences of the script module are lost, such as automatically cleaning up the script file once it is run, but it is trivial to perform those steps as additional playbook tasks.

Another work-around is to store local script files in EBCDIC. They may be unreadable on the ansible control node, but they will copy correctly to z/OS UNIX System Services targets in EBCDIC, and the script will run. This approach takes advantage of the built-in conveniences of the script module, but managing unreadable EBCDIC files locally makes maintaining those script files more difficult.

Certain Language Environment (LE) configurations enable automatic encoding conversion and automatic file tagging functionality required by Python on z/OS UNIX systems (IBM Open Enterprise SDK for Python ).

Include the following configurations when setting the remote environment for any z/OS UNIX managed nodes:

Ansible can be configured with remote environment variables in these options:

inventory - inventory.yml, group_vars/all.yml, or host_vars/all.yml

playbook - environment variable at top of playbook.

block or task - environment key word.

For more details, see Setting the remote environment.

Ansible requires a Python interpreter to run most modules on the remote host, and it checks for Python at the ‘default’ path /usr/bin/python.

On z/OS UNIX, the Python3 interpreter (from IBM Open Enterprise SDK for Python) is often installed to a different path, typically something like: /usr/lpp/cyp/v3r12/pyz.

The path to the Python interpreter can be configured with the Ansible inventory variable ansible_python_interpreter. For example:

When the path to the Python interpreter is not found in the default location on the target host, an error containing the following message may result: /usr/bin/python: FSUM7351 not found

For more details, see: How do I handle not having a Python interpreter at /usr/bin/python on a remote machine?.

The z/OS UNIX System Services managed node includes several shells. Currently the only supported shell is the z/OS Shell located in path /bin/sh. To configure which shell the Ansible control node uses on the target node, set inventory variable ansible_shell_executable. For example:

Enable ANSIBLE_PIPELINING in the ansible.cfg file.

When Ansible pipelining is enabled, Ansible passes any module code to the remote target node through Python’s stdin pipe and runs it in all in a single call rather than copying data to temporary files first and then reading from those files. For more details on pipelining, see: Pipelining.

Enabling this behavior is encouraged because Python will tag its pipes with the proper encoding, so there is less chance of encountering encoding errors. Further, using Python stdin pipes is more performant than file I/O.

Include the following in the environment for any tasks performed on z/OS UNIX managed nodes.

When Ansible pipelining is enabled but the PYTHONSTDINENCODING property is not correctly set, the following error may result. Note, the hex '\x81' below may vary depending on the source causing the error:

Seeing unreadable characters in playbook output is most typically an EBCDIC encoding mix up. Double check that the remote environment is set up properly. Also check the expected file encodings, both on the remote node and the control node. ansible.builtin modules will assume all textual data is UTF-8 encoded, while z/OS UNIX may be using EBCDIC. On many z/OS UNIX systems, the default encoding for untagged files is EBCDIC. This variation in default settings can easily lead to data being misinterpreted with the wrong encoding, whether that is failing to auto convert EBCDIC to UTF-8 or erroneously attempting to convert data that is already in UTF-8.

The z/OS operating system currently cannot be configured to run as an Ansible control node. z/OS UNIX System Services interface also cannot be configured to run as an Ansible control node, despite being POSIX-compliant.

There are options available on the IBM Z platform to use it as a control node:

IBM z/OS Container Extensions (zCX)

Red Hat OpenShift on IBM zSystems and LinuxONE

**Examples:**

Example 1 (unknown):
```unknown
- name: Tag my_file.txt as UTF-8.
  ansible.builtin.command: chtag -tc iso8859-1 my_file.txt
```

Example 2 (unknown):
```unknown
ansible.builtin.shell: "some_pgm | iconv -f ibm-1047 -t iso8859-1"
```

Example 3 (unknown):
```unknown
ansible.builtin.raw: |
    export _BPXK_AUTOCVT: "ON" ;
    export _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)" ;
    export _TAG_REDIR_ERR: "txt" ;
    export _TAG_REDIR_IN: "txt" ;
    export _TAG_REDIR_OUT: "txt" ;
    echo "hello world!"
```

Example 4 (unknown):
```unknown
- name: Tag my_file.txt as UTF-8.
  ansible.builtin.command: chtag -tc iso8859-1 my_file.txt
```

---

## Managing BSD hosts with Ansible — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/intro_bsd.html

**Contents:**
- Managing BSD hosts with Ansible
- Connecting to BSD nodes
- Bootstrapping BSD
- Setting the Python interpreter
  - FreeBSD packages and ports
  - INTERPRETER_PYTHON_FALLBACK
  - Debug the discovery of Python
  - Additional variables
- Which modules are available?
- Using BSD as the control node

Managing BSD machines is different from managing other Unix-like machines. If you have managed nodes running BSD, review these topics.

Connecting to BSD nodes

Setting the Python interpreter

FreeBSD packages and ports

INTERPRETER_PYTHON_FALLBACK

Debug the discovery of Python

Which modules are available?

Using BSD as the control node

BSD efforts and contributions

Ansible connects to managed nodes using OpenSSH by default. This works on BSD if you use SSH keys for authentication. However, if you use SSH passwords for authentication, Ansible relies on sshpass. Most versions of sshpass do not deal well with BSD login prompts, so when using SSH passwords against BSD machines, use paramiko to connect instead of OpenSSH. You can do this in ansible.cfg globally or you can set it as an inventory/group/host variable. For example:

Ansible is agentless by default, however, it requires Python on managed nodes. Only the raw module will operate without Python. Although this module can be used to bootstrap Ansible and install Python on BSD variants (see below), it is very limited and the use of Python is required to make full use of Ansible’s features.

The following example installs Python which includes the json library required for the full functionality of Ansible. On your control machine, you can execute the following for most versions of FreeBSD:

Once this is done you can now use other Ansible modules apart from the raw module.

This example demonstrated using pkg on FreeBSD and pkg_add on OpenBSD, however, you should be able to substitute the appropriate package tool for your BSD; the package name may also differ. Refer to the package list or documentation of the BSD variant you are using for the exact Python package name you intend to install.

To support a variety of Unix-like operating systems and distributions, Ansible cannot always rely on the existing environment or env variables to locate the correct Python binary. By default, modules point at /usr/bin/python as this is the most common location. On BSD variants, this path may differ, so it is advised to inform Ansible of the binary’s location. See INTERPRETER_PYTHON. For example, set ansible_python_interpreter inventory variable:

In FreeBSD, there is no guarantee that either /usr/local/bin/python executable file or a link to an executable file is installed by default. The best practice for a remote host, with respect to Ansible, is to install at least the Python version supported by Ansible, for example, lang/python311, and both meta ports lang/python3 and lang/python. Quoting from /usr/ports/lang/python3/pkg-descr:

Quoting from /usr/ports/lang/python/pkg-descr:

As a result, the following packages are installed:

and the following executables and links

Since version 2.8 Ansible provides a useful variable ansible_interpreter_python_fallback to specify a list of paths to search for Python. See INTERPRETER_PYTHON_FALLBACK. This list will be searched and the first item found will be used. For example, the configuration below would make the installation of the meta-ports in the previous section redundant, that is, if you don’t install the Python meta ports the first two items in the list will be skipped and /usr/local/bin/python3.11 will be discovered.

You can use this variable, prolonged by the lower versions of Python, and put it, for example, into the group_vars/all. Then, override it for specific groups in group_vars/{group1, group2, ...} and for specific hosts in host_vars/{host1, host2, ...} if needed. See Variable precedence: where should I put a variable?.

For example, given the inventory

You can see that the first item from the list ansible_interpreter_python_fallback was discovered at the FreeBSD remote host. The variable ansible_playbook_python keeps the path to Python at the Linux control node that ran the playbook.

Regarding the warning, quoting from INTERPRETER_PYTHON

You can either ignore it or get rid of it by setting the variable ansible_python_interpreter=auto_silent because this is, actually, what you want by using /usr/local/bin/python (“interpreters installed later may change which one is used”). For example

Interpreter Discovery

FreeBSD Wiki: Ports/DEFAULT_VERSIONS

If you use additional plugins beyond those bundled with Ansible, you can set similar variables for bash, perl or ruby, depending on how the plugin is written. For example:

The majority of the core Ansible modules are written for a combination of Unix-like machines and other generic services, so most should function well on the BSDs with the obvious exception of those that are aimed at Linux-only technologies (such as LVG).

Using BSD as the control machine is as simple as installing the Ansible package for your BSD variant or by following the pip or ‘from source’ instructions.

Ansible gathers facts from the BSDs in a similar manner to Linux machines, but since the data, names and structures can vary for network, disks and other devices, one should expect the output to be slightly different yet still familiar to a BSD administrator.

BSD support is important to us at Ansible. Even though the majority of our contributors use and target Linux we have an active BSD community and strive to be as BSD-friendly as possible. Please feel free to report any issues or incompatibilities you discover with BSD; pull requests with an included fix are also welcome!

Examples of basic commands

Learning Ansible’s configuration management language

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
[freebsd]
myfreebsdhost ansible_connection=paramiko
```

Example 2 (unknown):
```unknown
ansible -m raw -a "pkg install -y python" myfreebsdhost
```

Example 3 (unknown):
```unknown
ansible -m raw -a "pkg_add -I python%3.11" myopenbsdhost
```

Example 4 (unknown):
```unknown
[freebsd:vars]
ansible_python_interpreter=/usr/local/bin/python
[openbsd:vars]
ansible_python_interpreter=/usr/local/bin/python3
```

---

## Windows Remote Management — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_winrm.html

**Contents:**
- Windows Remote Management
- What is WinRM?
- WinRM Setup
  - Enumerate Listeners
  - Create Listener
  - Remove Listener
- WinRM Authentication
  - Basic
  - Certificate
  - NTLM

Unlike Linux/Unix hosts, which use SSH by default, Windows hosts are configured with WinRM. This topic covers how to configure and use WinRM with Ansible.

Kerberos and Negotiate

Non-Administrator Accounts

HTTPS Certificate Validation

WinRM Troubleshooting

WinRM is a management protocol used by Windows to remotely communicate with another server. It is a SOAP-based protocol that communicates over HTTP/HTTPS and is included in all recent Windows operating systems. Since Windows Server 2012, WinRM has been enabled by default, but in some cases, extra configuration is required to use WinRM with Ansible.

Ansible can use WinRM through the psrp or winrm connection plugins. These plugins have their own Python requirements that are not included in the Ansible package and must be installed separately.

If you chose the pipx install instructions, you can install those requirements by running the following:

Or, if you chose the pip install instructions:

Using the winrm or psrp connection plugins in Ansible on MacOS in the latest releases typically fails. This is a known problem that occurs deep within the Python stack and cannot be changed by Ansible. The only workaround today is to set the environment variable OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes, no_proxy=* and avoid using Kerberos auth.

Before Ansible can connect using WinRM, the Windows host must have a WinRM listener configured. This listener will listen on the configured port and accept incoming WinRM requests.

While this guide covers more details on how to enumerate, add, and remove listeners, you can run the following PowerShell snippet to setup the HTTP listener with the defaults:

To also add a HTTPS listener with a self signed certificate we can run the following:

The above scripts are for demonstration purposes only and should be reviewed before running in a production environment. Some changes, like opening the firewall port for all incoming connections, allowing local accounts to be used with WinRM, self signed certificates, may not be suitable for all environments.

To view the current listeners that are running on the WinRM service:

This will output something like:

In the example above there are two WinRM listeners configured. One is listening on port 5985 over HTTP and the other is listening on port 5986 over HTTPS. Some of the key options that are useful to understand are:

Transport: Whether the listener is run over HTTP or HTTPS

Port: The port the to listen on, default for HTTP is 5985 and HTTPS is 5986

CertificateThumbprint: For HTTPS, this is the thumbprint of the certificate used for the TLS connection

To view the certificate details that is specified by the CertificateThumbprint you can run the following PowerShell command:

Creating a HTTP listener can be done through the Enable-PSRemoting cmdlet but you can also use the following PowerShell code to manually create the HTTP listener.

Creating a HTTPS listener is similar but the Port is now 5986 and the CertificateThumbprint value must be set. The certificate can either be a self signed certificate or a certificate from a certificate authority. How to generate a certificate is outside the scope of this section.

The CertificateThumbprint value must be set to the thumbprint of a certificate that is installed in the LocalMachine\My certificate store.

The Address selector value can be set to one of three values:

* - binds to all addresses

IP:... - binds to the IPv4 or IPv6 address specified by ...

MAC:32-a3-58-90-be-cc - binds to the adapter with the MAC address specified

The following code can remove all listeners or a specific one:

WinRM has several different authentication options that can be used to authenticate a user with a Windows host. Each option has their own advantages and disadvantages so it is important to understand when to use each one and when to not.

The following matrix is a high-level overview of the options:

Active Directory Accounts

Credential Delegation

The Basic and NTLM authentication options should not be used over a HTTP listener as they either offer no encryption or very weak encryption. The psrp connection plugin also offers the Negotiate authentication option which will attempt to use Kerberos before falling back to NTLM. The winrm connection plugin must either specify kerberos or ntlm.

To specify the authentication protocol you can use the following variables:

The recommendations for WinRM would be to use Kerberos auth over HTTP if in a domain environment or Basic/NTLM over HTTPS for local accounts. CredSSP should only be used when absolutely necessary as it can be a security risk due to its use of unconstrained delegation.

Basic authentication is one of the simplest authentication options to use but is also the most insecure. This is because the username and password are simply base64 encoded, and if a secure channel is not in use (eg, HTTPS) then it can be decoded by anyone. Basic authentication can only be used for local accounts (not domain accounts).

The following example shows host vars configured for basic authentication:

Basic authentication is not enabled by default on a Windows host but can be enabled by running the following in PowerShell:

See WinRM Certificate Authentication for more information on how to configure and use certificate authentication.

NTLM is an older authentication mechanism used by Microsoft that can support both local and domain accounts. NTLM is enabled by default on the WinRM service, so no setup is required before using it.

NTLM is the easiest authentication protocol to use and is more secure than Basic authentication. If running in a domain environment, Kerberos should be used instead of NTLM.

Kerberos has several advantages over using NTLM:

NTLM is an older protocol and does not support newer encryption protocols.

NTLM is slower to authenticate because it requires more round trips to the host in the authentication stage.

Unlike Kerberos, NTLM does not allow credential delegation.

This example shows host variables configured to use NTLM authentication:

Kerberos is the recommended authentication option to use when running in a domain environment. Kerberos supports features like credential delegation and message encryption over HTTP and is one of the more secure options that is available through WinRM.

Kerberos does require some additional setup work on the Ansible host before it can be used properly. See Kerberos Authentication for more information on how to configure, use, and troubleshoot Kerberos authentication.

The following example shows host vars configured for Kerberos authentication:

CredSSP authentication is a newer authentication protocol that allows credential delegation. This is achieved by encrypting the username and password after authentication has succeeded and sending that to the server using the CredSSP protocol.

Because the username and password are sent to the server to be used for double hop authentication, ensure that the hosts that the Windows host communicates with are not compromised and are trusted.

CredSSP can be used for both local and domain accounts and also supports message encryption over HTTP.

To use CredSSP authentication, the host vars are configured like so:

CredSSP authentication is not enabled by default on a Windows host, but can be enabled by running the following in PowerShell:

CredSSP requires optional Python libraries to be installed and can be done with pipx:

Or, if you chose the pip install instructions:

CredSSP works by using a TLS connection to wrap the authentication tokens and subsequent messages sent over the connection. By default it will use a self-signed certificate automatically generated by Windows. While using CredSSP over a HTTPS connection will still need to validate the HTTPS certificate used by the WinRM listener, there is no validation done on the CredSSP certificate. It is possible to configure CredSSP to use a different certificate by setting the CertificateThumbprint option under the WinRM service configuration.

WinRM is configured by default to only allow connections from accounts in the local Administrators group. This can be changed by running:

This will display an ACL editor, where new users or groups may be added. To run commands over WinRM, users and groups must have at least the Read and Execute permissions enabled.

While non-administrative accounts can be used with WinRM, most typical server administration tasks require some level of administrative access, so the utility is usually limited.

By default, WinRM will fail to work when running over an unencrypted channel. The WinRM protocol considers the channel to be encrypted if using TLS over HTTP (HTTPS) or using message-level encryption. Using WinRM with TLS is the recommended option as it works with all authentication options, but requires a certificate to be created and used on the WinRM listener.

If in a domain environment, ADCS can create a certificate for the host that is issued by the domain itself.

If using HTTPS is not an option, then HTTP can be used when the authentication option is NTLM, Kerberos or CredSSP. These protocols will encrypt the WinRM payload with their own encryption method before sending it to the server. The message-level encryption is not used when running over HTTPS because the encryption uses the more secure TLS protocol instead. If both transport and message encryption is required, the following hostvars can be set:

Message encryption over HTTP requires pywinrm>=0.3.0.

A last resort is to disable the encryption requirement on the Windows host. This should only be used for development and debugging purposes, as anything sent from Ansible can be viewed or manipulated, and the remote session can be completely taken over by anyone on the same network. To disable the encryption requirement:

Do not disable the encryption check unless it is absolutely required. Doing so could allow sensitive information like credentials and files to be intercepted by others on the network.

As part of the TLS protocol, the certificate is validated to ensure the host matches the subject and the client trusts the issuer of the server certificate. If using a self-signed certificate, the certificate will not be trusted by the client and the connection will fail. To bypass this, set the following hostvars depending on the connection plugin used:

ansible_psrp_cert_validation: ignore

ansible_winrm_server_cert_validation: ignore

One of the more common ways of setting up an HTTPS listener in a domain environment is to use Active Directory Certificate Service (AD CS). AD CS is used to generate signed certificates from a Certificate Signing Request (CSR). If the WinRM HTTPS listener is using a certificate that has been signed by another authority, like AD CS, then Ansible can be set up to trust that issuer as part of the TLS handshake.

To get Ansible to trust a Certificate Authority (CA) like AD CS, the issuer certificate of the CA can be exported as a PEM-encoded certificate. This certificate can then be copied locally to the Ansible control node and used as a source of certificate validation, otherwise known as a CA chain.

The CA chain can contain a single or multiple issuer certificates and each entry is contained on a new line. To then use the custom CA chain as part of the validation process, set the following hostvar depending on the connection plugin used to the path of the CA PEM formatted file:

ansible_winrm_ca_trust_path

If this variable is not set, the default CA chain is used instead which is located in the install path of the Python package certifi. Some Linux distributions may have configured the underlying Python requests library that the psrp and winrm connection plugins use to use the system’s certificate store rather than certifi. If this is the case, the CA chain will be the same as the system’s certificate store.

Due to the design of the WinRM protocol, there are a few limitations when using WinRM which can cause issues when creating playbooks for Ansible. These include:

Credentials are not delegated for most authentication types, which causes authentication errors when accessing network resources or installing certain programs.

Many calls to the Windows Update API are blocked when running over WinRM.

Some programs fail to install with WinRM due to no credential delegation or because they access forbidden Windows APIs like WUA over WinRM.

Commands under WinRM are done under a non-interactive session, which can prevent certain commands or executables from running.

You cannot run a process that interacts with DPAPI, which is used by some installers (like Microsoft SQL Server).

Some of these limitations can be mitigated by doing one of the following:

Set the authentication method to use credssp or kerberos with credential delegation enabled

Use become to bypass all WinRM restrictions and run a command as it would locally. Unlike using an authentication transport like credssp, this will also remove the non-interactive restriction and API restrictions like WUA and DPAPI

Use a scheduled task to run a command that can be created with the win_scheduled_task module. Like become, this bypasses all WinRM restrictions but can only run a command and not modules.

WinRM has a wide range of configuration options, which makes its configuration complex. As a result, errors that Ansible displays could in fact be problems with the host setup instead.

To identify a host issue, run the following command from another Windows host to test out a connection to the target Windows host.

To verify that the target hostname is resolvable on the Ansible control node, run one of the following commands:

To verify that the WinRM service is listening and a firewall is not blocking the connection you can use nc to test the connection over the WinRM port:

To verify that WinRM has a HTTPS listener and is working you can use openssl s_client to test the connection and view the certificate details with:

The openssl s_client command will use the system trust store to validate the certificate which may not align with the trust store used in Ansible. See HTTPS Certificate Validation for more information.

An introduction to playbooks

Tips and tricks for playbooks

Windows-specific module list, all implemented in PowerShell

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
pipx inject ansible "pypsrp<=1.0.0"  # for psrp
pipx inject ansible "pywinrm>=0.4.0"  # for winrm
```

Example 2 (unknown):
```unknown
pip3 install "pypsrp<=1.0.0"  # for psrp
pip3 install "pywinrm>=0.4.0"  # for winrm
```

Example 3 (unknown):
```unknown
# Enables the WinRM service and sets up the HTTP listener
Enable-PSRemoting -Force

# Opens port 5985 for all profiles
$firewallParams = @{
    Action      = 'Allow'
    Description = 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5985]'
    Direction   = 'Inbound'
    DisplayName = 'Windows Remote Management (HTTP-In)'
    LocalPort   = 5985
    Profile     = 'Any'
    Protocol    = 'TCP'
}
New-NetFirewallRule @firewallParams

# Allows local user accounts to be used with WinRM
# This can be ignored if using domain accounts
$tokenFilterParams = @{
    Path         = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
    Name         = 'LocalAccountTokenFilterPolicy'
    Value        = 1
    PropertyType = 'DWORD'
    Force        = $true
}
New-ItemProperty @tokenFilterParams
```

Example 4 (unknown):
```unknown
# Create self signed certificate
$certParams = @{
    CertStoreLocation = 'Cert:\LocalMachine\My'
    DnsName           = $env:COMPUTERNAME
    NotAfter          = (Get-Date).AddYears(1)
    Provider          = 'Microsoft Software Key Storage Provider'
    Subject           = "CN=$env:COMPUTERNAME"
}
$cert = New-SelfSignedCertificate @certParams

# Create HTTPS listener
$httpsParams = @{
    Path                  = 'WSMan:\localhost\Listener'
    Address               = '*'
    CertificateThumbprint = $cert.Thumbprint
    Enabled               = $true
    Port                  = 5986
    Transport             = 'HTTPS'
    Force                 = $true
}
New-Item @httpsParams

# Opens port 5986 for all profiles
$firewallParams = @{
    Action      = 'Allow'
    Description = 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5986]'
    Direction   = 'Inbound'
    DisplayName = 'Windows Remote Management (HTTPS-In)'
    LocalPort   = 5986
    Profile     = 'Any'
    Protocol    = 'TCP'
}
New-NetFirewallRule @firewallParams
```

---

## Windows performance — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_performance.html

**Contents:**
- Windows performance
- Optimize PowerShell performance to reduce Ansible task overhead
- Fix high-CPU-on-boot for VMs/cloud instances

This document offers some performance optimizations you might like to apply to your Windows hosts to speed them up specifically in the context of using Ansible with them, and generally.

To speed up the startup of PowerShell by around 10x, run the following PowerShell snippet in an Administrator session. Expect it to take tens of seconds.

If native images have already been created by the ngen task or service, you will observe no difference in performance (but this snippet will at that point execute faster than otherwise).

PowerShell is used by every Windows Ansible module. This optimization reduces the time PowerShell takes to start up, removing that overhead from every invocation.

This snippet uses the native image generator, ngen to preemptively create native images for the assemblies that PowerShell relies on.

If you are creating golden images to spawn instances from, you can avoid a disruptive high CPU task near startup through processing the ngen queue within your golden image creation, if you know the CPU types won’t change between golden image build process and runtime.

Place the following near the end of your playbook, bearing in mind the factors that can cause native images to be invalidated (see MSDN).

**Examples:**

Example 1 (unknown):
```unknown
function Optimize-Assemblies {
    param (
        [string]$assemblyFilter = "Microsoft.PowerShell.",
        [string]$activity = "Native Image Installation"
    )

    try {
        # Get the path to the ngen executable dynamically
        $ngenPath = [System.IO.Path]::Combine([Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory(), "ngen.exe")

        # Check if ngen.exe exists
        if (-Not (Test-Path $ngenPath)) {
            Write-Host "Ngen.exe not found at $ngenPath. Make sure .NET Framework is installed."
            return
        }

        # Get a list of loaded assemblies
        $assemblies = [AppDomain]::CurrentDomain.GetAssemblies()

        # Filter assemblies based on the provided filter
        $filteredAssemblies = $assemblies | Where-Object { $_.FullName -ilike "$assemblyFilter*" }

        if ($filteredAssemblies.Count -eq 0) {
            Write-Host "No matching assemblies found for optimization."
            return
        }

        foreach ($assembly in $filteredAssemblies) {
            # Get the name of the assembly
            $name = [System.IO.Path]::GetFileName($assembly.Location)

            # Display progress
            Write-Progress -Activity $activity -Status "Optimizing $name"

            # Use Ngen to install the assembly
            Start-Process -FilePath $ngenPath -ArgumentList "install `"$($assembly.Location)`"" -Wait -WindowStyle Hidden
        }

        Write-Host "Optimization complete."
    } catch {
        Write-Host "An error occurred: $_"
    }
}

# Optimize PowerShell assemblies:
Optimize-Assemblies -assemblyFilter "Microsoft.PowerShell."
```

Example 2 (unknown):
```unknown
- name: generate native .NET images for CPU
  win_dotnet_ngen:
```

---

## Using Ansible and Windows — Ansible Core Documentation

**URL:** https://docs.ansible.com/ansible-core/2.19/os_guide/windows_usage.html

**Contents:**
- Using Ansible and Windows
- Use Cases
  - Installing Software
  - Installing Updates
  - Set Up Users and Groups
    - Local
    - Domain
  - Running Commands
    - Choosing Command or Shell
    - Argument Rules

When using Ansible to manage Windows, many of the syntax and rules that apply for Unix/Linux hosts also apply to Windows, but there are still some differences when it comes to components like path separators and OS-specific tasks. This document covers details specific to using Ansible for Windows.

Set Up Users and Groups

Choosing Command or Shell

Creating and Running a Scheduled Task

Path Formatting for Windows

Legacy key=value Style

Developing Windows Modules

Ansible can be used to orchestrate a multitude of tasks on Windows servers. Below are some examples and info about common tasks.

There are three main ways that Ansible can be used to install software:

Using the win_chocolatey module. This sources the program data from the default public Chocolatey repository. Internal repositories can be used instead by setting the source option.

Using the win_package module. This installs software using an MSI or .exe installer from a local/network path or URL.

Using the win_command or win_shell module to run an installer manually.

The win_chocolatey module is recommended since it has the most complete logic for checking to see if a package has already been installed and is up-to-date.

Below are some examples of using all three options to install 7-Zip:

Some installers like Microsoft Office or SQL Server require credential delegation or access to components restricted by WinRM. The best method to bypass these issues is to use become with the task. With become, Ansible will run the installer as if it were run interactively on the host.

Many installers do not properly pass back error information over WinRM. In these cases, if the install has been verified to work locally the recommended method is to use become.

Some installers restart the WinRM or HTTP services, or cause them to become temporarily unavailable, making Ansible assume the system is unreachable.

The win_updates and win_hotfix modules can be used to install updates or hotfixes on a host. The module win_updates is used to install multiple updates by category, while win_hotfix can be used to install a single update or hotfix file that has been downloaded locally.

The win_hotfix module has a requirement that the DISM PowerShell cmdlets are present. These cmdlets were only added by default on Windows Server 2012 and newer and must be installed on older Windows hosts.

The following example shows how win_updates can be used:

The following example show how win_hotfix can be used to install a single update or hotfix:

Ansible can be used to create Windows users and groups both locally and on a domain.

The modules win_user, win_group and win_group_membership manage Windows users, groups and group memberships locally.

The following is an example of creating local accounts and groups that can access a folder on the same host:

The modules win_domain_user and win_domain_group manages users and groups in a domain. The below is an example of ensuring a batch of domain users are created:

In cases where there is no appropriate module available for a task, a command or script can be run using the win_shell, win_command, raw, and script modules.

The raw module simply executes a Powershell command remotely. Since raw has none of the wrappers that Ansible typically uses, become, async and environment variables do not work.

The script module executes a script from the Ansible control node on one or more Windows hosts. Like raw, script currently does not support become, async, or environment variables.

The win_command module is used to execute a command which is either an executable or batch file, while the win_shell module is used to execute commands within a shell.

The win_shell and win_command modules can both be used to execute a command or commands. The win_shell module is run within a shell-like process like PowerShell or cmd, so it has access to shell operators like <, >, |, ;, &&, and ||. Multi-lined commands can also be run in win_shell.

The win_command module simply runs a process outside of a shell. It can still run a shell command like mkdir or New-Item by passing the shell commands to a shell executable like cmd.exe or PowerShell.exe.

Here are some examples of using win_command and win_shell:

Some commands like mkdir, del, and copy only exist in the CMD shell. To run them with win_command they must be prefixed with cmd.exe /c.

When running a command through win_command, the standard Windows argument rules apply:

Each argument is delimited by a white space, which can either be a space or a tab.

An argument can be surrounded by double quotes ". Anything inside these quotes is interpreted as a single argument even if it contains whitespace.

A double quote preceded by a backslash \ is interpreted as just a double quote " and not as an argument delimiter.

Backslashes are interpreted literally unless it immediately precedes double quotes; for example \ == \ and \" == "

If an even number of backslashes is followed by a double quote, one backslash is used in the argument for every pair, and the double quote is used as a string delimiter for the argument.

If an odd number of backslashes is followed by a double quote, one backslash is used in the argument for every pair, and the double quote is escaped and made a literal double quote in the argument.

With those rules in mind, here are some examples of quoting:

For more information, see escaping arguments.

WinRM has some restrictions in place that cause errors when running certain commands. One way to bypass these restrictions is to run a command through a scheduled task. A scheduled task is a Windows component that provides the ability to run an executable on a schedule and under a different account.

Ansible version 2.5 added modules that make it easier to work with scheduled tasks in Windows. The following is an example of running a script as a scheduled task that deletes itself after running:

The modules used in the above example were updated/added in Ansible version 2.5.

Windows differs from a traditional POSIX operating system in many ways. One of the major changes is the shift from / as the path separator to \. This can cause major issues with how playbooks are written, since \ is often used as an escape character on POSIX systems.

Ansible allows two different styles of syntax; each deals with path separators for Windows differently:

When using the YAML syntax for tasks, the rules are well-defined by the YAML standard:

When using a normal string (without quotes), YAML will not consider the backslash an escape character.

When using single quotes ', YAML will not consider the backslash an escape character.

When using double quotes ", the backslash is considered an escape character and needs to escaped with another backslash.

You should only quote strings when it is absolutely necessary or required by YAML, and then use single quotes.

The YAML specification considers the following escape sequences:

\0, \\, \", \_, \a, \b, \e, \f, \n, \r, \t, \v, \L, \N and \P – Single character escape

<TAB>, <SPACE>, <NBSP>, <LNSP>, <PSP> – Special characters

\x.. – 2-digit hex escape

\u.... – 4-digit hex escape

\U........ – 8-digit hex escape

Here are some examples on how to write Windows paths:

This is an example which will fail:

This example shows the use of single quotes when they are required:

The legacy key=value syntax is used on the command line for ad hoc commands, or inside playbooks. The use of this style is discouraged within playbooks because backslash characters need to be escaped, making playbooks harder to read. The legacy syntax depends on the specific implementation in Ansible, and quoting (both single and double) does not have any effect on how it is parsed by Ansible.

The Ansible key=value parser parse_kv() considers the following escape sequences:

\, ', ", \a, \b, \f, \n, \r, \t and \v – Single character escape

\x.. – 2-digit hex escape

\u.... – 4-digit hex escape

\U........ – 8-digit hex escape

\N{...} – Unicode character by name

This means that the backslash is an escape character for some sequences, and it is usually safer to escape a backslash when in this form.

Here are some examples of using Windows paths with the key=value style:

The failing examples don’t fail outright but will substitute \t with the <TAB> character resulting in tempdir being C:\Windows<TAB>emp.

Some things you cannot do with Ansible and Windows are:

Interact with the WinRM listeners

Because WinRM is reliant on the services being online and running during normal operations, you cannot upgrade PowerShell or interact with WinRM listeners with Ansible. Both of these actions will cause the connection to fail. This can technically be avoided by using async or a scheduled task, but those methods are fragile if the process it runs breaks the underlying connection Ansible uses, and are best left to the bootstrapping process or before an image is created.

Because Ansible modules for Windows are written in PowerShell, the development guides for Windows modules differ substantially from those for standard standard modules. Please see Windows module development walkthrough for more information.

An introduction to playbooks

Tips and tricks for playbooks

Windows specific module list, all implemented in PowerShell

Got questions? Need help? Want to share your ideas? Visit the Ansible communication guide

**Examples:**

Example 1 (unknown):
```unknown
# Install/uninstall with chocolatey
- name: Ensure 7-Zip is installed through Chocolatey
  win_chocolatey:
    name: 7zip
    state: present

- name: Ensure 7-Zip is not installed through Chocolatey
  win_chocolatey:
    name: 7zip
    state: absent

# Install/uninstall with win_package
- name: Download the 7-Zip package
  win_get_url:
    url: https://www.7-zip.org/a/7z1701-x64.msi
    dest: C:\temp\7z.msi

- name: Ensure 7-Zip is installed through win_package
  win_package:
    path: C:\temp\7z.msi
    state: present

- name: Ensure 7-Zip is not installed through win_package
  win_package:
    path: C:\temp\7z.msi
    state: absent

# Install/uninstall with win_command
- name: Download the 7-Zip package
  win_get_url:
    url: https://www.7-zip.org/a/7z1701-x64.msi
    dest: C:\temp\7z.msi

- name: Check if 7-Zip is already installed
  win_reg_stat:
    name: HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{23170F69-40C1-2702-1701-000001000000}
  register: 7zip_installed

- name: Ensure 7-Zip is installed through win_command
  win_command: C:\Windows\System32\msiexec.exe /i C:\temp\7z.msi /qn /norestart
  when: 7zip_installed.exists == false

- name: Ensure 7-Zip is uninstalled through win_command
  win_command: C:\Windows\System32\msiexec.exe /x {23170F69-40C1-2702-1701-000001000000} /qn /norestart
  when: 7zip_installed.exists == true
```

Example 2 (unknown):
```unknown
- name: Install all critical and security updates
  win_updates:
    category_names:
    - CriticalUpdates
    - SecurityUpdates
    state: installed
  register: update_result

- name: Reboot host if required
  win_reboot:
  when: update_result.reboot_required
```

Example 3 (unknown):
```unknown
- name: Download KB3172729 for Server 2012 R2
  win_get_url:
    url: http://download.windowsupdate.com/d/msdownload/update/software/secu/2016/07/windows8.1-kb3172729-x64_e8003822a7ef4705cbb65623b72fd3cec73fe222.msu
    dest: C:\temp\KB3172729.msu

- name: Install hotfix
  win_hotfix:
    hotfix_kb: KB3172729
    source: C:\temp\KB3172729.msu
    state: present
  register: hotfix_result

- name: Reboot host if required
  win_reboot:
  when: hotfix_result.reboot_required
```

Example 4 (unknown):
```unknown
- name: Create local group to contain new users
  win_group:
    name: LocalGroup
    description: Allow access to C:\Development folder

- name: Create local user
  win_user:
    name: '{{ item.name }}'
    password: '{{ item.password }}'
    groups: LocalGroup
    update_password: false
    password_never_expires: true
  loop:
  - name: User1
    password: Password1
  - name: User2
    password: Password2

- name: Create Development folder
  win_file:
    path: C:\Development
    state: directory

- name: Set ACL of Development folder
  win_acl:
    path: C:\Development
    rights: FullControl
    state: present
    type: allow
    user: LocalGroup

- name: Remove parent inheritance of Development folder
  win_acl_inheritance:
    path: C:\Development
    reorganize: true
    state: absent
```

---
