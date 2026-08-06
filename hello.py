import os

environment = os.environ.get("APP_ENV", "development")

print("Hello, World!")
print(f"Running in: {environment}")
