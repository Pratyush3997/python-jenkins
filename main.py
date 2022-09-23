# importing necessary modules
import re
import jenkins
import sys
import getopt

# this function has variables that will be used in the script
class DurationMetrics:
    username = ''
    password = ''
    existingvalue = ''
    updatedvalue = ''
    input = ''

    # variables will be passed using this constructor
    def __init__(self, username, password, existingvalue, updatedvalue, input):
        self.username = username
        self.password = password
        self.existingvalue = existingvalue
        self.updatedvalue = updatedvalue
        self.input = input

    # member function
    def getJobConfig(self):
        # get the job configuration
        jobs = self.server.get_all_jobs(folder_depth=None)
        # regex will filter required job
        regex = self.input
        print(regex)
        for job in jobs:
            job = job['name']
            # print(job)
            # searching the required job
            if re.search(regex, job, re.IGNORECASE):
                print("Matched Job :" + job)
                # get_job_config will get configuration of jobs
                myJob = self.server.get_job_config(job)
                print(self.input)
                print(self.existingvalue)
                print(self.updatedvalue)
                # replace will replace existing value of schedule with new one
                new = myJob.replace(self.existingvalue, self.updatedvalue)
                # print(new)
                # reconfig_job will reconfigure the changes
                myJob = self.server.reconfig_job(job, new)
                # print(myJob)
            else:
                print("Out of scope jobs:" + job)

    def connectToJenkins(self):
        # connect to Jenkins server
        self.server = jenkins.Jenkins('http://54.202.6.181:8080/', username=self.username, password=self.password)
        # will return the current user
        user = self.server.get_whoami()
        # will return the version of jenkins
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))

def main(argv):
    # in the main fuction passing, id, password to login into jenkins and existingvalue, updatedvalue as arguments to set required job schedule
    username = ''
    password = ''
    existingvalue = sys.argv[5]
    updatedvalue = sys.argv[6]
    input = sys.argv[7]
    try:
        # getopt package processes the arguments
        # opts help is used here to provide option to enter userID & password that will be entered by the user
        opts, args = getopt.getopt(argv, "hu:p:", ["username=", "password="])
    except getopt.GetoptError:
        print
        'python Job-Duration-Metrics.py -u <username> -p <password>'
        sys.exit(2)
    for opt, arg in opts:
        # h option will print out the usage
        if opt == '-h':
            print
            'python Job-Duration-Metrics.py -u <username> -p <password>'
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
    #calling functions
    durationMetrics = DurationMetrics(username, password, existingvalue, updatedvalue, input)
    durationMetrics.connectToJenkins()
    durationMetrics.getJobConfig()

    # calling main functions
if __name__ == "__main__":
    # sys args helps passing arguments as parameter
    main(sys.argv[1:])
