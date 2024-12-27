from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework import status

from rag_gemini_backend.backend.exceptions import BadRequest, ValidationError
from rag_gemini_backend.backend.response import CustomResponse

from firebase.utils import FirebaseHelper
from firebase.config import FirebaseConfig

# Create your views here.
class UploadFileViewSet(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request: Request):
        try:
            files = request.data.getlist("files")
            if not files:
                raise ValidationError("Files are required")
            urls = []
            for file in files:
                file_bytes = file.read()
                file_name = file.name
                url = FirebaseHelper.upload_file_and_get_url(
                    file_bytes, FirebaseConfig.storage_file_collection, file.name
                )
                urls.append({
                    "url": url,
                    "file_name": file_name
                })
            
            return CustomResponse(urls, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            raise BadRequest(str(e))
        pass
