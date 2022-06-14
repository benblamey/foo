import hashlib
import sys
import pathlib
import shutil
import os
from urllib.parse import urlparse

import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java

PIPELINE = sys.argv[1]

cellprofiler_core.preferences.set_headless()
cellprofiler_core.utilities.java.start_java()

_pipeline = cellprofiler_core.pipeline.Pipeline()
_pipeline.load(PIPELINE)

cache_dir_root = os.path.join("cp_worker_core_cache", PIPELINE)
os.makedirs(cache_dir_root, exist_ok=True)

while True:
    line = sys.stdin.readline().rstrip()
    input_file_uri, output_dir, allow_cache = line.split(",")
    allow_cache = allow_cache == 'True'

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    if allow_cache:
        sys.stderr.write(input_file_uri)
        input_file_uri_parsed = urlparse(input_file_uri)
        input_file_path = os.path.abspath(os.path.join(input_file_uri_parsed.netloc, input_file_uri_parsed.path))

        hash = hashlib.md5(pathlib.Path(input_file_path).read_bytes()).hexdigest()
        cache_dir = os.path.join(cache_dir_root, hash)
        if os.path.isdir(cache_dir):
            # instead of running CP, copy the cached files to the output dir.
            shutil.copytree(cache_dir, output_dir, dirs_exist_ok=True)
            print(f'Done (from cache).', flush=True)
            continue

    cellprofiler_core.preferences.set_default_output_directory(output_dir)
    # clear file list
    _pipeline.clear_urls()
    _pipeline.read_file_list([input_file_uri])

    output_measurements = _pipeline.run()

    if allow_cache:
        shutil.copytree(output_dir, cache_dir)

    print(f'Done.', flush=True)