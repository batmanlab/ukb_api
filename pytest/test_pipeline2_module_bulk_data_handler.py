import pytest
from ukb_api import module_bulk_data_handler
import pandas as pd
import os


def test_display_all_categories():
    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    bulk_module_object = module_bulk_data_handler.bulk_data_handler()

    unique_category_file_object = open(static_resource_path + "all_unique_categories.txt", "r")
    all_categories_list = unique_category_file_object.readlines()
    formatted_category_list = [a.rstrip() for a in all_categories_list]

    category_list_from_api = bulk_module_object.display_all_categories()

    assert (set(category_list_from_api) == set(formatted_category_list))


def test_get_field_ids():
    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    bulk_module_object = module_bulk_data_handler.bulk_data_handler()
    temp_field_ids_df = pd.read_csv(static_resource_path + "ukb_field_ids.csv")
    field_ids_from_meta_data = list(temp_field_ids_df[temp_field_ids_df['Category'] ==
                                                      "T1 structural brain MRI"]['Field ID'].unique())

    field_ids_from_api = list(bulk_module_object.get_field_ids_for_category("T1 structural brain MRI")
                              ['Field ID'].unique())

    assert (set(field_ids_from_meta_data) == set(field_ids_from_api))


def test_get_subject_list():
    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    bulk_module_object = module_bulk_data_handler.bulk_data_handler()

    subject_list_from_api = list(bulk_module_object.get_subject_list_field_ids(20252))

    columns_to_read = ["eid", "20252-2.0", "20252-3.0"]

    tempdf = pd.read_csv(static_resource_path + "ukb49570.csv", usecols=columns_to_read)
    tempdf = tempdf.dropna(thresh=2)

    subject_list_from_meta_data = list(tempdf['eid'].unique())

    assert (set(subject_list_from_api) == set(subject_list_from_meta_data))


def test_fetch_bulk_data():

    t1_directory = "/ocean/projects/asc170022p/shared/Data/ukBiobank/datalad_dataset/inputs/brain_imaging_ds/"
    t1_subjects = os.listdir(t1_directory)
    bulk_module_object = module_bulk_data_handler.bulk_data_handler()
    dict_from_api = bulk_module_object.fetch_bulk_data(t1_subjects,"T1_Image")[0]

    bulk_data_dict = {}

    for subject in t1_subjects:
        for data_version in ["20252_2_0", "20252_3_0"]:
            check_path = t1_directory + subject + "/" + data_version + "/T1/T1.nii.gz"
            if os.path.exists(check_path):
                bulk_data_dict[subject] = bulk_data_dict.get(subject, []) + [check_path]


    assert (bulk_data_dict == dict_from_api)







