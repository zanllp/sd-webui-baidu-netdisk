import urllib.request
import zipfile
import os
import platform
from scripts.baidu_netdisk.tool import cwd,is_win
bin_file_name = "BaiduPCS-Go.exe" if is_win else "BaiduPCS-Go"
bin_file_path = os.path.join(cwd, bin_file_name)

import hashlib

class IncorrectHashException(Exception):
    pass

def get_file_hash(filename):
    hash_obj = hashlib.sha256()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            hash_obj.update(data)
    return hash_obj.hexdigest()

def check_hash(filename, expected):
    actual = get_file_hash(filename).lower()
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
            file_name, hash = "BaiduPCS-Go-v3.9.0-darwin-osx-amd64", "a08132e44d0cd66881768c23a5f87dd16abbade8f252684ff5868bce01531433"
        elif machine == "arm64":
            file_name, hash = "BaiduPCS-Go-v3.9.0-darwin-osx-arm64", "f75bb12cac9cb58682b478f100248fe61198435511a407c92a09de375221d36e"
    elif system == "Linux":
        if machine == "i386":
            file_name, hash = "BaiduPCS-Go-v3.9.0-linux-386", "9742f84715528000d3a4095eb620fe2aff71d08563f5773350e7e829f04e89cf"
        elif machine == "x86_64":
            file_name, hash = "BaiduPCS-Go-v3.9.0-linux-amd64", "5510e85f2b863c98ecb6c481b8f76d3b06e7685982e0251e23e9116509a14d8d"
    elif system == "Windows":
        if machine == "AMD64":
            file_name, hash = "BaiduPCS-Go-v3.9.0-windows-x64", "1f4220b41bd49984e0e088e5491da4dee4f9520da18ad68a872245369a1eb25e"
        elif machine == "x86":
            file_name, hash = "BaiduPCS-Go-v3.9.0-windows-x86", "4344449c3e8e531955b677ef9136846b00e51523adaf3e28370cef4ae555fc5d"
    if not file_name:
        raise Exception(f"找不到对应的文件，请携带此信息找开发者 machine:{machine} system:{system}")
    return file_name, f"https://github.com/qjfoidnh/BaiduPCS-Go/releases/download/v3.9.0/{file_name}.zip", f"http://static.zanllp.cn/{file_name}.zip", hash


def download_bin_file():
    summary, url, fallback_url, hash = get_matched_summary()

    # 下载文件保存路径
    download_path = "BaiduPCS-Go.zip"

    try:
    # 下载文件并保存
        urllib.request.urlretrieve(url, download_path)
        check_hash(download_path, hash)
    except:
        urllib.request.urlretrieve(fallback_url, download_path)
        check_hash(download_path, hash)

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


