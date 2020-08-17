import sys
import subprocess
import json
import shutil
import os


library = '{{ cookiecutter.include_library }}'

libpaths = {
'SeismicPro': 'https://github.com/gazprom-neft/SeismicPro.git',
'seismiqb': 'https://github.com/gazprom-neft/seismiqb.git',
'petroflow': 'https://github.com/gazprom-neft/petroflow.git',
'batchflow': 'https://github.com/analysiscenter/batchflow.git'
# 'testlib': 'https://github.com/analysiscenter/segy.git',
}


print("initializing git repo ...")
subprocess.run(['git', 'init'])

git_config_user_name = '{{ cookiecutter.git_config_user_name }}'
git_config_user_email = '{{ cookiecutter.git_config_user_email }}'

if git_config_user_name is not "do_not_set":
    subprocess.run(['git', 'config', 'user.name', git_config_user_name])

if git_config_user_email is not "do_not_set":
    subprocess.run(['git', 'config', 'user.email', git_config_user_email])

if library is not "no":

    print("adding submodule", library, "...")

    path = libpaths[library]
    subprocess.run(['git', 'submodule', 'add', path])
    subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'])

    print("copying requirements...")
    shutil.copyfile(os.path.join(library, 'requirements.txt'), 'requirements.txt')


print("adding files to git ...")
subprocess.run(['git', 'add', '*'])
subprocess.run(['git', 'commit', '-m', 'initial commit'])

if '{{ cookiecutter.init_DVC }}' == 'yes':
    print("initializing DVC ...")

    subprocess.run(['dvc', 'init'])

    dvc_cache_dir_mode = '{{ cookiecutter.dvc_cache_dir_mode }}'
    lib_dvc_cache_dir_map = {{ cookiecutter.lib_dvc_cache_dir_map }}

    if dvc_cache_dir_mode == 'custom':
        subprocess.run(['dvc', 'cache', 'dir', '{{ cookiecutter.custom_dvc_cache_dir }}'])
    elif dvc_cache_dir_mode == 'infer' and library in lib_dvc_cache_dir_map:
        subprocess.run(['dvc', 'cache', 'dir', lib_dvc_cache_dir_map[library]])

    subprocess.run(['dvc', 'config', 'cache.protected', 'true'])
    subprocess.run(['dvc', 'config', 'cache.type', 'symlink'])

    subprocess.run(['git', 'add', '*'])
    subprocess.run(['git', 'commit', '-m', 'init DVC'])
