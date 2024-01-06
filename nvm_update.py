#!/opt/miniconda/bin/python
import requests
import os
import sys
import subprocess


def get_latest_version() -> str:
    response = requests.get(
        "https://api.github.com/repos/nvm-sh/nvm/releases/latest")
    if response.status_code == 200:
        tag_info = response.json()
        if tag_info:
            return tag_info['tag_name'].lstrip("v")
    return None


def get_local_version() -> str:
    nvm_bin = None
    for key, value in os.environ.items():
        if key == 'NVM_DIR':
            nvm_bin = f'. {value}/nvm.sh && nvm --version'
            break
    if not nvm_bin:
        return
    try:
        output = subprocess.check_output(
            nvm_bin, shell=True, stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode().strip()

def upgrade(version:str) :
    os.system(f"curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v{version}/install.sh | bash")


if __name__ == "__main__":
    LOCAL_VERSION = get_local_version()
    LATEST_VERSION = get_latest_version()
    if not LATEST_VERSION:
        print(f'获取最新版本失败')
        sys.exit(0)
    if LOCAL_VERSION == LATEST_VERSION:
        print(f"当前是最新版本: {LATEST_VERSION}")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "--no-dry-run":
        upgrade(LATEST_VERSION)
    else:
        print(f"检测出新版本: {LATEST_VERSION}, 请通过 nvm_upgrade --no-dry-run 进行更新")