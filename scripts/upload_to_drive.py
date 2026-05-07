import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Cấu hình
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = os.environ.get('GDRIVE_FOLDER_ID')
CREDENTIALS_JSON = os.environ.get('GDRIVE_CREDENTIALS')

def authenticate():
	creds_dict = json.loads(CREDENTIALS_JSON)
	return service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

def upload_files():
	creds = authenticate()
	service = build('drive', 'v3', credentials=creds)

	# Lấy danh sách các file .md trong commit mới nhất (ví dụ đơn giản)
	# Trong thực tế, bạn có thể lọc file dựa trên git log
	files = [f for f in os.listdir('.') if f.endswith('.md')]
	
	for file_name in files:
		file_metadata = {
			'name': file_name,
			'parents': [FOLDER_ID],
			'mimeType': 'application/vnd.google-apps.document'
		}
		media = MediaFileUpload(file_name, mimetype='text/markdown')
		
		file = service.files().create(body=file_metadata, media_body=media).execute()
		print(f'Đã upload thành công: {file_name} với ID: {file.get("id")}')

if __name__ == '__main__':
	upload_files()