import pandas as pd

meta_data_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
#local_static_path = "/media/tighu/extended_storage/local_static_files_ukb/"

encoding_dict = {"ethnicity": {"-3.0": "Prefer not to answer", "-1.0": "Do not know", "1.0": "White", "2.0": "Mixed",
                               "3.0": "Asian or Asian British", "4.0": "Black or Black British", "5.0": "Chinese",
                               "6.0": "Other ethnic group", "1001.0": "British", "1002.0": "Irish",
                               "1003.0": "Any other white background", "2001.0": "White and Black Caribbean",
                               "2002.0": "White and Black African", "2003.0": "White and Asian",
                               "2004.0": "Any other mixed background", "3001.0": "Indian", "3002.0": "Pakistani",
                               "3003.0": "Bangladeshi", "3004.0": "Any other Asian background", "4001.0": "Caribbean",
                               "4002.0": "African", "4003.0": "Any other Black background"},
                 "nationality_encoding_dict": {},
                 "imaging_data_dictionary": {}, }


class scalar_data_handler:

    """

    A class to represent family of methods for handling and fetching scalar data.

    """

    def __init__(self):
        self.columns_to_read_for_field_id = []
        return

    def display_all_categories(self):
        """The first prominent function which lets user see all the major
        categories present in the UKB dataset. Reads categories from a
        static resource file inside package.


        Args:
            None: Needs no parameters to operate.

        Returns:
            A list having all the unique categories of UKB.

        Example:
            api_object.display_all_categories()

        """

        unique_category_file_object = open(meta_data_path+"all_unique_categories.txt", "r")
        all_categories_list = unique_category_file_object.readlines()
        formatted_category_list = [a.rstrip() for a in all_categories_list]
        return formatted_category_list

    def get_field_ids_for_category(self, category_name=None):
        """A utility function which lets user see the associated field ids for
        each category, reads from a static file containing all the  category
        names and field ids.


        Args:
            category_name: a string representing a category name.

        Returns:
            A pandas object having related field ids of the category provided
            as input.

        Example:
            api_object.get_field_ids_for_category(category_name="Freesurfer Segmentation")

        """
        temp_field_ids_df = pd.read_csv(meta_data_path+"ukb_field_ids.csv")
        return temp_field_ids_df[temp_field_ids_df['Category'] == category_name]

    def get_subject_list_field_ids(self, field_id=None):
        """A helper function which lets user see subjects having data related
        to a field_id. Reads a metadata file into a pandas object, only
        reading relevant columns because of size of the csv file.


        Args:
            field_id: A integer representing a field id.

        Returns:
            A list of subject ids relevant to the input field_id.

        Example:
            api_object.get_subject_list_field_ids(field_id= 20263)

        """

        with open(meta_data_path+'new_column_list_1.txt') as f:
            columns_list_df1 = f.readlines()
        columns_to_read_for_field_id = []
        for column_name in columns_list_df1:
            if int(column_name.split("-")[0]) == field_id:
                columns_to_read_for_field_id.append(column_name.strip())

        tempdf = pd.read_csv(meta_data_path+"ukb49570.csv", usecols=columns_to_read_for_field_id+['eid'])

        return tempdf['eid'].unique()

    def get_data_scalar(self, field_id_list=None, subject_list=None):
        """A helper function which lets user fetch scalar data associated with
        a field id and subject list.The fields in UKB dataset have been
        encoded in the following way --> field_id-instance_number-array_index.

        field_id: Numerical Number representing a particular feature of UKB
            dataset. For example 20252 represents T1 NIFTI files.

        instance_number: Currently 4 instances are present in the UKB dataset
            represents in which years of study wasdata collected or recorded.

            - Instance 0--> 2006-2010.
            - Instance 1--> 2012-2013.
            - Instance 2--> (2014+).
            - Instance 3--> (2019+).
        array_index: It is the identifier present in cases where a single field
            id can have multiple values. An example could be multiple readings
            of blood-pressure taken after fixed intervals.

        Args:
            field_id_list: list of field id
            subject_list: list of subject ids of interest
        Returns:
            A pandas object containing the scalar data.

        Example:
            api_object.get_data_scalar(field_id_list= 20263)

        """

        if field_id_list is None or subject_list is None:
            raise Exception

        with open(meta_data_path+'new_column_list_1.txt') as f:
            columns_list_df1 = f.readlines()
        columns_to_read = []

        for column_name in columns_list_df1:
            if int(column_name.split("-")[0]) in field_id_list:
                columns_to_read.append(column_name.strip())

        tempdf = pd.read_csv(meta_data_path+"ukb49570.csv", usecols=columns_to_read+['eid'])
        tempdf = tempdf.set_index('eid')

        return tempdf[tempdf.index.isin(subject_list)]
