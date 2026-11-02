import os


def get_environment():
    return os.environ.get("APP_ENV", "development")


def get_version():
    return os.environ.get("APP_VERSION", "dev")


def build_message(environment, version):
    return f"Hello, World!\nRunning in: {environment}\nVersion: {version}"


def main():
    print(build_message(get_environment(), get_version()))


if __name__ == "__main__":
    main()
