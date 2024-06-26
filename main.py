import os
from fastapi import FastAPI, Response, HTTPException
from fastapi import status
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List

import sys
import os

# 현재 스크립트의 경로를 기준으로 mp4 폴더의 경로를 추가
current_directory = os.path.dirname(os.path.abspath(__file__))
mp4_directory = os.path.join(current_directory, 'mp4')
sys.path.append(mp4_directory)

from mp4imagecombine import merge_url_videos

app = FastAPI()

class MP4DownloadRequest(BaseModel):
    urls: List[str]  # 클라이언트의 JSON 키와 일치하도록 필드명을 urls로 변경

@app.post("/video/merge")
async def download_mp4(response: Response, request: MP4DownloadRequest):
    mp4_urls = request.urls
     # 다운로드할 MP4 파일의 URL 목록
    try: # mp4파일 병합
        fileName = await merge_url_videos(mp4_urls)
    except Exception as e:
        # 병합중 예외가 발생하면 500 서버 에러 반환
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    file_path = './'
    full_file_path = f"{file_path}{fileName}"

    # 생성한 파일경로 접근하여 데이터 메모리로 할당, 임시로 생성했던 파일은 삭제
    with open(full_file_path, 'rb') as file:  # 'rb'는 바이너리 읽기 모드
        file_content = file.read()
        os.remove(full_file_path)
    
    # 응답 헤더 생성
    headers = {
        "Content-Disposition": f"attachment; filename={fileName}"
    }
    # 파일반환
    return Response(content=file_content, media_type="video/mp4", headers=headers)