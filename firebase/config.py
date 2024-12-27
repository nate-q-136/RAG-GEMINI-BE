import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin.firestore
import os
from dotenv import load_dotenv
load_dotenv()

if not firebase_admin._apps:
    credentials_firebase = credentials.Certificate(os.getenv("FIREBASE_KEY"))
    firebase_admin.initialize_app(
        credentials_firebase, {"storageBucket": "chat-app-react-cc93a.appspot.com"}
    )
storage_firebase = storage.bucket()
firestore_db = firebase_admin.firestore.client()


class FirebaseConfig:
    storage_file_collection = "files_gemini"