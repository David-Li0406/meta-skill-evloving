#!/usr/bin/env python3
"""
NixOS Remote Cache Server - Configuration Generator
Generates optimized cache server configuration based on hardware profile
"""

import argparse
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

@dataclass
class HardwareProfile:
    name: str
    ram_mb: int
    cpu_cores: int
    storage_gb: int
    
    def get_max_jobs(self) -> int:
        """Calculate optimal max-jobs based on CPU and RAM"""
        # Rule: 1 job per core, but limited by RAM (assuming ~2GB per job)
        ram_based_limit = max(1, self.ram_mb // 2048)
        cpu_based_limit = max(1, self.cpu_cores)
        return min(ram_based_limit, cpu_based_limit)
    
    def get_max_free(self) -> int:
        """Calculate max-free bytes (keep 25% free)"""
        return int(self.storage_gb * 1024 * 1024 * 1024 * 0.25)
    
    def get_min_free(self) -> int:
        """Calculate min-free bytes (maintain at least 10GB or 15%)"""
        min_absolute = 10 * 1024 * 1024 * 1024  # 10GB
        min_relative = int(self.storage_gb * 1024 * 1024 * 1024 * 0.15)
        return max(min_absolute, min_relative)
    
    def needs_zram(self) -> bool:
        """Determine if zram compression should be enabled"""
        return self.ram_mb < 8192
    
    def get_cache_ttl(self) -> int:
        """Get cache TTL based on storage constraints"""
        if self.storage_gb < 100:
            return 7  # 7 days for limited storage
        elif self.storage_gb < 250:
            return 14  # 14 days
        else:
            return 30  # 30 days

def detect_hardware() -> HardwareProfile:
    """Auto-detect hardware specifications"""
    # Get RAM
    try:
        mem_info = subprocess.check_output(['free', '-m'], text=True)
        ram_mb = int([line for line in mem_info.split('\n') if line.startswith('Mem:')][0].split()[1])
    except:
        print("Warning: Could not detect RAM, defaulting to 4096MB", file=sys.stderr)
        ram_mb = 4096
    
    # Get CPU cores
    try:
        cpu_cores = int(subprocess.check_output(['nproc'], text=True).strip())
    except:
        print("Warning: Could not detect CPU cores, defaulting to 2", file=sys.stderr)
        cpu_cores = 2
    
    # Get storage
    try:
        df_output = subprocess.check_output(['df', '-BG', '/'], text=True)
        storage_line = [line for line in df_output.split('\n') if line.startswith('/')][0]
        storage_gb = int(storage_line.split()[1].rstrip('G'))
    except:
        print("Warning: Could not detect storage, defaulting to 100GB", file=sys.stderr)
        storage_gb = 100
    
    return HardwareProfile(
        name="auto-detected",
        ram_mb=ram_mb,
        cpu_cores=cpu_cores,
        storage_gb=storage_gb
    )

def generate_cache_config(profile: HardwareProfile, server_ip: str = "10.255.255.1") -> str:
    """Generate NixOS cache server configuration"""
    
    config = f"""# NixOS Remote Cache Server Configuration
# Hardware Profile: {profile.name}
# RAM: {profile.ram_mb}MB | CPU: {profile.cpu_cores} cores | Storage: {profile.storage_gb}GB

{{ config, pkgs, ... }}:

{{
  # Cache Server Service
  services.nix-serve = {{
    enable = true;
    secretKeyFile = "/var/cache-priv-key.pem";
    port = 5000;
  }};

  # Nix daemon optimization
  nix.settings = {{
    # Build settings
    max-jobs = {profile.get_max_jobs()};
    cores = {max(1, profile.cpu_cores - 1)};  # Leave 1 core for system
    
    # Storage management
    max-free = {profile.get_max_free()};  # {profile.get_max_free() // (1024**3)}GB
    min-free = {profile.get_min_free()};  # {profile.get_min_free() // (1024**3)}GB
    
    # Cache behavior
    keep-outputs = true;
    keep-derivations = true;
    
    # Optimize for local network
    http-connections = 25;  # Increased for local network
    
    # Build optimization
    auto-optimise-store = true;
    
    # Substituters (this machine builds and caches)
    substituters = [
      "https://cache.nixos.org"
    ];
  }};
  
  # Automatic garbage collection
  nix.gc = {{
    automatic = true;
    dates = "daily";
    options = "--delete-older-than {profile.get_cache_ttl()}d";
  }};
  
  # Network optimization
  networking.interfaces.eth0 = {{
    ipv4.addresses = [{{
      address = "{server_ip}";
      prefixLength = 24;
    }}];
  }};
  
  # Kernel optimizations for cache server
  boot.kernel.sysctl = {{
    # Network performance
    "net.core.rmem_max" = 134217728;
    "net.core.wmem_max" = 134217728;
    "net.ipv4.tcp_rmem" = "4096 87380 67108864";
    "net.ipv4.tcp_wmem" = "4096 65536 67108864";
    "net.ipv4.tcp_congestion_control" = "bbr";
    "net.core.default_qdisc" = "fq";
    
    # File system performance
    "vm.swappiness" = {10 if profile.ram_mb < 8192 else 1};
    "vm.vfs_cache_pressure" = 50;
  }};
"""

    # Add zram if low memory
    if profile.needs_zram():
        config += """
  # ZRAM compression for low memory systems
  zramSwap = {
    enable = true;
    memoryPercent = 50;  # Use up to 50% of RAM for compressed swap
    algorithm = "zstd";  # Fast compression
  };
"""

    # Add resource monitoring
    config += """
  # System monitoring (optional but recommended)
  services.prometheus = {
    enable = true;
    exporters = {
      node = {
        enable = true;
        enabledCollectors = [ "systemd" "processes" ];
        port = 9100;
      };
    };
  };
  
  # Firewall configuration
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 
      5000   # nix-serve
      9100   # prometheus node exporter (optional)
    ];
  };
}
"""

    return config

def main():
    parser = argparse.ArgumentParser(
        description='Generate optimized NixOS cache server configuration'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Auto-detect hardware and generate config'
    )
    parser.add_argument(
        '--ram',
        type=int,
        help='RAM in MB (e.g., 4096)'
    )
    parser.add_argument(
        '--cpu',
        type=int,
        help='Number of CPU cores'
    )
    parser.add_argument(
        '--storage',
        type=int,
        help='Storage in GB'
    )
    parser.add_argument(
        '--server-ip',
        default='10.255.255.1',
        help='Server IP address (default: 10.255.255.1)'
    )
    parser.add_argument(
        '--output',
        default='/tmp/cache-server-config.nix',
        help='Output file path'
    )
    
    args = parser.parse_args()
    
    # Determine hardware profile
    if args.auto:
        profile = detect_hardware()
        print(f"Auto-detected: {profile.ram_mb}MB RAM, {profile.cpu_cores} cores, {profile.storage_gb}GB storage", file=sys.stderr)
    elif args.ram and args.cpu and args.storage:
        profile = HardwareProfile(
            name="custom",
            ram_mb=args.ram,
            cpu_cores=args.cpu,
            storage_gb=args.storage
        )
    else:
        print("Error: Use --auto or provide --ram, --cpu, and --storage", file=sys.stderr)
        sys.exit(1)
    
    # Generate configuration
    config = generate_cache_config(profile, args.server_ip)
    
    # Write to file
    with open(args.output, 'w') as f:
        f.write(config)
    
    print(f"\n✓ Configuration generated: {args.output}", file=sys.stderr)
    print(f"\nHardware Profile Summary:", file=sys.stderr)
    print(f"  RAM: {profile.ram_mb}MB", file=sys.stderr)
    print(f"  CPU: {profile.cpu_cores} cores", file=sys.stderr)
    print(f"  Storage: {profile.storage_gb}GB", file=sys.stderr)
    print(f"\nOptimizations Applied:", file=sys.stderr)
    print(f"  max-jobs: {profile.get_max_jobs()}", file=sys.stderr)
    print(f"  Cache TTL: {profile.get_cache_ttl()} days", file=sys.stderr)
    print(f"  ZRAM: {'Enabled' if profile.needs_zram() else 'Disabled'}", file=sys.stderr)
    print(f"\nNext steps:", file=sys.stderr)
    print(f"  1. Review the configuration: cat {args.output}", file=sys.stderr)
    print(f"  2. Merge with your /etc/nixos/configuration.nix", file=sys.stderr)
    print(f"  3. Generate cache keys: nix-store --generate-binary-cache-key cache-key /var/cache-priv-key.pem cache-pub-key.pem", file=sys.stderr)
    print(f"  4. Apply: sudo nixos-rebuild switch", file=sys.stderr)

if __name__ == '__main__':
    main()
