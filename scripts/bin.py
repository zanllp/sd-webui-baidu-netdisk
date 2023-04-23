import urllib.request
import zipfile
import os
import platform
from scripts.tool import cwd,is_win
bin_file_name = "BaiduPCS-Go.exe" if is_win else "BaiduPCS-Go"
bin_file_path = os.path.join(cwd, bin_file_name)

import hashlib

class IncorrectHashException(Exception):
    pass

def check_hash(filename, expected):
    with open(filename, "rb") as f:
        actual = hashlib.file_digest(f, "sha256").hexdigest().lower()
    if expected.lower() != actual:
        raise IncorrectHashException("Incorrect hash for download!\n" +
            f"Expected: {expected}\n" +
            f"Actual:   {actual}")

def check_bin_exists():
    return os.path.exists(bin_file_path)


def get_matched_summary():
    system = platform.system()
    machine = platform.machine()
    if system == "Darwin":
        if machine == "x86_64":
            file_name = "BaiduPCS-Go-v3.9.0-darwin-osx-amd64"
        elif machine == "arm64":
            file_name = "BaiduPCS-Go-v3.9.0-darwin-osx-arm64"
    elif system == "Linux":
        if machine == "i386":
            file_name = "BaiduPCS-Go-v3.9.0-linux-386"
        elif machine == "x86_64":
            file_name = "BaiduPCS-Go-v3.9.0-linux-amd64"
    elif system == "Windows":
        if machine == "AMD64":
            file_name = "BaiduPCS-Go-v3.9.0-windows-x64"
        elif machine == "x86":
            file_name = "BaiduPCS-Go-v3.9.0-windows-x86"
    if not file_name:
        raise Exception(f"找不到对应的文件，请携带此信息找开发者 machine:{machine} system:{system}")
    return file_name, f"https://github.com/qjfoidnh/BaiduPCS-Go/releases/download/v3.9.0/{file_name}.zip", f"http://static.zanllp.cn/{file_name}.zip"


def download_bin_file():
    summary, url, fallback_url = get_matched_summary()

    # 下载文件保存路径
    download_path = "BaiduPCS-Go.zip"

    try:
    # 下载文件并保存
        urllib.request.urlretrieve(url, download_path)
    except:
        urllib.request.urlretrieve(fallback_url, download_path)

    # 解压缩
    with zipfile.ZipFile(download_path, "r") as zip_ref:
        zip_ref.extractall()

    # 移动文件夹到当前目录下
    os.rename(os.path.join(summary, bin_file_name), bin_file_path)
    try:
        os.chmod(bin_file_path, 0o755) # unix only
    except Exception:
        pass
    # 删除下载的压缩包和空的文件夹
    os.remove(download_path)
    os.remove(os.path.join(summary, "README.md"))
    os.rmdir(summary)


