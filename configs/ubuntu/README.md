### Checklist and Process for Building, Installing, and Configuring Custom Kernels with NVIDIA Drivers

#### **1\. Kernel Source Preparation**

1.  **Clone or access the Linux kernel source**:
    
    `cd /data/src/linux`
    
2.  **Ensure the `.config` file is properly prepared**:
    
    -   Disable signing keys:
        
        `scripts/config --disable SYSTEM_TRUSTED_KEYS scripts/config --disable SYSTEM_REVOCATION_KEYS`
        
    -   Copy a known working config (e.g., from the current kernel):
        
        `cp /boot/config-$(uname -r) .config`
        
3.  **Configure the kernel interactively or update defaults**:
    
    `make oldconfig`
    

#### **2\. Build the Kernel**

1.  Compile the kernel and modules:
    
    `make -j$(nproc) make -j$(nproc) modules`
    
2.  Package the kernel into Debian packages:
    
    `make -j$(nproc) deb-pkg`
    

#### **3\. Install the Kernel**

1.  Install the newly built kernel packages:
    
    `sudo dpkg -i ../linux-*-6.13.0-*`
    

#### **4\. Prepare the Environment**

1.  **Set up kernel headers**:
    
    -   Link headers for DKMS compatibility:
        
        `sudo ln -s /lib/modules/6.13.0-rc2+/build /usr/src/linux-headers-6.13.0-rc2+`
        
    -   Ensure proper configuration is in place:
        
        `sudo cp /boot/config-$(uname -r) /lib/modules/6.13.0-rc2+/build/.config`
        
2.  **Prepare the kernel for module compilation**:
    
    `make modules_prepare`
    

#### **5\. Install and Configure NVIDIA Drivers**

1.  **Remove any existing NVIDIA drivers**:
    
    `sudo apt remove --purge '^nvidia.*' sudo apt autoremove`
    
2.  **Install the appropriate NVIDIA driver**:
    
    -   Use the `.run` installer or package manager:
        
        `sudo ./NVIDIA-Linux-x86_64-550.144.03.run`
        
    -   Optionally:
        
        `sudo apt install nvidia-driver-550`
        
3.  **Verify NVIDIA setup**:
    
    -   Set NVIDIA as the active GPU:
        
        `sudo prime-select nvidia`
        
    -   Check the driver and GPU status:
        
        `nvidia-smi`
        

#### **6\. Update Bootloader and Reboot**

1.  **Update GRUB**:
    
    `sudo update-grub`
    
2.  **Reboot**:
    
    `sudo reboot`
    

#### **7\. Test Configuration**

1.  Confirm kernel is active:
    
    `uname -r`
    
2.  Verify NVIDIA GPU rendering:
    
    `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo | grep "OpenGL renderer"`
    

#### **8\. Additional Considerations**

1.  **Certificate Installation for Ubuntu DKMS**:
    
    -   Install missing Ubuntu certificates for DKMS signing:
        
        `sudo apt install shim-signed mokutil`
        
    -   Use the certificates located at:
        
        `/usr/local/src/debian/canonical-certs.pem`
        
2.  **DKMS Configuration**:
    
    -   Run DKMS autoinstall to ensure modules are built:
        
        `sudo dkms autoinstall`
        
3.  **Nouveau Blacklisting**:
    
    -   Ensure Nouveau is blacklisted to avoid conflicts:
        
        `echo "blacklist nouveau" | sudo tee -a /etc/modprobe.d/blacklist-nouveau.conf sudo update-initramfs -u`
        

* * *

### Summary of Key Commands

```
# Kernel build and installation
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS
make -j$(nproc) && make -j$(nproc) modules && make -j$(nproc) deb-pkg
sudo dpkg -i ../linux-*-6.13.0-*

# Prepare headers
sudo ln -s /lib/modules/6.13.0-rc2+/build /usr/src/linux-headers-6.13.0-rc2+
make modules_prepare

# NVIDIA setup
sudo apt remove --purge '^nvidia.*' && sudo apt autoremove
sudo ./NVIDIA-Linux-x86_64-550.144.03.run
sudo prime-select nvidia
nvidia-smi

# Test rendering
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo | grep "OpenGL renderer"

# Reboot after GRUB update
sudo update-grub
sudo reboot
```
This workflow can now be incorporated into your CI/CD pipeline with minor adjustments for automation. Let me know if you want assistance with scripting or further streamlining! 🚀

