# Security Hardening & Exploitation Prevention

## NixOS Security Profiles

### Extreme Hardening Configuration

```nix
{ config, lib, pkgs, ... }:

{
  # Kernel hardening parameters
  boot.kernel.sysctl = {
    # Network security
    "net.ipv4.conf.all.rp_filter" = 1;
    "net.ipv4.conf.default.rp_filter" = 1;
    "net.ipv4.conf.all.accept_redirects" = 0;
    "net.ipv4.conf.default.accept_redirects" = 0;
    "net.ipv4.conf.all.send_redirects" = 0;
    "net.ipv4.conf.default.send_redirects" = 0;
    "net.ipv4.conf.all.accept_source_route" = 0;
    "net.ipv6.conf.all.accept_source_route" = 0;
    "net.ipv4.icmp_echo_ignore_broadcasts" = 1;
    "net.ipv4.icmp_ignore_bogus_error_responses" = 1;
    "net.ipv4.tcp_syncookies" = 1;
    
    # Memory protection
    "kernel.kptr_restrict" = 2;
    "kernel.dmesg_restrict" = 1;
    "kernel.yama.ptrace_scope" = 2;
    "kernel.unprivileged_bpf_disabled" = 1;
    "net.core.bpf_jit_harden" = 2;
    
    # ASLR enhancement
    "kernel.randomize_va_space" = 2;
    
    # Prevent privilege escalation
    "kernel.unprivileged_userns_clone" = 0;
    "kernel.kexec_load_disabled" = 1;
    
    # Core dump restrictions
    "kernel.core_uses_pid" = 1;
    "fs.suid_dumpable" = 0;
  };
  
  # Kernel parameters
  boot.kernelParams = [
    "slab_nomerge"
    "init_on_alloc=1"
    "init_on_free=1"
    "page_alloc.shuffle=1"
    "pti=on"
    "vsyscall=none"
    "debugfs=off"
    "oops=panic"
    "mce=0"
    "quiet"
    "loglevel=0"
  ];
  
  # Blacklist vulnerable modules
  boot.blacklistedKernelModules = [
    "dccp" "sctp" "rds" "tipc"    # Network protocols
    "n-hdlc" "ax25" "netrom"      # Amateur radio
    "x25" "rose" "decnet"          # Legacy protocols
    "econet" "af_802154"           # Rare protocols
    "ipx" "appletalk" "psnap"      # Legacy network
    "p8023" "p8022" "llc"          # LLC protocols
    "bluetooth" "btusb"            # Bluetooth (if not needed)
    "uvcvideo"                     # Webcam (if not needed)
  ];
  
  # AppArmor mandatory access control
  security.apparmor = {
    enable = true;
    killUnconfinedConfinables = true;
    packages = [ pkgs.apparmor-profiles ];
  };
  
  # Audit system
  security.audit.enable = true;
  security.auditd.enable = true;
  
  # Restrict /proc and /sys
  security.hideProcessInformation = true;
  security.protectKernelImage = true;
  
  # Disable unnecessary filesystems
  boot.supportedFilesystems = lib.mkForce [ "ext4" "vfat" ];
  
  # Firewall with strict rules
  networking.firewall = {
    enable = true;
    allowPing = false;
    logRefusedConnections = true;
    logRefusedPackets = true;
    rejectPackets = true;
  };
  
  # SSH hardening
  services.openssh = {
    enable = true;
    settings = {
      PasswordAuthentication = false;
      KbdInteractiveAuthentication = false;
      PermitRootLogin = "no";
      X11Forwarding = false;
      AllowUsers = [ "admin" ];
      MaxAuthTries = 3;
      ClientAliveInterval = 300;
      ClientAliveCountMax = 2;
      Ciphers = [
        "chacha20-poly1305@openssh.com"
        "aes256-gcm@openssh.com"
      ];
      KexAlgorithms = [
        "curve25519-sha256"
        "curve25519-sha256@libssh.org"
      ];
      Macs = [
        "hmac-sha2-512-etm@openssh.com"
        "hmac-sha2-256-etm@openssh.com"
      ];
    };
    extraConfig = ''
      AllowAgentForwarding no
      AllowStreamLocalForwarding no
      AllowTcpForwarding no
      PermitUserEnvironment no
      LogLevel VERBOSE
    '';
  };
  
  # Automatic security updates
  system.autoUpgrade = {
    enable = true;
    allowReboot = false;
    dates = "03:00";
  };
}
```

## Container Security

### Hardened Container Runtime

```nix
{ config, pkgs, ... }:

{
  # Rootless containers
  virtualisation.docker = {
    enable = true;
    rootless = {
      enable = true;
      setSocketVariable = true;
    };
    daemon.settings = {
      # Security options
      no-new-privileges = true;
      seccomp-profile = "${pkgs.docker}/etc/docker/seccomp.json";
      userns-remap = "default";
      
      # Resource limits
      default-ulimits = {
        nofile = {
          Hard = 64000;
          Soft = 64000;
        };
      };
      
      # Logging
      log-driver = "json-file";
      log-opts = {
        max-size = "10m";
        max-file = "3";
      };
    };
  };
  
  # Podman with advanced security
  virtualisation.podman = {
    enable = true;
    dockerCompat = false;
    
    defaultNetwork.settings = {
      dns_enabled = true;
      firewall_driver = "nftables";
    };
    
    extraPackages = with pkgs; [
      crun                    # Faster OCI runtime
      slirp4netns             # Rootless networking
      fuse-overlayfs          # Rootless storage
    ];
  };
  
  # Container networking isolation
  networking.nat = {
    enable = true;
    internalInterfaces = [ "ve-+" ];
  };
}

# Secure container definition
{ pkgs, ... }:

pkgs.dockerTools.buildImage {
  name = "secure-app";
  tag = "latest";
  
  runAsRoot = ''
    #!${pkgs.runtimeShell}
    
    # Create non-root user
    ${pkgs.shadow}/bin/groupadd -r app
    ${pkgs.shadow}/bin/useradd -r -g app -s /sbin/nologin app
    
    # Minimal permissions
    chmod 755 /app
    chown -R app:app /app
  '';
  
  config = {
    User = "app";
    WorkingDir = "/app";
    
    # Security options
    SecurityOpt = [
      "no-new-privileges:true"
      "seccomp=unconfined"
    ];
    
    # Read-only root filesystem
    ReadOnlyRootFilesystem = true;
    
    # Drop all capabilities
    CapDrop = [ "ALL" ];
    
    # Resource limits
    Memory = "512m";
    MemorySwap = "512m";
    CpuShares = 512;
    
    # Healthcheck
    Healthcheck = {
      Test = [ "CMD" "curl" "-f" "http://localhost:8080/health" ];
      Interval = "30s";
      Timeout = "3s";
      Retries = 3;
    };
  };
}
```

## Binary Security Analysis

### Automated Security Scanner

```bash
#!/usr/bin/env bash
# security-scan.sh

set -euo pipefail

binary="$1"

echo "=== Binary Security Analysis ==="
echo "Target: $binary"
echo

# Check if binary exists
if [[ ! -f "$binary" ]]; then
    echo "Error: Binary not found"
    exit 1
fi

# File type and architecture
echo "File Info:"
file "$binary"
echo

# Check security features
echo "Security Features:"
readelf -l "$binary" | grep -E "GNU_STACK|GNU_RELRO" || echo "No GNU protections found"
readelf -d "$binary" | grep -E "BIND_NOW|FLAGS" || echo "No binding flags"
echo

# Symbols (look for dangerous functions)
echo "Dangerous Functions:"
nm -D "$binary" 2>/dev/null | grep -E "strcpy|strcat|sprintf|gets|system|exec" || echo "None found"
echo

# RPATH/RUNPATH analysis
echo "Library Paths:"
readelf -d "$binary" | grep -E "RPATH|RUNPATH" || echo "No RPATH/RUNPATH set"
echo

# Dependencies
echo "Dependencies:"
ldd "$binary" | head -20
echo

# Check for PIE (Position Independent Executable)
echo "PIE Check:"
readelf -h "$binary" | grep -q "DYN" && echo "✓ PIE enabled" || echo "✗ PIE disabled"
echo

# Stack canary
echo "Stack Canary:"
readelf -s "$binary" | grep -q "__stack_chk_fail" && echo "✓ Stack canary enabled" || echo "✗ No stack canary"
echo

# FORTIFY_SOURCE
echo "FORTIFY_SOURCE:"
readelf -s "$binary" | grep -E "__.*_chk" | head -5 || echo "✗ Not fortified"
echo

# Check for hardcoded secrets
echo "Potential Secrets:"
strings "$binary" | grep -E "password|token|secret|key|api" -i | head -10 || echo "None found"
echo

# Writable and executable segments (bad)
echo "Memory Segments:"
readelf -l "$binary" | awk '/LOAD/ {printf "%s %s\n", $1, $7}' | while read -r segment perms; do
    if [[ "$perms" == *W*X* ]] || [[ "$perms" == *X*W* ]]; then
        echo "⚠ WARNING: Writable AND executable segment found: $perms"
    fi
done
echo

echo "=== Analysis Complete ==="
```

### Exploit Mitigation Wrapper

```nix
{ lib, stdenv, makeWrapper }:

{ pname, version, src }:

let
  # Generate seccomp profile
  seccompProfile = pkgs.writeText "seccomp.json" (builtins.toJSON {
    defaultAction = "SCMP_ACT_ERRNO";
    architectures = [ "SCMP_ARCH_X86_64" ];
    syscalls = [
      {
        names = [
          "read" "write" "open" "close" "stat" "fstat" "lstat"
          "poll" "lseek" "mmap" "mprotect" "munmap" "brk"
          "rt_sigaction" "rt_sigprocmask" "ioctl" "access"
          "socket" "connect" "accept" "sendto" "recvfrom"
          "bind" "listen" "setsockopt" "getsockopt"
        ];
        action = "SCMP_ACT_ALLOW";
      }
    ];
  });

in stdenv.mkDerivation {
  inherit pname version src;
  
  nativeBuildInputs = [ makeWrapper ];
  
  postInstall = ''
    # Wrap binary with security measures
    for bin in $out/bin/*; do
      wrapProgram "$bin" \
        --set SECCOMP_PROFILE "${seccompProfile}" \
        --set MALLOC_CHECK_ 3 \
        --set MALLOC_PERTURB_ $((RANDOM % 255 + 1)) \
        --prefix LD_PRELOAD : "${pkgs.libseccomp}/lib/libseccomp.so"
    done
  '';
  
  meta.security = {
    seccomp = true;
    malloc_hardening = true;
  };
}
```

## Network Security

### Advanced Firewall Configuration

```nix
{ config, lib, pkgs, ... }:

{
  # nftables-based firewall
  networking.nftables = {
    enable = true;
    
    ruleset = ''
      table inet filter {
        # Connection tracking helpers
        ct helper ftp-standard {
          type "ftp" protocol tcp
        }
        
        chain input {
          type filter hook input priority 0; policy drop;
          
          # Accept loopback
          iif lo accept
          
          # Connection tracking
          ct state invalid drop
          ct state { established, related } accept
          
          # Rate limiting for SSH
          tcp dport 22 ct state new limit rate 3/minute accept
          
          # ICMP rate limiting
          ip protocol icmp limit rate 10/second accept
          ip6 nexthdr icmpv6 limit rate 10/second accept
          
          # Drop port scans
          tcp flags & (fin|syn|rst|ack) == syn ct state new limit rate 100/second burst 150 packets accept
          
          # Log dropped packets
          limit rate 5/minute log prefix "nftables-dropped: " level info
        }
        
        chain forward {
          type filter hook forward priority 0; policy drop;
        }
        
        chain output {
          type filter hook output priority 0; policy accept;
        }
      }
      
      # NAT rules
      table ip nat {
        chain postrouting {
          type nat hook postrouting priority 100; policy accept;
          oifname "eth0" masquerade
        }
      }
    '';
  };
  
  # IDS/IPS with Suricata
  services.suricata = {
    enable = true;
    settings = {
      vars = {
        address-groups = {
          HOME_NET = "[192.168.0.0/16,10.0.0.0/8]";
          EXTERNAL_NET = "!$HOME_NET";
        };
      };
      
      outputs = [
        {
          fast = {
            enabled = true;
            filename = "fast.log";
          };
        }
      ];
      
      af-packet = [{
        interface = "eth0";
        cluster-id = 99;
        cluster-type = "cluster_flow";
      }];
    };
  };
}
```

## Zero-Trust Architecture

```nix
{ config, lib, pkgs, ... }:

{
  # mTLS for all services
  services.nginx = {
    enable = true;
    
    virtualHosts."secure.example.com" = {
      forceSSL = true;
      sslCertificate = "/var/lib/certs/server.crt";
      sslCertificateKey = "/var/lib/certs/server.key";
      
      # Client certificate authentication
      extraConfig = ''
        ssl_client_certificate /var/lib/certs/ca.crt;
        ssl_verify_client on;
        ssl_verify_depth 2;
        
        # TLS 1.3 only
        ssl_protocols TLSv1.3;
        ssl_prefer_server_ciphers off;
        
        # HSTS
        add_header Strict-Transport-Security "max-age=63072000" always;
        
        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer" always;
        add_header Content-Security-Policy "default-src 'self'" always;
      '';
    };
  };
  
  # WireGuard VPN for zero-trust networking
  networking.wireguard.interfaces.wg0 = {
    ips = [ "10.100.0.1/24" ];
    listenPort = 51820;
    
    privateKeyFile = "/var/lib/wireguard/private.key";
    
    peers = [
      {
        publicKey = "CLIENT_PUBLIC_KEY";
        allowedIPs = [ "10.100.0.2/32" ];
        persistentKeepalive = 25;
      }
    ];
    
    postSetup = ''
      ${pkgs.iptables}/bin/iptables -A FORWARD -i wg0 -j ACCEPT
      ${pkgs.iptables}/bin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    '';
  };
}
```

## Runtime Application Self-Protection (RASP)

```bash
#!/usr/bin/env bash
# rasp-wrapper.sh - Runtime protection wrapper

set -euo pipefail

APP="$1"
shift

# Enable all security features
export MALLOC_CHECK_=3
export MALLOC_PERTURB_=$((RANDOM % 255 + 1))

# Randomize ASLR
echo 2 > /proc/sys/kernel/randomize_va_space

# Run under restricted namespaces
unshare --map-root-user --net --pid --fork bash -c "
    # Network isolation
    ip link set lo up
    
    # Resource limits
    ulimit -n 1024
    ulimit -u 100
    ulimit -m 512000
    
    # Execute with seccomp
    exec '$APP' \"\$@\"
" "$@"
```
