# Local Testing Instructions

## Prerequisites
- Docker installed on your system.
- Repository cloned locally.

## Steps

1. **Run a Docker Container**:
   - For Ubuntu:
     ```bash
     docker run --rm -it -v $(pwd):/repo ubuntu:latest bash
     ```
   - For Rocky Linux:
     ```bash
     docker run --rm -it -v $(pwd):/repo rockylinux:9 bash
     ```

2. **Set Up the Build Environment**:
   ```bash
   apt update && apt install -y build-essential bc bison flex libssl-dev \
                                libncurses-dev devscripts fakeroot ccache
