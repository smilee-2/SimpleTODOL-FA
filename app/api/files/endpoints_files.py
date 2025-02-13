import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from app.api.files.models_files import FileModel
from app.database.crud import FileCrud, UserCrud
from typing import Annotated
from ..auth.depends import oauth2_scheme


router = APIRouter(prefix='/files', tags=['Files'])
BASE_DIR = Path(__file__).parent.parent.parent.parent


# Загрузить один файл
@router.post('/upload_file')
async def upload_file(up_file: UploadFile, token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:

    new_dir = BASE_DIR / f'files/{token}'
    new_dir.mkdir(parents=True, exist_ok=True)

    file = up_file.file
    file_path = os.path.join(new_dir, up_file.filename)

    with open(f'{file_path}', 'wb') as fl:
        fl.write(file.read())

    return {'msg': 'file upload'}


# Загрузить несколько файлов
@router.post('/upload_files')
async def upload_files(up_files: list[UploadFile], token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    for up_file in up_files:
        new_dir = BASE_DIR / f'files/{token}'
        new_dir.mkdir(parents=True, exist_ok=True)

        file = up_file.file
        file_path = os.path.join(new_dir, up_file.filename)

        with open(f'{file_path}', 'wb') as fl:
            fl.write(file.read())

    return {'msg': 'files upload'}


# Скачать файл
# TODO
@router.get('/download_file')
async def download_file(file_id:int ,token: Annotated[str, Depends(oauth2_scheme)]):
    user_file = await FileCrud.get_user_file(file_id=file_id, username=token)
    if user_file:
        return FileResponse(user_file.directory)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='file not found')



