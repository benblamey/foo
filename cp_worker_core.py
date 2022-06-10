import sys
import pathlib
import os
import shutil
import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java

cellprofiler_core.preferences.set_headless()
cellprofiler_core.utilities.java.start_java()

_pipeline = cellprofiler_core.pipeline.Pipeline()
_pipeline.load("ExampleNeighbors.cppipe")

while True:
    line = sys.stdin.readline().rstrip()
    input_file, output_dir = line.split(",")

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    cellprofiler_core.preferences.set_default_output_directory(output_dir)
    # clear file list
    _pipeline.clear_urls()
    _pipeline.read_file_list([input_file])

    output_measurements = _pipeline.run()

    print(f'Done.', flush=True)
