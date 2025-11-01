import os


class Config:
    """Configuration settings for the Flask application"""

    # Secret key for session management
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'your-secret-key-change-in-production'

    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes in seconds

    # File paths
    DATA_DIR = 'data'
    ENCODINGS_FILE = os.path.join(DATA_DIR, 'face_encodings.pkl')
    USERS_FILE = os.path.join(DATA_DIR, 'users.pkl')

    # Facial recognition settings
    FACE_DETECTION_MODEL = 'hog'  # or 'cnn' for better accuracy (requires GPU)
    TOLERANCE = 0.6
    FACE_ENCODINGS_PATH = 'models'

    # Camera settings
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
