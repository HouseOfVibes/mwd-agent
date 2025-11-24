"""
Google Workspace API Integration
Google Drive, Docs, Gmail for file management and communication
"""

import os
import io
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Note: Google Workspace APIs require OAuth2 authentication
# This module provides the structure - actual auth requires additional setup

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google API client not installed. Install with: pip install google-api-python-client google-auth")


class GoogleWorkspaceClient:
    """Client for Google Workspace APIs (Drive, Docs, Gmail)"""

    def __init__(self):
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', '')
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', '')

        self.credentials = None
        self.drive_service = None
        self.docs_service = None
        self.gmail_service = None

        if GOOGLE_AVAILABLE and self.credentials_path and os.path.exists(self.credentials_path):
            try:
                self.credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=[
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/documents',
                        'https://www.googleapis.com/auth/gmail.compose'
                    ]
                )
                self._init_services()
            except Exception as e:
                logger.error(f"Failed to initialize Google credentials: {e}")

    def _init_services(self):
        """Initialize Google API services"""
        if self.credentials:
            try:
                self.drive_service = build('drive', 'v3', credentials=self.credentials)
                self.docs_service = build('docs', 'v1', credentials=self.credentials)
                self.gmail_service = build('gmail', 'v1', credentials=self.credentials)
            except Exception as e:
                logger.error(f"Failed to initialize Google services: {e}")

    def is_configured(self) -> bool:
        """Check if client is properly configured"""
        return (GOOGLE_AVAILABLE and
                self.credentials is not None and
                self.drive_service is not None)

    # ==========================================================================
    # GOOGLE DRIVE
    # ==========================================================================

    def create_folder(self, name: str, parent_id: str = None) -> Dict[str, Any]:
        """
        Create a folder in Google Drive

        Args:
            name: Folder name
            parent_id: Parent folder ID (optional)

        Returns:
            Created folder info
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_id:
                file_metadata['parents'] = [parent_id]

            folder = self.drive_service.files().create(
                body=file_metadata,
                fields='id, name, webViewLink'
            ).execute()

            return {
                'success': True,
                'folder_id': folder['id'],
                'name': folder['name'],
                'url': folder.get('webViewLink', '')
            }
        except Exception as e:
            logger.error(f"Google Drive create folder error: {e}")
            return {'success': False, 'error': str(e)}

    def create_project_structure(self, project_name: str,
                                parent_id: str = None) -> Dict[str, Any]:
        """
        Create standard project folder structure

        Args:
            project_name: Project name
            parent_id: Parent folder ID

        Returns:
            Created folder structure
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            # Create main project folder
            main_folder = self.create_folder(project_name, parent_id)
            if not main_folder['success']:
                return main_folder

            main_folder_id = main_folder['folder_id']

            # Create subfolders
            subfolders = [
                '01_Strategy',
                '02_Design',
                '03_Content',
                '04_Assets',
                '05_Deliverables',
                '06_Client_Feedback'
            ]

            created_folders = {'main': main_folder}

            for subfolder in subfolders:
                result = self.create_folder(subfolder, main_folder_id)
                if result['success']:
                    created_folders[subfolder] = result

            return {
                'success': True,
                'project_folder_id': main_folder_id,
                'project_folder_url': main_folder['url'],
                'subfolders': created_folders
            }
        except Exception as e:
            logger.error(f"Google Drive create project structure error: {e}")
            return {'success': False, 'error': str(e)}

    def list_files(self, folder_id: str = None,
                   file_type: str = None) -> Dict[str, Any]:
        """
        List files in Drive or folder

        Args:
            folder_id: Folder to list (optional, defaults to root)
            file_type: Filter by MIME type

        Returns:
            List of files
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            query_parts = []

            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")
            if file_type:
                query_parts.append(f"mimeType='{file_type}'")

            query_parts.append("trashed=false")
            query = ' and '.join(query_parts)

            results = self.drive_service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, webViewLink, createdTime, modifiedTime)"
            ).execute()

            files = results.get('files', [])

            return {
                'success': True,
                'files': files,
                'count': len(files)
            }
        except Exception as e:
            logger.error(f"Google Drive list files error: {e}")
            return {'success': False, 'error': str(e)}

    def share_file(self, file_id: str, email: str,
                   role: str = 'reader') -> Dict[str, Any]:
        """
        Share a file or folder

        Args:
            file_id: File/folder ID
            email: Email to share with
            role: Permission role (reader, writer, commenter)

        Returns:
            Share result
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }

            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=True
            ).execute()

            return {
                'success': True,
                'file_id': file_id,
                'shared_with': email,
                'role': role
            }
        except Exception as e:
            logger.error(f"Google Drive share error: {e}")
            return {'success': False, 'error': str(e)}

    def find_folder_by_name(self, folder_name: str, parent_id: str = None) -> Dict[str, Any]:
        """
        Find a folder by name in Google Drive

        Args:
            folder_name: Name of the folder to find
            parent_id: Optional parent folder ID to search within

        Returns:
            Folder info if found
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            query_parts = [
                f"name='{folder_name}'",
                "mimeType='application/vnd.google-apps.folder'",
                "trashed=false"
            ]

            if parent_id:
                query_parts.append(f"'{parent_id}' in parents")

            query = ' and '.join(query_parts)

            results = self.drive_service.files().list(
                q=query,
                pageSize=10,
                fields="files(id, name, webViewLink)"
            ).execute()

            files = results.get('files', [])

            if files:
                folder = files[0]
                return {
                    'success': True,
                    'folder_id': folder['id'],
                    'name': folder['name'],
                    'url': folder.get('webViewLink', '')
                }
            else:
                return {
                    'success': False,
                    'error': f"Folder '{folder_name}' not found"
                }
        except Exception as e:
            logger.error(f"Google Drive find folder error: {e}")
            return {'success': False, 'error': str(e)}

    def upload_file(self, file_content: bytes, file_name: str,
                    mime_type: str, folder_id: str = None) -> Dict[str, Any]:
        """
        Upload a file to Google Drive

        Args:
            file_content: File content as bytes
            file_name: Name for the file
            mime_type: MIME type of the file
            folder_id: Folder to upload to

        Returns:
            Uploaded file info
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            file_metadata = {'name': file_name}

            if folder_id:
                file_metadata['parents'] = [folder_id]

            # Create media upload from bytes
            media = MediaFileUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )

            # For MediaFileUpload with BytesIO, we need to use MediaIoBaseUpload instead
            from googleapiclient.http import MediaIoBaseUpload
            media = MediaIoBaseUpload(
                io.BytesIO(file_content),
                mimetype=mime_type,
                resumable=True
            )

            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, webContentLink'
            ).execute()

            return {
                'success': True,
                'file_id': file['id'],
                'name': file['name'],
                'url': file.get('webViewLink', ''),
                'download_url': file.get('webContentLink', '')
            }
        except Exception as e:
            logger.error(f"Google Drive upload error: {e}")
            return {'success': False, 'error': str(e)}

    def upload_files_batch(self, files: List[Dict], folder_id: str) -> Dict[str, Any]:
        """
        Upload multiple files to Google Drive

        Args:
            files: List of dicts with 'content', 'name', 'mime_type'
            folder_id: Folder to upload to

        Returns:
            Results for all uploads
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        results = []
        for file_data in files:
            result = self.upload_file(
                file_content=file_data['content'],
                file_name=file_data['name'],
                mime_type=file_data['mime_type'],
                folder_id=folder_id
            )
            results.append({
                'name': file_data['name'],
                **result
            })

        successful = sum(1 for r in results if r.get('success'))

        return {
            'success': successful == len(files),
            'total': len(files),
            'successful': successful,
            'failed': len(files) - successful,
            'results': results
        }

    def get_folder_tree(self, folder_id: str, max_depth: int = 2) -> Dict[str, Any]:
        """
        Get folder structure/tree for a Drive folder

        Args:
            folder_id: Root folder ID
            max_depth: How deep to traverse (default 2)

        Returns:
            Folder tree structure
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        def get_children(parent_id: str, depth: int) -> List[Dict]:
            if depth > max_depth:
                return []

            try:
                results = self.drive_service.files().list(
                    q=f"'{parent_id}' in parents and trashed=false",
                    pageSize=100,
                    fields="files(id, name, mimeType, webViewLink, createdTime, modifiedTime)",
                    orderBy="name"
                ).execute()

                items = []
                for file in results.get('files', []):
                    item = {
                        'id': file['id'],
                        'name': file['name'],
                        'type': 'folder' if file['mimeType'] == 'application/vnd.google-apps.folder' else 'file',
                        'url': file.get('webViewLink', ''),
                        'modified': file.get('modifiedTime', '')
                    }

                    # Recurse into folders
                    if item['type'] == 'folder' and depth < max_depth:
                        item['children'] = get_children(file['id'], depth + 1)

                    items.append(item)

                return items
            except Exception as e:
                logger.error(f"Error getting children: {e}")
                return []

        try:
            # Get root folder info
            root = self.drive_service.files().get(
                fileId=folder_id,
                fields="id, name, webViewLink"
            ).execute()

            return {
                'success': True,
                'folder_id': folder_id,
                'name': root.get('name', ''),
                'url': root.get('webViewLink', ''),
                'children': get_children(folder_id, 1)
            }
        except Exception as e:
            logger.error(f"Google Drive get folder tree error: {e}")
            return {'success': False, 'error': str(e)}

    def move_file(self, file_id: str, new_parent_id: str,
                  remove_from_current: bool = True) -> Dict[str, Any]:
        """
        Move a file to a different folder

        Args:
            file_id: File to move
            new_parent_id: Destination folder ID
            remove_from_current: Remove from current parents

        Returns:
            Move result
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            # Get current parents
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='parents, name'
            ).execute()

            previous_parents = ",".join(file.get('parents', []))

            # Move the file
            update_params = {
                'fileId': file_id,
                'addParents': new_parent_id,
                'fields': 'id, name, parents, webViewLink'
            }

            if remove_from_current and previous_parents:
                update_params['removeParents'] = previous_parents

            result = self.drive_service.files().update(**update_params).execute()

            return {
                'success': True,
                'file_id': result['id'],
                'name': result['name'],
                'url': result.get('webViewLink', ''),
                'new_parent': new_parent_id
            }
        except Exception as e:
            logger.error(f"Google Drive move file error: {e}")
            return {'success': False, 'error': str(e)}

    def search_files(self, query: str, folder_id: str = None,
                     file_type: str = None, max_results: int = 50) -> Dict[str, Any]:
        """
        Search for files in Google Drive

        Args:
            query: Search query (searches name and content)
            folder_id: Limit search to this folder and subfolders
            file_type: Filter by type ('image', 'video', 'document', 'folder')
            max_results: Maximum results to return

        Returns:
            Search results
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            query_parts = [f"name contains '{query}'", "trashed=false"]

            if folder_id:
                # Search in folder and all subfolders requires fullText search
                # For now, limit to direct children
                query_parts.append(f"'{folder_id}' in parents")

            if file_type:
                type_map = {
                    'image': "mimeType contains 'image/'",
                    'video': "mimeType contains 'video/'",
                    'document': "(mimeType contains 'document' or mimeType contains 'pdf' or mimeType contains 'text/')",
                    'folder': "mimeType = 'application/vnd.google-apps.folder'"
                }
                if file_type in type_map:
                    query_parts.append(type_map[file_type])

            search_query = ' and '.join(query_parts)

            results = self.drive_service.files().list(
                q=search_query,
                pageSize=max_results,
                fields="files(id, name, mimeType, webViewLink, parents, createdTime, modifiedTime)",
                orderBy="modifiedTime desc"
            ).execute()

            files = []
            for file in results.get('files', []):
                files.append({
                    'id': file['id'],
                    'name': file['name'],
                    'type': 'folder' if file['mimeType'] == 'application/vnd.google-apps.folder' else 'file',
                    'mime_type': file['mimeType'],
                    'url': file.get('webViewLink', ''),
                    'created': file.get('createdTime', ''),
                    'modified': file.get('modifiedTime', '')
                })

            return {
                'success': True,
                'query': query,
                'results': files,
                'count': len(files)
            }
        except Exception as e:
            logger.error(f"Google Drive search error: {e}")
            return {'success': False, 'error': str(e)}

    def rename_file(self, file_id: str, new_name: str) -> Dict[str, Any]:
        """
        Rename a file or folder

        Args:
            file_id: File to rename
            new_name: New name

        Returns:
            Rename result
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            result = self.drive_service.files().update(
                fileId=file_id,
                body={'name': new_name},
                fields='id, name, webViewLink'
            ).execute()

            return {
                'success': True,
                'file_id': result['id'],
                'name': result['name'],
                'url': result.get('webViewLink', '')
            }
        except Exception as e:
            logger.error(f"Google Drive rename error: {e}")
            return {'success': False, 'error': str(e)}

    def delete_file(self, file_id: str, permanent: bool = False) -> Dict[str, Any]:
        """
        Delete a file (move to trash or permanently)

        Args:
            file_id: File to delete
            permanent: If True, permanently delete (not recoverable)

        Returns:
            Delete result
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            if permanent:
                self.drive_service.files().delete(fileId=file_id).execute()
            else:
                # Move to trash
                self.drive_service.files().update(
                    fileId=file_id,
                    body={'trashed': True}
                ).execute()

            return {
                'success': True,
                'file_id': file_id,
                'action': 'deleted' if permanent else 'trashed'
            }
        except Exception as e:
            logger.error(f"Google Drive delete error: {e}")
            return {'success': False, 'error': str(e)}

    def get_recent_files(self, folder_id: str = None, days: int = 7,
                         max_results: int = 20) -> Dict[str, Any]:
        """
        Get recently modified files

        Args:
            folder_id: Limit to this folder
            days: How many days back to look
            max_results: Maximum results

        Returns:
            Recent files
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            from datetime import datetime, timedelta
            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'

            query_parts = [f"modifiedTime > '{cutoff}'", "trashed=false"]

            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")

            results = self.drive_service.files().list(
                q=' and '.join(query_parts),
                pageSize=max_results,
                fields="files(id, name, mimeType, webViewLink, modifiedTime)",
                orderBy="modifiedTime desc"
            ).execute()

            files = []
            for file in results.get('files', []):
                files.append({
                    'id': file['id'],
                    'name': file['name'],
                    'type': 'folder' if file['mimeType'] == 'application/vnd.google-apps.folder' else 'file',
                    'url': file.get('webViewLink', ''),
                    'modified': file.get('modifiedTime', '')
                })

            return {
                'success': True,
                'results': files,
                'count': len(files),
                'days': days
            }
        except Exception as e:
            logger.error(f"Google Drive get recent files error: {e}")
            return {'success': False, 'error': str(e)}

    # ==========================================================================
    # GOOGLE DOCS
    # ==========================================================================

    def create_document(self, title: str,
                       folder_id: str = None) -> Dict[str, Any]:
        """
        Create a new Google Doc

        Args:
            title: Document title
            folder_id: Folder to create in

        Returns:
            Created document info
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            # Create the document
            doc = self.docs_service.documents().create(
                body={'title': title}
            ).execute()

            doc_id = doc['documentId']

            # Move to folder if specified
            if folder_id:
                self.drive_service.files().update(
                    fileId=doc_id,
                    addParents=folder_id,
                    fields='id, parents'
                ).execute()

            return {
                'success': True,
                'document_id': doc_id,
                'title': doc['title'],
                'url': f"https://docs.google.com/document/d/{doc_id}/edit"
            }
        except Exception as e:
            logger.error(f"Google Docs create error: {e}")
            return {'success': False, 'error': str(e)}

    def append_to_document(self, document_id: str,
                          content: str) -> Dict[str, Any]:
        """
        Append text to a Google Doc

        Args:
            document_id: Document ID
            content: Text to append

        Returns:
            Update result
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            # Get document to find end index
            doc = self.docs_service.documents().get(
                documentId=document_id
            ).execute()

            end_index = doc['body']['content'][-1]['endIndex'] - 1

            requests = [
                {
                    'insertText': {
                        'location': {'index': end_index},
                        'text': content
                    }
                }
            ]

            self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()

            return {
                'success': True,
                'document_id': document_id,
                'content_added': len(content)
            }
        except Exception as e:
            logger.error(f"Google Docs append error: {e}")
            return {'success': False, 'error': str(e)}

    def create_deliverable_doc(self, title: str, content: Dict,
                              folder_id: str = None) -> Dict[str, Any]:
        """
        Create a formatted deliverable document

        Args:
            title: Document title
            content: Structured content with sections
            folder_id: Folder to create in

        Returns:
            Created document info
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Google Workspace client not configured'}

        try:
            # Create document
            doc_result = self.create_document(title, folder_id)
            if not doc_result['success']:
                return doc_result

            document_id = doc_result['document_id']

            # Build content string
            text_content = f"\n{title}\n{'=' * len(title)}\n\n"

            for section_title, section_content in content.items():
                text_content += f"\n{section_title}\n{'-' * len(section_title)}\n"

                if isinstance(section_content, list):
                    for item in section_content:
                        text_content += f"  - {item}\n"
                elif isinstance(section_content, dict):
                    for key, value in section_content.items():
                        text_content += f"  {key}: {value}\n"
                else:
                    text_content += f"{section_content}\n"

                text_content += "\n"

            # Add content to document
            self.append_to_document(document_id, text_content)

            return {
                'success': True,
                'document_id': document_id,
                'title': title,
                'url': doc_result['url']
            }
        except Exception as e:
            logger.error(f"Google Docs create deliverable error: {e}")
            return {'success': False, 'error': str(e)}

    # ==========================================================================
    # GMAIL (Placeholder - requires additional OAuth setup for user context)
    # ==========================================================================

    def send_email(self, to: str, subject: str, body: str,
                   cc: List[str] = None) -> Dict[str, Any]:
        """
        Send email via Gmail API

        Note: Requires OAuth2 with user consent for Gmail access

        Args:
            to: Recipient email
            subject: Email subject
            body: Email body (plain text)
            cc: CC recipients

        Returns:
            Send result
        """
        if not self.is_configured() or not self.gmail_service:
            return {
                'success': False,
                'error': 'Gmail API not configured. Requires OAuth2 user consent.'
            }

        # Note: Full implementation requires creating MIME message
        # and using users().messages().send()
        # This is a placeholder showing the structure

        return {
            'success': False,
            'error': 'Gmail send not fully implemented. Requires OAuth2 user flow.',
            'note': 'Use draft_email methods from other AI integrations instead.'
        }

    def create_draft(self, to: str, subject: str,
                    body: str) -> Dict[str, Any]:
        """
        Create email draft

        Args:
            to: Recipient
            subject: Subject
            body: Body

        Returns:
            Draft info
        """
        return {
            'success': False,
            'error': 'Gmail draft creation requires OAuth2 user flow.',
            'suggestion': 'Use Perplexity or OpenAI to draft emails, then copy to Gmail.'
        }
