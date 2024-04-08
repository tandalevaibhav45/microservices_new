import subprocess
def run_django_project(port,path):
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'Chat_GPT_API.settings'
    subprocess.Popen(['python', path, 'runserver', f'127.0.0.1:{port}'])

if __name__ == "__main__":
    # Define ports for each Django project
    ports = {8000:r"D:\djangofile\microservice_project\user_authentication_microservices\user_login\manage.py",
             8001:r"D:\djangofile\microservice_project\user_authentication_microservices\user_register\manage.py",
             8003:r"D:\djangofile\microservice_project\user_authentication_microservices\acc_info_update\manage.py",
             8002:r"D:\djangofile\microservice_project\user_authentication_microservices\reset_password\manage.py"}  # Add more ports if needed
    
    # Run each Django project in a separate subprocess
    for port,path in ports.items():
        run_django_project(port,path)