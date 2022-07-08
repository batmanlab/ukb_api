import pytest
import os
from ukb_api import module_scalar_data_handler
import pandas as pd

def test_display_all_categories():
    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    scalar_module_object = module_scalar_data_handler.scalar_data_handler()

    unique_category_file_object = open(static_resource_path + "all_unique_categories.txt", "r")
    all_categories_list = unique_category_file_object.readlines()
    formatted_category_list = [a.rstrip() for a in all_categories_list]

    category_list_from_api = scalar_module_object.display_all_categories()

    assert (set(category_list_from_api) == set(formatted_category_list))


def test_get_subject_list():
    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    scalar_module_object = module_scalar_data_handler.scalar_data_handler()

    subject_list_from_api = list(scalar_module_object.get_subject_list_field_ids(21000))

    columns_to_read = ["eid", "21000-0.0","21000-1.0", "21000-2.0"]

    tempdf = pd.read_csv(static_resource_path + "ukb49570.csv", usecols=columns_to_read)
    tempdf = tempdf.dropna(thresh=2)

    subject_list_from_meta_data = list(tempdf['eid'].unique())

    assert (set(subject_list_from_api) == set(subject_list_from_meta_data))

def test_get_data_scalar():

    static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
    scalar_module_object = module_scalar_data_handler.scalar_data_handler()
    test_subjects = list(scalar_module_object.get_subject_list_field_ids(21000))[:100]

    columns_to_read = ["eid", "21000-0.0"]

    tempdf = pd.read_csv(static_resource_path + "ukb49570.csv", usecols=columns_to_read)
    tempdf = tempdf.set_index('eid')
    values_from_meta_data = list(tempdf[tempdf.index.isin(test_subjects)]["21000-0.0"].unique())


    df_from_api = scalar_module_object.get_data_scalar([21000],test_subjects)
    values_from_api = list(df_from_api['21000-0.0'].unique())

    assert(set(values_from_meta_data) == set(values_from_api))









