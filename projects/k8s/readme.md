## Amazon EKS Multi-AZ: Kubernetes Ingress AWS ALB | 3 Real-World Demos Path, TLS & Subdomain Routing
### Step 1: Provision EKS Cluster
Create a file named eks-config.yaml with the following contents:
```bash
apiVersion: eksctl.io/v1alpha5       # Defines the API version used by eksctl for parsing this config
kind: ClusterConfig                  # Declares the type of resource (an EKS cluster configuration)

metadata:
  name: gaurav-practice            # Name of the EKS cluster to be created
  region: ap-south-1                 # AWS region where the cluster will be deployed (Ohio)
  tags:                             # Custom tags for AWS resources created as part of this cluster
    owner: gaurav              # Tag indicating the owner of the cluster
    bu: clourwarriors                      # Tag indicating business unit or project group
    project: ingress-demo          # Tag for grouping resources under the ingress demo project

availabilityZones:
  - ap-south-1a                      # First availability zone for high availability
  - ap-south-1b                      # Second availability zone to span the cluster

iam:
  withOIDC: true                    # Enables IAM OIDC provider, required for IAM roles for service accounts (IRSA)

managedNodeGroups:
  - name: gaurav-eks-priv-ng          # Name of the managed node group
    instanceType: t3.small          # EC2 instance type for worker nodes
    minSize: 4                      # Minimum number of nodes in the group
    maxSize: 4                      # Maximum number of nodes (fixed at 4 here; no autoscaling)
    privateNetworking: true         # Launch nodes in **private subnets only** (no public IPs)
    volumeSize: 20                  # Size (in GB) of EBS volume attached to each node
    iam:
      withAddonPolicies:           # Enables AWS-managed IAM policies for certain addons
        autoScaler: true           # Allows Cluster Autoscaler to manage this node group
        externalDNS: false         # Disables permissions for ExternalDNS (not used in this demo)
        certManager: yes           # Grants cert-manager access to manage certificates using IAM
        ebs: false                 # Disables EBS volume policy (not required here)
        fsx: false                 # Disables FSx access
        efs: false                 # Disables EFS access
        albIngress: true           # Grants permissions needed by AWS Load Balancer Controller (ALB)
        xRay: false                # Disables AWS X-Ray (tracing not needed)
        cloudWatch: false          # Disables CloudWatch logging from nodes (optional in minimal setups)
    labels:
      lifecycle: ec2-autoscaler     # Custom label applied to all nodes in this group (useful for targeting in node selectors or autoscaler configs)
```
Create the cluster using: (it will take 20-25 min)
```bash
eksctl create cluster -f eks-config.yaml
```
Verify the node distribution across AZs:
```bash
kubectl get nodes --show-labels | grep topology.kubernetes.io/zone
```
