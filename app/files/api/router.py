from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from files.dependency_injection.container import get_files_uc
from authentication.dependency_injection.auth_dependencies import get_current_token

router = APIRouter()

class FileMetaIn(BaseModel):
    name: str
    description: str | None = None

@router.get("")
def list_files(token: str = Depends(get_current_token)):
    try:
        return get_files_uc().list_files(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("")
def create_file(meta: FileMetaIn, token: str = Depends(get_current_token)):
    try:
        fid = get_files_uc().create_file(token, meta.dict())
        return {"file_id": fid}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/{fid}")
def get_file(fid: str, token: str = Depends(get_current_token)):
    try:
        return get_files_uc().get_file(token, fid)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/{fid}")
def delete_file(fid: str, token: str = Depends(get_current_token)):
    try:
        get_files_uc().delete_file(token, fid)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/{fid}")
def upload_content(fid: str, file: UploadFile = File(...), token: str = Depends(get_current_token)):
    try:
        get_files_uc().upload_file_content(token, fid, file)
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

class MergeIn(BaseModel):
    file_ids: list[str]

@router.post("/merge")
def merge_files(payload: MergeIn, token: str = Depends(get_current_token)):
    try:
        out_fid = get_files_uc().merge_pdfs(token, payload.file_ids)
        return {"file_id": out_fid}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
