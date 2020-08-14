import sys


def validate_custom_dvc_cache_dir():
    dvc_cache_dir_mode = '{{ cookiecutter.dvc_cache_dir_mode }}'
    custom_dvc_cache_dir = '{{ cookiecutter.custom_dvc_cache_dir }}'
    if dvc_cache_dir_mode == 'custom' and custom_dvc_cache_dir == 'pass':
        raise ValueError("You chose custom dvc cache dir but did not specify it")


def validate_infer_dvc_cache_dir():
    dvc_cache_dir_mode = '{{ cookiecutter.dvc_cache_dir_mode }}'
    library = '{{ cookiecutter.include_library }}'
    lib_dvc_cache_dir_map = {{ cookiecutter.lib_dvc_cache_dir_map }}

    if dvc_cache_dir_mode == 'infer' and library not in lib_dvc_cache_dir_map:
        msg = (
            "Dvc cahe dir can be inferred only for {},".format(', '.join(lib_dvc_cache_dir_map.keys())),
            "but you selected include_library == {}".format(library)
        )
        raise ValueError(" ".join(msg))


validators = (
    validate_custom_dvc_cache_dir,
    validate_infer_dvc_cache_dir,
)

for validator in validators:
    try:
        validator()
    except ValueError as ex:
        print(ex)
        sys.exit(1)
