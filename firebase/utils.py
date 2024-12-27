from datetime import timedelta
from .config import storage_firebase
from google.cloud.storage.blob import Blob
from google.cloud.firestore import DocumentReference

class FirebaseHelper:
    @staticmethod
    def list_files_in_folder(folder_name):
        """
        List all files in a specific folder (prefix) in Firebase Storage.

        :param folder_name: The folder/prefix name where the files are stored.
        :return: A list of file paths.
        """
        # Đảm bảo việc truyền max_results là số nguyên
        blobs: Blob = storage_firebase.list_blobs(
            prefix=folder_name, max_results=1000
        )  # Thêm max_results là số nguyên
        file_paths = [blob.name for blob in blobs if not blob.name.endswith("/")]
        return file_paths

    @staticmethod
    def get_file_url(file_path):
        """
        Get the download URL of a file in Firebase Storage.

        :param file_path: The path to the file.
        :return: The download URL of the file.
        """
        blob = storage_firebase.blob(file_path)
        if not blob.exists():
            return None
        return blob.generate_signed_url(expiration=timedelta(days=1000)), "file name"


    @staticmethod
    def upload_file_and_get_url(file: bytes, folder_name: str, file_name: str):
        """
        Upload a file to Firebase Storage and return the download URL.

        :param file: The file to upload as bytes.
        :param folder_name: The folder in Firebase Storage where the file will be uploaded.
        :param file_name: The name of the file (e.g., image.jpg) to be uploaded.
        :return: The download URL of the uploaded file.
        """
        # Định nghĩa đường dẫn trên Firebase Storage
        file_path = f"{folder_name}/{file_name}"

        # Lấy blob object trong Firebase
        blob = storage_firebase.blob(file_path)

        # Upload file dưới dạng bytes
        blob.upload_from_string(file)

        # Tạo URL có thời hạn
        return blob.generate_signed_url(expiration=timedelta(days=9999))
    