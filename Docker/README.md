# BuildKit server configuration
turning a single EC2 into a dedicated BuildKit server that supports your multi-language builds with per-language caches. This will use local NVMe storage but is also compatible with optional EBS persistence.

We’ll cover:
- OS and Docker setup
- BuildKit configuration (buildkitd.toml)
- Cache directories per technology
- Buildx builder creation
- Bootstrap command for CI SSH usage
