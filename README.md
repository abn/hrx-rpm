# hrx-rpm

Fedora RPM packages for [HRX (Hip Runtime Extended)](https://github.com/ROCm/hrx-system), a low-latency, high-performance runtime substrate for AMD NPU, GPU, and CPU devices.

The source is integrated via git submodule from [ROCm/hrx-system](https://github.com/ROCm/hrx-system).

## Packages

This repository produces the following RPM packages:

* **`hrx`**: Core runtime library (`libhrx.so`) and diagnostic tool (`hrx-info`).
* **`hrx-devel`**: Development headers (`/usr/include/hrx/`) and CMake package targets (`hrx::hrx`) for building consumers like FastFlowLM.
* **`hrx-hip`**: HIP runtime compatibility layer (`libamdhip64.so`) for executing HIP kernels on the HRX streaming backend.

## Installation

These packages target Fedora 44+ and are published to COPR:

```bash
# Enable the COPR repository
sudo dnf copr enable abn/amd-npu

# Install the HRX runtime
sudo dnf install hrx

# Install development headers for building FastFlowLM
sudo dnf install hrx-devel
```

## Usage

Verify device detection and runtime initialization:

```bash
hrx-info
```

## Development

This project uses [tito](https://github.com/rpm-software-management/tito) for versioning and package release management.

### Containerized Builds (Recommended)

To compile the RPM package inside the `quay.io/abn/rpmbuilder:fedora-44` container:

1. **Start the builder container**:
   ```bash
   podman run -d --rm -i --name rpmbuilder-hrx \
     -v ${PWD}:/sources:z \
     quay.io/abn/rpmbuilder:fedora-44 sleep inf
   ```

2. **Run tito build**:
   ```bash
   podman exec rpmbuilder-hrx rpmbuilder
   ```

3. **Copy output RPMs**:
   Output RPMs are placed in the container `/output/` folder and can be copied back:
   ```bash
   podman cp rpmbuilder-hrx:/output/. ./output/
   ```

4. **Clean up container**:
   ```bash
   podman stop rpmbuilder-hrx
   ```

### Tagging a Release

To tag a new version:
```bash
tito tag
```

> **Note**: As per Tito rules, commit all spec changes to git prior to testing or tagging. Do not manually edit the `%changelog` section; let `tito tag` generate release entries automatically.
