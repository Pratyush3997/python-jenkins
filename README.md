# Introduction

## Modules Used
  Jenkins - 
  sys - 
  getopt - 
  re - 

## Functionality
  when program is called the main function will get invoked and its gonna pass the command line arguments with help of "sys.argv"
  get_all_jobs will get all the jobs from jenkins. 
  using regex we'll get required jobs once reuiqred job is there using get_job_config we'll get config of the job 
  and using replace function existing value will be replaced with updated value
  reconfig_job will again reconfigure the changes that were made


## Connection with Jenkins
  For making a connection with jenkins, jenkins IP, Userid and password/token is passed in this fuction.
  "get_whoami()" will give jenkins admin name "get_version()" will give version of jenkins.

  
