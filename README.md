# UKB_Wrapper_Repo

This library has been designed to provide convenient access to UKB dataset to users of PSC and Openmind7 clusters by leveraging Datalad package. Datalad allows its users to store large datasets in a distributed manner and faciliate easier collaboration. Currently the repo has modules dedicated to three types of data stored within the UKB dataset namely Scalar, Genetic and Bulk data types. The library also serves as a directory for all the unique categories and field ids which are part of UKB dataset. 

Datalad is designed as a tool to version control large datasets in a manner quite similar to Git but limited to either a single network, HPC cluster. This library has been designed to help the end user make use the principles of datalad to access data stored on a different cluster and even with limited knowledge of how datalad works.

Additionally this repository also houses the notebook files related to this project showcasing exploratory data analysis done on multiple categories.The modules are currently designed to give access to the necessary data through the use of maximum of three-four lines of code.

1. Import relevant modules and initilize objects
```
from UKBRepo.UKBRepo import module_scalar_data_handler as scalar_module

scalar_handler_object=scalar_module.scalar_data_handler()
```
2. Pick the main category to which your datatype belongs (T1_Images/Freesurfer/Diet/Smoking)
```
scalar_handler_object.display_all_ukb_categories()
```
3. Fetch relevant field for that Category
```
bulk_handler_object.get_field_ids_for_category(Category_Name)
```
4. Retrive the list of subjects who have those particular field ids
```
bulk_handler_object.get_subject_list_field_ids(Field_Id_List)
```
5. Retrive relevant data for the subjects
```
bulk_handler_object.get_data_bulk(Field_Id,subject_id)
```

After executing the funtion of data retrival,the output user receives depends upon the type of data bieng requested. In case of scalar data the user will recive the actual data in the output whereas in case of bulk data it will be the path where the fetched bulk data files have been stored. 

# Requirements

1. Datalad
2. Git-annex
3. Pandas
4. Numpy

# Refrences

http://handbook.datalad.org/en/latest/
