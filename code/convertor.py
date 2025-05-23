import config
import subprocess
import multiprocessing
from pathlib import Path


def convert(file_path):
    process = multiprocessing.Process(target=pandoc_process, args=(file_path,))
    process.start()


def pandoc_process(file_path):
    name = Path(file_path).stem
    cmd = f"pandoc '{file_path}' -o '{config.cache_dir}{name}.pdf'; pdftoppm '{config.cache_dir}{name}.pdf' '{config.cache_dir}{name}' -png"
    subprocess.run(cmd, shell=True, check=True)
