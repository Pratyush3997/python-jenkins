# python-jenkins

#prerequisite 
 Jenkins 

# modules required 
 jenkins, sys, getopt, re

# if 
 when program is called the main function will get invoked and its gonna pass the command line arguments with help of "sys.argv"

# main will take arguments as input, we will provide option for user to input userid and password

# connectToJenkins - 
 for making a connection with jenkins, jenkins IP, Userid and password/token is passed in this fuction
 get_whoami() will give jenkins admin name
 get_version() will give version of jenkins

# getJobConfig - 
 get_all_jobs will get all the jobs from jenkins.
 using regex we'll get required jobs
 once reuiqred job is there using get_job_config we'll get config of the job and using replace function existing value will be replaced with updated value
 reconfig_job will again reconfigure the changes that were made
