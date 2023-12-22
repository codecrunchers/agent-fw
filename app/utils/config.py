# Configuration class or method
def get_environment_config():
    # Logic to determine the environment and get config
    return {
        "db_type": "dev",
        "db_uri": "sqlite:///Chinook.db",
        "file_loader_type": "unstructured",
    }
