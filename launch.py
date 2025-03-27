import os
import ssl
import sys
import platform

# Print system arguments
print(f'[System ARGV] {sys.argv}')

# Set the root directory
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

# Set environment variables for PyTorch
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
os.environ.setdefault("GRADIO_SERVER_PORT", "7865")

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

import fooocus_version
from build_launcher import build_launcher
from modules.launch_util import (
    is_installed, run, python, run_pip, requirements_met, delete_folder_content
)
from modules.model_loader import load_file_from_url

# Configuration flags
REINSTALL_ALL = False
TRY_INSTALL_XFORMERS = False


def prepare_environment():
    """Prepare the runtime environment by installing dependencies."""
    torch_index_url = os.getenv('TORCH_INDEX_URL', "https://download.pytorch.org/whl/cu121")
    torch_command = os.getenv('TORCH_COMMAND',
                              f"pip install torch==2.1.0 torchvision==0.16.0 --extra-index-url {torch_index_url}")
    requirements_file = os.getenv('REQS_FILE', "requirements_versions.txt")

    print(f"Python {sys.version}")
    print(f"Fooocus version: {fooocus_version.version}")

    if REINSTALL_ALL or not is_installed("torch") or not is_installed("torchvision"):
        run(f'"{python}" -m {torch_command}', "Installing torch and torchvision", "Couldn't install torch", live=True)

    if TRY_INSTALL_XFORMERS and (REINSTALL_ALL or not is_installed("xformers")):
        xformers_package = os.getenv('XFORMERS_PACKAGE', 'xformers==0.0.23')
        if platform.system() == "Windows" and platform.python_version().startswith("3.10"):
            run_pip(f"install -U -I --no-deps {xformers_package}", "xformers", live=True)
        elif platform.system() == "Linux":
            run_pip(f"install -U -I --no-deps {xformers_package}", "xformers")
        else:
            print("xformers installation is not supported on this version of Python.")

    if REINSTALL_ALL or not requirements_met(requirements_file):
        run_pip(f"install -r \"{requirements_file}\"", "requirements")


def ini_args():
    """Initialize and return script arguments."""
    from args_manager import args
    return args


prepare_environment()
build_launcher()
args = ini_args()

# Configure GPU settings if specified
if args.gpu_device_id is not None:
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_device_id)
    print("Set device to:", args.gpu_device_id)

if args.hf_mirror is not None:
    os.environ['HF_MIRROR'] = str(args.hf_mirror)
    print("Set hf_mirror to:", args.hf_mirror)

from modules import config
from modules.hash_cache import init_cache

# Set environment paths
os.environ["U2NET_HOME"] = config.path_inpaint
os.environ['GRADIO_TEMP_DIR'] = config.temp_path

# Cleanup temp directory if enabled
if config.temp_path_cleanup_on_launch:
    print(f'[Cleanup] Deleting content of temp dir {config.temp_path}')
    if delete_folder_content(config.temp_path, '[Cleanup] '):
        print("[Cleanup] Cleanup successful")
    else:
        print("[Cleanup] Cleanup failed.")


def download_models():
    """Download required models if not already present."""
    from modules.util import get_file_from_folder_list

    vae_approx_filenames = [
        ('xlvaeapp.pth', 'https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth'),
        ('vaeapp_sd15.pth', 'https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt'),
        ('xl-to-v1_interposer-v4.0.safetensors',
         'https://huggingface.co/mashb1t/misc/resolve/main/xl-to-v1_interposer-v4.0.safetensors')
    ]

    for file_name, url in vae_approx_filenames:
        load_file_from_url(url=url, model_dir=config.path_vae_approx, file_name=file_name)

    load_file_from_url(
        url='https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin',
        model_dir=config.path_fooocus_expansion,
        file_name='pytorch_model.bin'
    )

    if args.disable_preset_download:
        print('Skipped model download.')
        return

    default_model = config.default_base_model_name
    checkpoint_downloads = config.checkpoint_downloads

    for file_name, url in checkpoint_downloads.items():
        model_dir = os.path.dirname(get_file_from_folder_list(file_name, config.paths_checkpoints))
        load_file_from_url(url=url, model_dir=model_dir, file_name=file_name)


download_models()
config.update_files()
init_cache(config.model_filenames, config.paths_checkpoints, config.lora_filenames, config.paths_loras)

from webui import *
