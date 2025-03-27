# 🛠 Troubleshooting Guide

Below are common issues and their solutions.

## ❗ General Errors

### **RuntimeError: CPUAllocator**
### **Model loaded, then paused, then nothing happens**
### **Segmentation Fault**
### **Aborted**
### **Core Dumped**
### **Killed**
### **^C, then quit**
### **adm 2816, then stuck**
### **Connection errored out**
### **Error 1006**
### **WinError 10060**
### **Read timed out**
### **No error, but the console closes instantly**
### **Model loading is extremely slow (more than 1 min)**

📌 **Solution:** All these issues are likely due to **insufficient System Swap**.

## 🔄 System Swap Issues
- Ensure you have **at least 40GB of System Swap**.
- If you have **64GB+ RAM**, you *might* not need swap, but it's still recommended.
- **SSD vs HDD:** If your swap is on an HDD, model loading will be slow. Use an SSD if possible.
- **Windows Users:** Windows 10/11 automatically manages swap if there is 40GB free on your disk.
- **Linux/Mac Users:** Follow the official system documentation to set up swap properly.
- If using an **unofficial Windows version**, verify your swap settings.
- Restart your PC after changing swap settings.

## 🔄 Model Corruption Issues
### **MetadataIncompleteBuffer**
### **PytorchStreamReader failed**
### **Model corrupted**
📌 **Solution:** Fooocus will re-download corrupted models automatically. If the issue persists, manually download the model files.

## 🔄 CUDA & GPU Issues
### **Torch not compiled with CUDA enabled**
### **CUDA kernel errors might be reported later**
### **Found no NVIDIA driver on your system**
### **NVIDIA driver too old**
### **Using Nvidia with 8GB, 6GB, or 4GB VRAM - CUDA Out of Memory**
📌 **Solution:**
1. Ensure you are using the **official Fooocus version**.
2. Upgrade your **Nvidia driver** (must be **53X+**, not 3XX or 4XX).
3. Try **CUDA 11 + Xformers** by replacing the `python_embeded` folder with the one from the [release page](https://github.com/lllyasviel/Fooocus/releases/tag/release).
4. If issues persist, **open a GitHub issue**.

### **I am using AMD GPU on Windows/Linux**
📌 **Solution:**
- AMD support is **experimental**.
- **Windows:** Fooocus may not work on AMD GPUs.
- **Linux:** Slightly better support with **ROCm**.
- If you can run **SDXL on other software**, report it so support can be improved.

## ⚠️ Miscellaneous Issues
### **subprocess-exited-with-error**
📌 **Solution:** Use **Python 3.10** and follow the **official installation guide**.

### **SSL: CERTIFICATE_VERIFY_FAILED**
📌 **Solution:** If in **China**, disable VPN or manually download models. Otherwise, search [Google](https://www.google.com/search?q=SSL+Certificate+Error).

### **Fooocus is suddenly slow**
📌 **Solution:** Ensure you're **not running two instances** of Fooocus simultaneously.

### **I tried flags like --lowvram, --gpu-only, etc., but it’s worse**
📌 **Solution:** Remove these flags; they often introduce more problems than they solve.

---
❓ Still facing issues? **Open an issue on GitHub** with detailed logs for better support!