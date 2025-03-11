import os
import ast
import subprocess
import importlib.util

# 配置 pip 镜像地址，这里以阿里云镜像为例
PIP_MIRROR = 'https://mirrors.aliyun.com/pypi/simple/'
# 路径(默认当前路径)
INSTALL_DIRECTORY = '.'


# 定义一个函数来更新 pip
def update_pip():
    try:
        print("Checking for pip updates...")
        subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip', '-i', PIP_MIRROR])
        print("pip has been updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating pip: {e}")


# 定义一个函数来提取 Python 文件中的导入包名
def extract_imports(file_path):
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return imports


# 定义一个函数来扫描当前目录及子目录下的所有 Python 文件
def scan_directory(directory='.'):
    all_imports = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = extract_imports(file_path)
                all_imports.extend(imports)
    return set(all_imports)


# 判断是否为标准库模块
def is_standard_library(module_name):
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            if spec.origin is not None and 'site-packages' not in spec.origin:
                return True
    except ImportError:
        pass
    return False


# 定义一个函数来检查包是否已经安装
def check_packages_installed(packages):
    installed_packages = subprocess.check_output(['pip', 'list']).decode('utf-8')
    not_installed = []
    for package in packages:
        if package not in installed_packages and not is_standard_library(package):
            not_installed.append(package)
    return not_installed


# 定义一个函数来安装缺失的包
def install_packages(packages):
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call(['pip', 'install', package, '-i', PIP_MIRROR])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
        except KeyboardInterrupt:
            print("Installation interrupted by user. Exiting...")
            break


if __name__ == "__main__":
    # 更新 pip
    update_pip()
    # 扫描当前目录及子目录下的所有 Python 文件，提取导入的包名
    all_imports = scan_directory(INSTALL_DIRECTORY)
    # 检查这些包是否已经安装
    not_installed = check_packages_installed(all_imports)
    if not_installed:
        print("The following packages are not installed:")
        for pkg in not_installed:
            print(pkg)
        # 安装缺失的包
        install_packages(not_installed)
    else:
        print("All required packages are already installed.")