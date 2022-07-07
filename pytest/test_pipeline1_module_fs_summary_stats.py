import pytest
import pandas as pd
from ukb_api import module_get_fs_summary_stats


def test_function_get_subject_list():
    meta_data_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    summary_stats_object = module_get_fs_summary_stats.summary_stats_fs()
    subject_ids_from_api = summary_stats_object.get_subject_ids()

    with open(meta_data_path + 'UKB_fs_folder_paths_march_2022.csv') as f:
        folder_paths = f.read().splitlines()

    fs_subject_list = []
    for path in folder_paths:
        fs_subject_list.append(path.split("/")[-3])

    subject_ids_from_file = list(set(fs_subject_list))

    assert (set(subject_ids_from_api) == set(subject_ids_from_file))


def test_get_summary_stats():
    summary_stats_object = module_get_fs_summary_stats.summary_stats_fs()
    df_from_api = summary_stats_object.get_freesurfer_summary_stats()

    generated_df = pd.read_csv(meta_data_path+"ukb_basic_demographics_and_summary_stats.csv")

    assert(generated_df.equals(df_from_api))











