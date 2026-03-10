# HashiCorp Vault on Amazon Web Services
## Architecture Overview (Production Design)
```bash
                +-----------------------------+
                |        AWS Route53         |
                +-------------+---------------+
                              |
                        Internal DNS
                              |
                    +---------v---------+
                    |   AWS NLB (TLS)   |
                    +---------+---------+
                              |
           +------------------+------------------+
           |                                     |
    +------v------+                       +------v------+
    | Vault Node 1 |                      | Vault Node 2 |
    | EC2 (Leader) |                      | EC2 (Standby)|
    +------+-------+                      +------+-------+
           |                                     |
           +------------------+------------------+
                              |
                       +------v------+
                       | Vault Node 3|
                       |  EC2 Standby|
                       +------+------+
                              |
                       +------v------+
                       | Integrated  |
                       |   Raft      |
                       | Storage     |
                       +-------------+

Monitoring:
Prometheus + Grafana

Audit Logs:
CloudWatch / S3

Auto Unseal:
AWS KMS
```
## Key components
```bash
| Component  | Purpose                   |
| ---------- | ------------------------- |
| EC2        | Vault servers             |
| NLB        | Highly available endpoint |
| KMS        | Auto-unseal               |
| Raft       | HA storage                |
| IAM        | Secure authentication     |
| CloudWatch | Logging                   |
| Prometheus | metrics                   |
```
## 2. Network Setup (VPC)
Create a dedicated VPC for Vault.
```bash
VPC
├── Public Subnet (ALB/NLB if needed)
└── Private Subnets
      ├── Vault Node 1
      ├── Vault Node 2
      └── Vault Node 3
```
### Steps
Create VPC
```bash
CIDR: 10.10.0.0/16
```
Create 3 private subnets
```bash
10.10.1.0/24
10.10.2.0/24
10.10.3.0/24
```
Attach:
- Internet Gateway
- NAT Gateway (for package updates)
## 3. Security Groups
### Create vault-sg
Allow:
```bash
8200  TCP  internal VPC only
8201  TCP  internal VPC only
22    TCP  bastion host
```
Example inbound:
```bash
source: 10.10.0.0/16
ports: 8200,8201
```
## 4. EC2 Provisioning
Launch 3 EC2 instances.
```bash
c6i.large
m6i.large
# system specification
CPU: 4+
RAM: 8GB+
NVMe SSD
OS: Ubuntu 22.04
```
**Note: ** Recommended instance types for high throughput
## 5. Install Vault
```bash
sudo apt update
wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip
unzip vault_1.15.0_linux_amd64.zip
sudo mv vault /usr/local/bin/
# verify
vault --version
```
## 6. Create Vault User
```bash
sudo useradd --system --home /etc/vault.d --shell /bin/false vault

# Directories:
sudo mkdir -p /opt/vault/data
sudo mkdir -p /etc/vault.d

# Permissions
sudo chown -R vault:vault /opt/vault
sudo chown -R vault:vault /etc/vault.d
```
## 7. TLS Configuration
Generate certificate via:
- ACM Private CA
- Internal PKI
- Let's Encrypt
**Example structure:**
```bash
/etc/vault.d/tls/

vault.crt
vault.key
ca.crt
```
## 8. Configure Vault (RAFT Storage)
```bash
vi /etc/vault.d/vault.hcl
```
**config:**
```bash
ui = true

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault.d/tls/vault.crt"
  tls_key_file  = "/etc/vault.d/tls/vault.key"
}

storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-node-1"

  retry_join {
    leader_api_addr = "https://vault-node-1:8200"
  }

  retry_join {
    leader_api_addr = "https://vault-node-2:8200"
  }

  retry_join {
    leader_api_addr = "https://vault-node-3:8200"
  }
}

api_addr = "https://vault.service.consul:8200"
cluster_addr = "https://127.0.0.1:8201"

disable_mlock = false
```
## 9. Enable Auto-Unseal with KMS
Create a KMS key in **Amazon Web Services.
**Update config:**
```bash
seal "awskms" {
  region     = "ap-south-1"
  kms_key_id = "xxxxxxxx-xxxx"
}
```
**Attach IAM role to EC2:**
policy
```bash
kms:Encrypt
kms:Decrypt
kms:DescribeKey
```
## 10. Systemd Service
Create service:
```bash
/etc/systemd/system/vault.service
```
```bash
[Unit]
Description=Vault
After=network.target

[Service]
User=vault
Group=vault

ExecStart=/usr/local/bin/vault server -config=/etc/vault.d/vault.hcl

LimitMEMLOCK=infinity
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable vault
sudo systemctl start vault
```
## 11. Initialize Vault
**Run once:**
```bash
vault operator init
```
Outputs:
```bash
Unseal keys
Root token
```


























