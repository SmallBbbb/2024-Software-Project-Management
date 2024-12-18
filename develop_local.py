import os
import subprocess
import sys

def run_command(command):
    """执行 shell 命令并打印输出"""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)

def create_virtualenv():
    """创建虚拟环境"""
    print("Creating virtual environment...")
    run_command("python3 -m venv venv")
    print("Virtual environment created.")

def install_requirements():
    """安装项目依赖"""
    print("Installing dependencies...")
    run_command("pip install -r requirements.txt")
    print("Dependencies installed.")

def migrate_database():
    """执行数据库迁移"""
    print("Running database migrations...")
    run_command("python manage.py migrate")
    print("Database migrated.")

def collect_static_files():
    """收集静态文件"""
    print("Collecting static files...")
    run_command("python manage.py collectstatic --noinput")
    print("Static files collected.")

def run_server():
    """启动 Django 开发服务器"""
    print("Starting Django development server...")
    run_command("python manage.py runserver")
    print("Django development server started.")

def deploy():
    """部署 Django 项目到本地"""
    if not os.path.exists('venv'):
        create_virtualenv()

    # 激活虚拟环境
    if os.name == 'nt':
        activate_script = 'venv\\Scripts\\activate.bat'
    else:
        activate_script = 'venv/bin/activate'

    # 激活虚拟环境并安装依赖
    if os.name == 'nt':
        run_command(f"call {activate_script} && pip install -r requirements.txt")
    else:
        run_command(f"source {activate_script} && pip install -r requirements.txt")

    # 执行后续步骤
    migrate_database()
    collect_static_files()
    run_server()

if __name__ == "__main__":
    deploy()
