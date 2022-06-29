import os
from difflib import get_close_matches
import pandas as pd

static_resource_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
T1_directory = "/ocean/projects/asc170022p/shared/Data/ukBiobank/datalad_dataset/inputs/brain_imaging_ds/"
Freesurfer_directory = "/ocean/projects/asc170022p/tighu/UKB_Freesurfer_March2022/"


class bulk_data_handler:
    """

    A class to represent family of methods that can to read and fetch bulk
    data.

    """

    def __init__(self):
        self.columns_to_read_for_field_id = []
        return

    def display_all_categories(self):
        """Utility function which lets user see all the major categories
        present in the UKB dataset. Reads categories from a static resource
        file.


        Args:
            None: No parameter required for this function.


        Returns:
            List of strings which represent all the data categories
            present in the UKB dataset.

        Example:
            api_object.display_all_categories()

        """

        unique_category_file_object = open(static_resource_path+"all_unique_categories.txt", "r")
        all_categories_list = unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return formatted_category_list

    def get_field_ids_for_category(self, category_name=None):
        """A utility function which lets user see the associated field ids for
        each category, reads from a static file containing all the category
        names and field ids.

        Args:
            category_name: A string representing a category name.

        Returns:
            A pandas object having related field ids of the input category.

        Example:
            api_object.get_field_ids_for_category("T1 Brain Imaging")
        """

        temp_field_ids_df = pd.read_csv(static_resource_path+"ukb_field_ids.csv")
        return temp_field_ids_df[temp_field_ids_df['Category'] == category_name]

    def get_subject_list_field_ids(self, field_id=None):
        """A helper function which lets user see subjects having data related
        to a field_id. Reads a metadata file into a pandas object, only reading
        relevant columns because of size of the csv file.

        Args:
            field_id: A int representing a field id.

        Returns:
            A list of subject ids associated with the input field id.

        Example:
            api_object.get_subject_list_field_ids(20252)

        """

        with open(static_resource_path+'new_column_list_1.txt') as f:
            columns_list_df1 = f.readlines()

        for column_name in columns_list_df1:
            if int(column_name.split("-")[0]) == field_id:
                self.columns_to_read_for_field_id.append(column_name.strip())

        tempdf = pd.read_csv(static_resource_path+"ukb49570.csv", usecols=self.columns_to_read_for_field_id+['eid'])
        tempdf = tempdf.dropna(thresh=2)

        return tempdf['eid'].unique()

    def get_data_bulk(self, field_id=None, subject_id=None):
        """A helper function which lets user download bulk data related to
        a subject, invokes datalad under the hood.Download starts after
        user provides credentials in a new terminal shell.

        Args:
            field_id: A integer representing a field id.
            subject_id: A list of subject id's.

        Returns:
           A string representing the location on bridges2 where file was downloaded.

        """

        str_subject_id = str(subject_id)
        sting_for_datalad_command = ""
        for col in self.columns_to_read_for_field_id:
            modified_col = col.replace('-', '_').replace('.', '_')
            temp_str = str_subject_id+"/"+str_subject_id+"_"+modified_col+".zip"+" "
            sting_for_datalad_command += temp_str
        print(sting_for_datalad_command)

        return "/ocean/projects/asc170022p/tighu/ukb/inputs/"+str_subject_id

    def search_category_by_name(self, query=None):
        """A helper function which return closest matching UKB category based
        on query given by user, uses built-in function to get close match.

        Args:
            query: A string representing the query user wants to search for.


        Returns:
           A list of categories closely matching with the input query.

        """

        unique_category_file_object = open("all_unique_categories.txt", "r")
        all_categories_list = unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return get_close_matches(query, formatted_category_list, 5, 0.3)

    def fetch_bulk_data(self, subject_list=None, data_type="T1_Image"):
        """A helper function which returns file paths to imaging and freesurfer
        data for provided subjects based on type string provided.By default,
        returns file paths for T1 image.

        Args:
            subject_list: A list of subjects of interest.
            data_type: A string representing the type of file to be
                fetched. Examples include T1_image,FS_brain,FS_wm.

        Returns:
           A bulk data dictionary which has key as subject_ids and values as
           list of file paths along with a list of subjects currently not
           available.

        Example:
            api_object.fetch_bulk_data(subject_list=subject_list, data_type_string="T1_Image")


        """

        if subject_list is None:
            raise Exception

        if data_type == "T1_Image":
            subjects_available = os.listdir(T1_directory)
            bulk_data_dict = {}
            subjects_not_available = []

            for subject in subject_list:

                if subject in subjects_available:
                    for data_version in ["20252_2_0", "20252_3_0"]:
                        check_path = T1_directory+subject+"/"+data_version+"/T1/T1.nii.gz"
                        if os.path.exists(check_path):
                            bulk_data_dict[subject] = bulk_data_dict.get(subject, [])+[check_path]

                else:

                    subjects_not_available.append(subject)

            return bulk_data_dict, subjects_not_available

        elif data_type == "FS_brain":

            subjects_available = os.listdir(Freesurfer_directory)
            bulk_data_dict = {}
            subjects_not_available = []

            for subject in subject_list:

                if subject in subjects_available:
                    for data_version in ["20263_2_0", "20263_3_0"]:
                        check_path = Freesurfer_directory+subject+"/"+subject+"_" +\
                                     data_version+"/FreeSurfer/mri/brain.mgz"
                        if os.path.exists(check_path):
                            bulk_data_dict[subject] = bulk_data_dict.get(subject, []) + [check_path]

                else:
                    subjects_not_available.append(subject)

            return bulk_data_dict, subjects_not_available

        elif data_type == "FS_wm":

            subjects_available = os.listdir(Freesurfer_directory)
            bulk_data_dict = {}
            subjects_not_available = []

            for subject in subject_list:

                if subject in subjects_available:
                    for data_version in ["20263_2_0", "20263_3_0"]:
                        check_path = Freesurfer_directory + subject + "/" + subject + "_" + \
                                     data_version + "/FreeSurfer/mri/wm.mgz"
                        if os.path.exists(check_path):
                            bulk_data_dict[subject] = bulk_data_dict.get(subject, []) + [check_path]

                else:
                    subjects_not_available.append(subject)

            return bulk_data_dict, subjects_not_available
