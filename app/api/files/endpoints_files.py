import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.api.files.models_files import FileModel
from app.database.crud import FileCrud
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

    file_for_db = FileModel(filename=up_file.filename, size=up_file.size, directory=file_path)

    with open(f'{file_path}', 'wb') as fl:
        fl.write(file.read())

    result = await FileCrud.add_user_file(file_for_db, token)

    return {'msg': 'file upload'}


# Загрузить несколько файлов
@router.post('/upload_files')
async def upload_files(up_files: list[UploadFile], token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    for up_file in up_files:
        new_dir = BASE_DIR / f'files/{token}'
        new_dir.mkdir(parents=True, exist_ok=True)

        file = up_file.file
        file_path = os.path.join(new_dir, up_file.filename)
        user_file = FileModel
        with open(f'{file_path}', 'wb') as fl:
            fl.write(file.read())

    return {'msg': 'files upload'}


# Скачать файл
# TODO
@router.get('/download_file')
async def download_file(file_id:int ,token: Annotated[str, Depends(oauth2_scheme)]):
    user_file = await FileCrud.get_user_file(file_id=file_id, username=token)
    print(user_file)
    print(user_file.directory)
    print(os.path.exists(str(user_file.directory)))
    if user_file:
        return FileResponse(user_file.directory)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='file not found')



