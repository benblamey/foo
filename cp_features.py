import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
import subprocess


CP_OUTPUT_DIR = 'output'

procs = []
if True:
    procs = [subprocess.Popen(["python3", "cp_worker_core.py", "ExampleNeighbors.cppipe"],
                              stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE,
                              text=True) for i in range(16)]


def cp_features(file_list):
    #print(pathlib.Path('.').absolute())
    #print(file_list)
    file_uris = [file.as_uri() for file in file_list]

    if len(file_uris) > 0:
        output_pandas = []
        for i, file_uri in enumerate(file_uris):
            proc = procs[i]
            output_dir = os.path.join(CP_OUTPUT_DIR, str(i))
            output_pandas.append(os.path.join(output_dir, "Image.csv"))
            allow_cache = 'original' in file_uri

            #print(output_dir)

            proc.stdin.write(f'{file_uri},{output_dir},{allow_cache}\n')
            proc.stdin.flush()

        for i, file_uri in enumerate(file_uris):
            # Read one line of output.
            proc = procs[i]
            line = proc.stdout.readline().strip()
            # print(line)

        sim = _read_data(output_pandas)

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
            res.append(cosine_similarity([cp_df_sim.iloc[i, :-1]],
                                         [cp_df_sim.iloc[i + 1, :-1]])[0][0])
        else:
            raise 'the original and decoded image numbers for similarity calculation should match.'
    sim = tf.reduce_mean(res)
    return sim

if __name__ == '__main__':
    #cp_features()
    filenames = [f'output/{i}/Image.csv' for i in range(16)]
    print(filenames)
    _read_data(filenames)