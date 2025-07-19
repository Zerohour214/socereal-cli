from pyfakefs.fake_filesystem_unittest import Patcher

from src.modules.file_utils import collect_image_files
from src.adapters.csv_writer import write_ocr_results


def test_collect_image_files_on_windows():
    with Patcher() as patcher:
        fs = patcher.fs
        fs.is_windows_fs = True
        fs.path_separator = '\\'
        fs.reset()
        fs.create_dir(r'C:\images')
        fs.create_file(r'C:\images\img1.jpg')
        fs.create_file(r'C:\images\img2.png')

        files = collect_image_files([r'C:\images'])
        assert set(files) == {r'C:\images\img1.jpg', r'C:\images\img2.png'}


def test_write_ocr_results_on_windows():
    with Patcher() as patcher:
        fs = patcher.fs
        fs.is_windows_fs = True
        fs.path_separator = '\\'
        fs.reset()
        out_dir = r'C:\out'
        fs.create_dir(out_dir)
        csv_file = rf'{out_dir}\results.csv'
        results = [(r'C:\images\img1.jpg', 'hello', 'OK')]
        write_ocr_results(results, csv_file)
        with open(csv_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'filename,text,validation' in content
        assert 'img1.jpg' in content

