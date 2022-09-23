# Description
  This is a Python script for changing Jenkins job schedule. 
  After connecting to Jenkins it will fetch all the jobs and using regex filter the required one.
  Using Jenkins-Python API functions it will replace existing values with updated values.

# Modules Used
  #### jenkins - For using Python-Jenkins API functions it is required to import "jenkins".
  #### sys,getopt - These Modules will help in the authentication of the jenkins server using parameters(UserID & Password) that will be provided.
  #### re - For using regex functions "re" module is necessary.

## Connection with Jenkins
  For making a connection with jenkins, jenkins IP, Userid and password/token is passed in this fuction.
  "get_whoami()" will give jenkins admin name & "get_version()" will give version of jenkins.

## Functionality
  when program is called the main function will get invoked and its gonna pass the arguments with help of "sys.argv".
  #### getJobConfig fucntion :
  "get_all_jobs" will get all the jobs from jenkins. 
  Using "regex" it will filter and the get required jobs, once required job is there using "get_job_config" we'll get config of the job 
  and using replace function existing value will be replaced with updated value
  "reconfig_job" will again reconfigure the changes that were made



  
