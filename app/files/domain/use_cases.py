import io
from pypdf import PdfMerger

class FilesUseCases:
    def __init__(self, token_repo, file_repo, storage_repo):
        self.token_repo = token_repo
        self.file_repo = file_repo
        self.storage = storage_repo

    def _user(self, token):
        data = self.token_repo.get(token)
        if not data:
            raise ValueError("Invalid token")
        return data["email"]

    def list_files(self, token):
        user = self._user(token)
        return self.file_repo.list_by_owner(user)

    def create_file(self, token, meta: dict):
        user = self._user(token)
        return self.file_repo.create(owner=user, meta=meta)

    def get_file(self, token, fid):
        user = self._user(token)
        f = self.file_repo.get(owner=user, fid=fid)
        if f.get("key"):
            f["download_url"] = self.storage.get_presigned_url(f["key"])
        return f

    def delete_file(self, token, fid):
        user = self._user(token)
        f = self.file_repo.get(owner=user, fid=fid)
        if f.get("key"):
            self.storage.delete(f["key"])
        self.file_repo.delete(owner=user, fid=fid)

    def upload_file_content(self, token, fid, upload_file):
        user = self._user(token)
        f = self.file_repo.get(owner=user, fid=fid)
        key = f"{user}/{fid}/{upload_file.filename}"
        self.storage.put(key, upload_file.file, upload_file.content_type)
        self.file_repo.update(owner=user, fid=fid, data={"key": key})

    def merge_pdfs(self, token, file_ids):
        user = self._user(token)
        merger = PdfMerger()

        keys = []
        for fid in file_ids:
            f = self.file_repo.get(owner=user, fid=fid)
            key = f.get("key")
            if not key:
                raise ValueError(f"File {fid} has no content to merge")
            keys.append(key)

        for key in keys:
            data = self.storage.get_object(key)
            merger.append(io.BytesIO(data))

        out_fid = self.file_repo.create(owner=user, meta={"name": "merged.pdf", "description": "merged", "source_ids": file_ids})
        out_key = f"{user}/{out_fid}/merged.pdf"

        buf = io.BytesIO()
        merger.write(buf)
        merger.close()
        buf.seek(0)

        self.storage.put(out_key, buf, "application/pdf")
        self.file_repo.update(owner=user, fid=out_fid, data={"key": out_key})
        return out_fid
