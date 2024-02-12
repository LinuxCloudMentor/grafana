import subprocess

print("Make sure your system meets the minimum system requirements: Minimum recommended memory: 512 MB, Minimum recommended CPU: 1.")

# Download and import GPG key
subprocess.run(["wget", "-q", "-O", "gpg.key", "https://rpm.grafana.com/gpg.key"])
subprocess.run(["sudo", "rpm", "--import", "gpg.key"])

# Create Grafana repository configuration file
grafana_repo_config = """
[grafana]
name=grafana
baseurl=https://rpm.grafana.com
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://rpm.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
exclude=*beta*
"""
with open("/etc/yum.repos.d/grafana.repo", "w") as f:
    f.write(grafana_repo_config)

# Ask Grafana version
grafana_version = input("Enter Grafana version (e.g., 10.2.0, 10.3.1): ")
# Ask for Grafana port and update configuration
grafana_port = input("Enter Grafana port: ")
# Ask for installation option
print("Choose installation option:")
print("1. Install open source software")
print("2. Install enterprise")
option = input("Enter your choice (1 or 2): ")

# Select appropriate installation command based on the option
if option == "1":
    grafana_url = f"https://dl.grafana.com/oss/release/grafana-{grafana_version}-1.x86_64.rpm"
elif option == "2":
    grafana_url = f"https://dl.grafana.com/enterprise/release/grafana-enterprise-{grafana_version}-1.x86_64.rpm"
else:
    print("Invalid option selected.")
    exit()

# Install Grafana
subprocess.run(["sudo", "yum", "install", "-y", grafana_url])

# Start and enable Grafana service
subprocess.run(["sudo", "systemctl", "start", "grafana-server"])
subprocess.run(["sudo", "systemctl", "enable", "grafana-server"])

# Add Grafana port to firewalld
print(f"Firewall adding Grafana {grafana_port}")

subprocess.run(["sudo", "firewall-cmd", "--zone=public", "--add-port", f"{grafana_port}/tcp", "--permanent"])
subprocess.run(["sudo", "firewall-cmd", "--reload"])

# Add Grafana port to selinux
print(f"Selinux adding Grafana {grafana_port}")

# Add Grafana port to SELinux
subprocess.run(["sudo", "semanage", "port", "-a", "-t", "http_port_t", "-p", "tcp", grafana_port])

# Update Grafana configuration file with port
grafana_ini_config = f"""
[server]
http_port = {grafana_port}
"""
with open("/etc/grafana/grafana.ini", "a") as f:
    f.write(grafana_ini_config)

# Restart Grafana service
subprocess.run(["sudo", "systemctl", "restart", "grafana-server"])

print("Grafana installation and configuration completed.")

print(f"http://ip_address:{grafana_port} default Username : admin & Password : admin")


