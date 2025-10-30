#!/bin/bash

set -e

echo "=========================================="
echo "AWS Fitness Tracker Deployment Script"
echo "=========================================="

# Check if running on EC2
if [ ! -f /sys/hypervisor/uuid ] || ! grep -q ec2 /sys/hypervisor/uuid 2>/dev/null; then
    echo "Warning: This script is designed to run on AWS EC2 instances"
fi

# Update system
echo "[1/8] Updating system packages..."
sudo yum update -y || sudo apt-get update -y

# Install Docker
echo "[2/8] Installing Docker..."
if ! command -v docker &> /dev/null; then
    # Amazon Linux 2
    if [ -f /etc/amazon-linux-release ]; then
        sudo yum install -y docker
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
    # Ubuntu
    else
        sudo apt-get install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
    fi
    echo "Docker installed. You may need to log out and back in for group changes to take effect."
else
    echo "Docker already installed"
fi

# Install Docker Compose
echo "[3/8] Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose already installed"
fi

# Install Git
echo "[4/8] Installing Git..."
if ! command -v git &> /dev/null; then
    sudo yum install -y git || sudo apt-get install -y git
else
    echo "Git already installed"
fi

# Generate security keys if needed
echo "[5/8] Generating security keys..."
if [ -f .env.aws ]; then
    if grep -q "REPLACE_WITH_GENERATED_KEY" .env.aws; then
        KEY1=$(openssl rand -hex 32)
        KEY2=$(openssl rand -hex 32)
        sed -i "s/REPLACE_WITH_GENERATED_KEY_1/$KEY1/" .env.aws
        sed -i "s/REPLACE_WITH_GENERATED_KEY_2/$KEY2/" .env.aws
        echo "Security keys generated"
    else
        echo "Keys already configured"
    fi
else
    echo "Error: .env.aws file not found"
    exit 1
fi

# Stop existing containers
echo "[6/8] Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Build and start containers
echo "[7/8] Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to be ready
echo "[8/8] Waiting for services to start..."
sleep 10

# Check container status
echo "=========================================="
echo "Container Status:"
docker-compose -f docker-compose.prod.yml ps

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Application URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'EC2_PUBLIC_IP'):8000"
echo "API Health Check: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'EC2_PUBLIC_IP'):8000/api/v1/health"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "To stop:"
echo "  docker-compose -f docker-compose.prod.yml down"
echo "=========================================="
