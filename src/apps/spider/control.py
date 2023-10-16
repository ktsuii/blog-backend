import os
import pathlib
from datetime import datetime
from zipfile import ZipFile

from flask import stream_with_context, make_response

from settings import Config

from spiders.crawler_base import Crawler
from database.mysql.model.spider import Wallpaper


def crawl_wallpaper(session, crawlor: Crawler, keyword: str):
    """
    爬取指定关键词的壁纸
    :param session: 数据库连接
    :param crawlor: 爬虫器
    :param keyword: 爬取关键词
    :return:
    """
    dirname = datetime.now().strftime("%Y%m%d%H%M%S")
    directory_path = pathlib.Path(Config.ZZZMH_SAVE_DIR, str(dirname))
    pictures = crawlor.zzzmh.run(keyword=keyword, max_page=1, save_dir=directory_path)
    session.add_all([Wallpaper(**pic) for pic in pictures])
    session.commit()

    zip_path = pathlib.Path(Config.ZZZMH_SAVE_DIR).joinpath(f'{dirname}.zip')

    with ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))

    bytes_data = stream_download(zip_path)

    response = make_response(stream_with_context(bytes_data))
    response.headers.set('Content-Disposition', 'attachment', filename=f'{dirname}.zip')
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Transfer-Encoding', 'binary')

    return response


def stream_download(file_path: pathlib.Path, buffer_size=1024 * 4):
    """
    流式下载
    :param file_path: 文件路径
    :param buffer_size: 缓冲区大小
    :return:
    """
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            yield data
