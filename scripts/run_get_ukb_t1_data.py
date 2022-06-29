import subprocess

slurm_command_template = "sbatch --export=idx=start_index -p RM-shared -N 1 --ntasks-per-node=1 -A asc170022p -t 48:00:00 /ocean/projects/asc170022p/tighu/get_ukb_t1_data.job"


#3june_1-21  --->500 subjects per job
#5 June 21-61 ---->400subjects per job start=10K
#11June 1-21 --->400 remaining subjects
#13June 1-101 --->50 subjects per job
#15 June 101-201-->50 subjects per job
#16June 201-301-->50 subjects per job
#17June 301-401-->50 subjects per job
#18June 401-501--> 50 subjects per job
#20June 501-601-->50 subejcts per job
#23June 601,701--->50 subjects per job
#26June 701, 780 --->50 subjects per job
start=0
subjects_per_job=50
for job_counter in range(701,780):
    new_start_idx= str(start + (job_counter-1)*subjects_per_job)
    slurm_command=slurm_command_template.replace("start_index",new_start_idx)
    subprocess.Popen(slurm_command.split(" "))
