#!/usr/bin/env python3
import sys
import os
import glob
import datalad.api

# read the list of required ds as a refrence
with open("/ocean/projects/asc170022p/shared/Data/ukBiobank/datalad_dataset/code/brain_imaging_subjects.txt", "r") as fp:
    lines = fp.readlines()
    ds_list = [ds.split("\n")[0] for ds in lines]

st = int(sys.argv[1])
n = 500
if st + n > len(ds_list):
    ed = len(ds_list)
else:
    ed = st + n

chunk_toget = ds_list[st:ed]

# path to folder where all ds are going to be cloned
superds_path = "/ocean/projects/asc170022p/shared/Data/ukBiobank/datalad_dataset"
root_path = os.path.join(superds_path, "inputs/subjects")

for ds in chunk_toget:
    source = "tighu@openmind7.mit.edu:" + "/om4/project/biobank/ukb/inputs/subjects/" + ds
    path = os.path.join(root_path, ds)
    # clone the dataset if it is not already cloned
    try:
        if not os.path.exists(path):
            datalad.api.clone(source, path)
    except Exception as e:
        with open("/ocean/projects/asc170022p/tighu/error_files_ukb_fs_jobs/FSexception-{}.txt".format(st), "at") as fp:
            fp.writelines(ds+str(e))


    # find fields to get in dataset
    fields_toget = glob.glob(path + "/" + "20263_[0-9]*_[0-9]")

    # get freesurfer data if it is downloaded by source
    if fields_toget:
        for field in fields_toget:
            data_path = os.path.join(path, field)
            # get the data
            try:
                datalad.api.get(path=data_path, dataset=path)
            except Exception as e:
                with open("/ocean/projects/asc170022p/tighu/error_files_ukb_fs_jobs/FSexception-{}.txt".format(st), "at") as fp:
                    fp.writelines(ds+str(e))
    else:
        with open("/ocean/projects/asc170022p/tighu/error_files_ukb_fs_jobs/FSdata_missing-{}.txt".format(st), "at") as fp:
            fp.writelines(f"{ds}\n")
