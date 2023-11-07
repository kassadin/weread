import tomlkit


def read_config():
    with open('config.tml', 'r') as config_file:
        return tomlkit.parse(config_file.read())


def update_config(config):
    with open('config.tml', 'w') as config_file:
        config_file.write(tomlkit.dumps(config))


if __name__ == '__main__':
    config = read_config()
    print(config['totalCount'])
    config['totalCount'] = 100
    update_config(config)
    config = read_config()
    print(config['totalCount'])