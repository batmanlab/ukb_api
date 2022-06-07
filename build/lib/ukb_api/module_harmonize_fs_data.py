import pandas as pd
meta_data_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"
fs_combat_cols = ['eid', '53-2.0', '34-0.0', '31-0.0', '54-2.0']


class harmonize_fs_data:
    def __init__(self):
        return

    @staticmethod
    def get_subject_ids():
        """A utility function which lets user fetch a list of subject ids whose
        free-surfer data is available on PSC.


        Args:
            None: Needs no parameters to operate.

        Returns:
            A list object containing the subject ids.

        """

        with open(meta_data_path+'UKB_fs_folder_paths_march_2022.csv') as f:
            folder_paths = f.read().splitlines()

        fs_subject_list = []
        for path in folder_paths:
            fs_subject_list.append(path.split("/")[-3])

        return list(set(fs_subject_list))

    @staticmethod
    def ukb_subject_sex(sex):
        if sex == 0.0:
            return "F"
        else:
            return "M"

    @staticmethod
    def ukb_subject_age(year):
        return int(2022 - year)

    @staticmethod
    def ukb_subject_age_at_scan(row):
        return int(row['Date_of_Brain_Scan'].year - row['Year_of_Birth'])

    @staticmethod
    def parse_subject_id_from_path(path):
        return path.split("/")[-3]

    @staticmethod
    def get_center(center):
        if center == 11025.0:
            return "Cheadle"

        elif center == 11026.0:
            return "Reading"

        elif center == 11027.0:
            return "Newcastle"

    def get_demographics_data(self, subject_list=None):
        """The primary function of this module which lets user provide a
        subject list. Returned is a pandas dataframe which has metadata
        and freesurfer features. If no subject list is provided all
        subjects are considered.


        Args:
            subject_list: A python list of subjects whose freesurfer and
                metadata features is required.

        Returns:
            A pandas dataframe which has all the features from freesurfer
            like cortical measurements and subcortical volume numbers.

        """

        if subject_list is None:
            fs_subject_list = harmonize_fs_data.get_subject_ids()
        else:
            fs_subject_list = subject_list

        long_combat_df = pd.read_csv(meta_data_path + "ukb_brain_imaging_metadata.csv")
        long_combat_df = long_combat_df[long_combat_df['eid'].isin(fs_subject_list)]
        long_combat_df = long_combat_df.rename(
            columns={"eid": "Subject_ID", "31-0.0": "Sex", "34-0.0": "Year_of_Birth", "53-2.0": "Date_of_Brain_Scan",
                     "54-2.0": "Assesment_Centre"})
        long_combat_df['Assesment_Centre'] = long_combat_df['Assesment_Centre'].apply(lambda x:
                                                                                      harmonize_fs_data.get_center(x))
        long_combat_df = long_combat_df.reset_index(drop=True)
        long_combat_df['Date_of_Brain_Scan'] = pd.to_datetime(long_combat_df['Date_of_Brain_Scan'])
        long_combat_df['Sex'] = long_combat_df['Sex'].apply(lambda x: harmonize_fs_data.ukb_subject_sex(x))
        long_combat_df['Age'] = long_combat_df['Year_of_Birth'].apply(lambda x: harmonize_fs_data.ukb_subject_age(x))
        long_combat_df['Age_at_Scan'] = long_combat_df.apply(lambda x: harmonize_fs_data.ukb_subject_age_at_scan(x),
                                                             axis=1)

        fs_features_df = pd.read_csv(meta_data_path + "ukb_fs_features.csv")
        fs_features_df = fs_features_df[fs_features_df['Subject_ID'].isin(fs_subject_list)]

        long_combat_df['Subject_ID'] = long_combat_df['Subject_ID'].astype(str)
        fs_features_df['Subject_ID'] = fs_features_df['Subject_ID'].astype(str)

        final_df = pd.merge(long_combat_df, fs_features_df, on='Subject_ID', how='outer')

        return final_df
