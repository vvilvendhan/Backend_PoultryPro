import os
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path




SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

}



# API_KEY
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework_api_key.permissions.HasAPIKey',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'account.authentication.SessionAwareJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


AUTH_USER_MODEL = 'account.User'