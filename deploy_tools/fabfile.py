import random
from string import ascii_letters, digits
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run



REPO_URL = "https://github.com/mannotrobot/studyTDD.git"



def _create_directory_structure_if_necessary(site_folder):
    """создать структуру каталога, если нужно"""
    for subfolder in ("database", 'static', 'virtualenv', 'source'):
        #run(f'mkdir -p {site_folder}/{subfolder}')
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """получить самый свежий исходный код"""
    if exists(source_folder + "/.git"):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    """обновить настройки"""
    setting_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = TRUE", "DEBUG = FALSE")
    sed(setting_path,
        'ALLOWED_HOSTS =.+$',
        f'ALOWED_HOSTS = ["{site_name}"]',
        )

    secret_key_file = source_folder + '/superlists_secret_key.py/'
    if not exits(secret_key_file):
        chars = ascii_letters + digits + '!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtuaenv(source_folder):
    """обновить виртуальную среду"""
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.10 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder} requirements.txt')


def _update_static_files(source_folder):
    """обновить статические файлы"""
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    """обновить базу данных"""
    run(
        f' && ../virtualenv/bin/python manage.py migrate --noinput'
    )


def deploy():
    """развернуть"""
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


