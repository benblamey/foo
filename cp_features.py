import pathlib
import os
import shutil

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf

# if __name__ != '__main__':
#     import cellprofiler_core.pipeline
#     import cellprofiler_core.preferences
#     import cellprofiler_core.utilities.java

_pipeline = None
CP_OUTPUT_DIR = 'output'

import subprocess
procs = []
if True:
    procs = [subprocess.Popen(["python3","cp_worker_core.py"],
                              stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE,
                              text=True) for i in range(16)]


def cp_features(file_list):
    # global _pipeline
    # if _pipeline is None:
    #     # Cellprofiler feature loss
    #     cellprofiler_core.preferences.set_headless()
    #     cellprofiler_core.utilities.java.start_java()
    #     # os.makedirs('cp/image', exist_ok=True)
    #
    #     os.makedirs(CP_OUTPUT_DIR, exist_ok=True)
    #
    #     _pipeline = cellprofiler_core.pipeline.Pipeline()
    #     _pipeline.load("ExampleNeighbors.cppipe")
    #
    #     cellprofiler_core.preferences.set_default_output_directory(CP_OUTPUT_DIR)

    print(pathlib.Path('.').absolute())
    print(file_list)
    files = [file.as_uri() for file in file_list]

    if len(files) > 0:
        output_pandas = []
        for i, file_path in enumerate(files):
            proc = procs[i]
            output_dir = os.path.join(CP_OUTPUT_DIR, str(i))
            output_pandas.append(os.path.join(output_dir, "Image.csv"))
            allow_cache = 'original' in file_path

            print(output_dir)

            proc.stdin.write(f'{file_path},{output_dir},{allow_cache}\n')
            proc.stdin.flush()

        for i, file_path in enumerate(files):
            # Read one line of output.
            proc = procs[i]
            data = proc.stdout.readline().strip()
            #print(data)


            # shutil.rmtree(output_dir, ignore_errors=True)
            # os.makedirs(output_dir)
            # cellprofiler_core.preferences.set_default_output_directory(output_dir)
            # # clear file list
            # _pipeline.clear_urls()
            # _pipeline.read_file_list([file])
            # output_measurements = _pipeline.run()


        #_pipeline.read_file_list(files)
        #output_measurements = _pipeline.run()
        sim = _read_data(output_pandas)

        # tf.print('running here')
        # tf.print(sim)

        # tf.print(files)
    return sim


def _read_data(output_pandas):
    #cp_df = pd.read_csv("output/Image.csv")
    cp_df = pd.concat([pd.read_csv(filename) for filename in output_pandas])
    cp_df_sim = cp_df.filter(regex='^Count|^Mean|URL_Original', axis=1)
    # tf.print('running here')
    # cellprofiler feature similarity
    res = []

    # relies on tha fact that the images are ordered into 2 consecutive lists, so that orig and decoded pairs have fixed offset.
    for i in range(0,8,2):
        decoded_num = cp_df_sim.iloc[i]['URL_Original'].replace('.', '_').split('_')[-2]
        original_num = cp_df_sim.iloc[i + 1]['URL_Original'].replace('.', '_').split('_')[-2]
        if decoded_num == original_num:
            res.append(cosine_similarity([cp_df_sim.iloc[i, :-1]], [cp_df_sim.iloc[i + 1, :-1]])[0][0])
        else:
            print('the original and decoded image numbers for similarity calculation should match.')
    sim = tf.reduce_mean(res)
    return sim

if __name__ == '__main__':
    #cp_features()
    filenames = [f'output/{i}/Image.csv' for i in range(16)]
    print(filenames)
    _read_data(filenames)