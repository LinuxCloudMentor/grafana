import subprocess

# Stop Grafana service
subprocess.run(["sudo", "systemctl", "stop", "grafana-server"])

# Uninstall Grafana
subprocess.run(["sudo", "yum", "remove", "-y", "grafana"])

# Remove Grafana repository configuration file
subprocess.run(["sudo", "rm", "/etc/yum.repos.d/grafana.repo"])

# Extract Grafana port from configuration file
grafana_port = None
with open("/etc/grafana/grafana.ini", "r") as f:
    for line in f:
        if line.startswith("http_port"):
            grafana_port = line.split("=")[1].strip()
            break

if grafana_port:
    # Remove Grafana port from firewalld
    subprocess.run(["sudo", "firewall-cmd", "--zone=public", "--remove-port", f"{grafana_port}/tcp", "--permanent"])
    subprocess.run(["sudo", "firewall-cmd", "--reload"])

    # Remove Grafana port from SELinux
    subprocess.run(["sudo", "semanage", "port", "-d", "-t", "http_port_t", "-p", "tcp", grafana_port])
else:
    print("Grafana port not found in configuration file.")
subprocess.run(["sudo", "rm", '-rf', "/etc/grafana"])
print("Grafana uninstallation completed.")

