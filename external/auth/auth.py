try:
    import gspread
    from google.oauth2.service_account import Credentials
    
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "gspread",
        "google-auth",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ])

    import gspread
    from google.oauth2.service_account import Credentials
    
import os


# Defina as permissões necessárias
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_google_sheets_client():

    # Obter o caminho do arquivo credentials.json
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # Autenticação com suas credenciais
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)

    
    return client
