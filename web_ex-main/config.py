import secrets

class Config:
    # Генерация и присвоение секретного ключа
    SECRET_KEY = secrets.token_hex(16)  # Генерирует 32-значный шестнадцатеричный ключ
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Для проверки вы можете распечатать сгенерированный ключ
if __name__ == "__main__":
    print(f"Generated SECRET_KEY: {Config.SECRET_KEY}")
