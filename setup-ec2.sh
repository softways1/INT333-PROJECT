#!/bin/bash
# ==============================================================================
# Master EC2 Provisioning & Tooling Setup Script
# Project: AI Powered Resume Analyzer - DevOps Lifecycle (INT333)
# Student: AMAN KUMAR SINGH (12301704)
# ==============================================================================

set -e

echo ">>> [1/7] Configuring 4GB Swap Space for Free-Tier Memory Stability..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 4G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "Swap configured successfully:"
    free -h
else
    echo "Swapfile already exists."
fi

echo ">>> [2/7] Updating Base System Packages..."
sudo apt-get update -y
sudo apt-get install -y curl wget git unzip htop software-properties-common apt-transport-https ca-certificates gnupg

echo ">>> [3/7] Installing Docker & Docker Compose Plugin..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker ubuntu
sudo usermod -aG docker jenkins 2>/dev/null || true
sudo systemctl enable docker
sudo systemctl start docker

echo ">>> [4/7] Installing Terraform (HashiCorp)..."
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update -y
sudo apt-get install -y terraform

echo ">>> [5/7] Installing Puppet Standalone..."
sudo apt-get install -y puppet-agent || sudo apt-get install -y puppet || true
export PATH=$PATH:/opt/puppetlabs/bin

echo ">>> [6/7] Installing Jenkins (OpenJDK 17 + Jenkins Engine)..."
sudo apt-get install -y openjdk-17-jdk-headless
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y jenkins

# Configure low-memory JVM args for Free Tier stability
sudo sed -i 's/JAVA_ARGS="-Djava.awt.headless=true"/JAVA_ARGS="-Djava.awt.headless=true -Xmx350m -Xms128m"/' /etc/default/jenkins 2>/dev/null || true
sudo systemctl enable jenkins
sudo systemctl restart jenkins

echo ">>> [7/7] Installing Nagios Core & Monitoring Plugins..."
sudo apt-get install -y nagios4 nagios-plugins-contrib nagios-nrpe-plugin apache2
sudo systemctl enable nagios4 apache2
sudo systemctl start nagios4 apache2

# Set default Nagios admin credentials
sudo htpasswd -b -c /etc/nagios4/htpasswd.users nagiosadmin admin123 || true

echo "========================================================================"
echo " All DevOps Tools Installed Successfully!"
echo " Jenkins Initial Admin Password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword 2>/dev/null || echo "Jenkins is initializing..."
echo " Nagios Admin: nagiosadmin / admin123"
echo "========================================================================"
