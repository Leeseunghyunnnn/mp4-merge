# import os
import ffmpeg
import aiohttp
import tempfile
import os
from typing import List
import uuid

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def merge_url_videos(urls: List[str]):

    # 다운로드한 파일 내용을 임시 파일에 저장하고, 해당 파일 경로를 리스트에 저장
    input_files = []
    for url in urls:
        file_content = await download_file(url)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            input_files.append(temp_file.name)

    # 임시 파일에 저장된 비디오들을 ffmpeg의 input으로 변환하고, 해상도를 조절
    inputs = [ffmpeg.input(file).filter('scale', 1280, 720) for file in input_files]  # 1280x720 해상도로 조절

    # 모든 입력 파일을 하나의 비디오로 병합
    output = ffmpeg.concat(*inputs)
    # 생성할 파일 이름
    fileName = f'{uuid.uuid4()}.mp4'

    # 병합된 비디오를 output.mp4 파일로 저장
    (
        ffmpeg
        .output(output, fileName, vcodec='libx264', pix_fmt='yuv420p', crf=23, preset='medium', r='30')
        .global_args('-profile:v', 'high', '-level', '4.1')
        .run()
    )

    # 임시 파일 삭제
    for file_path in input_files:
        os.remove(file_path)
    
    return fileName

def get_file_object(file_path: str):
    """
    지정된 경로의 파일을 열고 파일 객체를 반환합니다.
    :param file_path: 파일의 전체 경로
    :return: 열린 파일 객체
    """
    try:
        # 파일을 바이너리 읽기 모드로 열기
        file = open(file_path, 'rb')
        return file
    except FileNotFoundError:
        print("File not found")
        return None
    
# asyncio.run(merge_url_videos(urls))