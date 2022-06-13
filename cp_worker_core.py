import hashlib
import sys
import pathlib
import os
import shutil
import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java

PIPELINE = "ExampleNeighbors.cppipe"

cellprofiler_core.preferences.set_headless()
cellprofiler_core.utilities.java.start_java()

_pipeline = cellprofiler_core.pipeline.Pipeline()
_pipeline.load(PIPELINE)

# cache_dir = os.path.join(".cp_worker_core", PIPELINE)
# os.makedirs(cache_dir, exist_ok=True)


while True:
    line = sys.stdin.readline().rstrip()
    input_file, output_dir, allow_cache = line.split(",")

    # TODO: implement caching.

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    cellprofiler_core.preferences.set_default_output_directory(output_dir)
    # clear file list
    _pipeline.clear_urls()
    _pipeline.read_file_list([input_file])

    output_measurements = _pipeline.run()

    print(f'Done.', flush=True)
