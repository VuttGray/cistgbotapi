from json import load
from os import path, environ
from dynaconf import Dynaconf, Validator

config_folder = path.join(environ['LOCALAPPDATA'], 'PythonConfigs')
settings = Dynaconf(settings_files=[path.join(config_folder, 'cistgbotapi.toml')],
                    validators=[
                        Validator("default.tgbot.token",
                                  "default.tgbot.admins",
                                  must_exist=True),
                    ])


def load_json_settings(file_name: str):
    json_path = path.join(config_folder, file_name)
    with open(json_path, 'r', encoding='utf-8') as f:
        return load(f)
