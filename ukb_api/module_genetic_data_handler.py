import numpy as np
import random
from pandas_plink import read_plink1_bin
import pickle
import xarray
genetic_data_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/UKB_Genetic_Data/"
meta_dath_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/meta_data_files/"


class genetic_data_handler:
    """

    A class to represent family of methods that can fetch list of xarray objects based on combination of list of
    subjects and variants provided.

    """

    def __init__(self):

        genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + "1" + "_b0_v2.bed",
                                     genetic_data_path + "bim_files/" + "ukb_snp_chr" + "1" + "_v2.bim",
                                     genetic_data_path + "fam_files/" + "ukb22418_c" + "1" + "_b0_v2_s488176.fam",
                                     verbose=True)
        genetic_df = genetic_df.set_index({"variant": "snp"})
        self.all_ukb_subjects = genetic_df.sample.values

    def get_subject_ids(self):
        """A utility function which lets user fetch numpy array
        containing the list of all subject ids.


        Args:
            None: No parameter required for this function.


        Returns:
            A list containing the subject IDs.

        """

        if self.all_ukb_subjects is None:
            print("Please initialize Module")
            return None

        else:
            return self.all_ukb_subjects

    @staticmethod
    def get_path_genetic_files():
        """A static function which lets user see all the
        genetic data locations.


        Args:
            None: No parameter required for this function.


        Returns:
            A string representing the path where Genetic
            Data is stored on Bridges2.

        """

        return genetic_data_path

    def get_genetic_data(self, subject_list=None, variant_dict=None):
        """The Primary function of the module which allows user to provide a
        subject list and dictionary which has keys as chromosome numbers and
        values as a list of variants of interest. If no subjects list is
        provided 100 random subjects are considered.If no dictionary is
        provided as input, an exception is raised.


        Args:
            subject_list: List of subjects which are of interest.
            variant_dict: A python dictionary having keys as relevant
                chromosome number and values as list of variants that are
                of interest to us.



        Returns:
            A single concatenated XArrayDataset.

        Example:
            api_object.get_genetic_data(subject_list=subject_list, variant_dict={chr1: [snp0001]})

        """

        if subject_list is None:

            subject_list = random.sample(self.all_ukb_subjects, 100)

        elif variant_dict is None:
            raise Exception

        genetic_data_array = []
        for chr_num in variant_dict.keys():

            genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + chr_num + "_b0_v2.bed",
                                         genetic_data_path + "bim_files/" + "ukb_snp_chr" + chr_num + "_v2.bim",
                                         genetic_data_path + "fam_files/" + "ukb22418_c" + chr_num +
                                         "_b0_v2_s488176.fam", verbose=True)

            genetic_df = genetic_df.set_index({"variant": "snp"})
            genetic_df = genetic_df.where(genetic_df['sample'].isin(subject_list) & genetic_df['variant'].isin(
                variant_dict[chr_num]), drop=True)

            genetic_data_array.append(genetic_df)
        res = xarray.concat(genetic_data_array, dim="variant")
        return res

    def get_genetic_data_from_snps(self, subject_list=None, snp_list=None):
        """The Primary function of the module which allows user to provide a
         subject list and list of snps to retrieve genetic data in form of
         XArray Datasets.


        Args:
            subject_list: List of subjects which are of interest.
            snp_list: A python list containing SNPs of interest.

        Returns:
            A single concatenated XArrayDataset.

        Example:
            api_object.get_genetic_data_from_snps(subject_list=subject_list, snp_list=[snp0001,snp0002,snp0003])

        """

        if subject_list is None:

            subject_list = random.sample(self.all_ukb_subjects, 100)

        elif snp_list is None:
            raise Exception

        with open(meta_dath_path+'ukb_chr_variant_mapping.pkl', 'rb') as f:
            mapping_dict = pickle.load(f)

        variant_dict = {}
        genetic_data_array = []
        for key in mapping_dict.keys():
            res = mapping_dict[key].intersection(set(snp_list))

            if len(res) != 0:
                variant_dict[key] = list(res)

        for chr_num in variant_dict.keys():

            genetic_df = read_plink1_bin(genetic_data_path + "bed_files/" + "ukb22418_c" + chr_num + "_b0_v2.bed",
                                         genetic_data_path + "bim_files/" + "ukb_snp_chr" + chr_num + "_v2.bim",
                                         genetic_data_path + "fam_files/" + "ukb22418_c" + chr_num +
                                         "_b0_v2_s488176.fam", verbose=True)

            genetic_df = genetic_df.set_index({"variant": "snp"})
            genetic_df = genetic_df.where(genetic_df['sample'].isin(subject_list) & genetic_df['variant'].isin(
                variant_dict[chr_num]), drop=True)

            genetic_data_array.append(genetic_df)
        res = xarray.concat(genetic_data_array, dim="variant")
        return res

