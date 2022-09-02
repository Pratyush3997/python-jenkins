import re
import jenkins
import sys
import getopt
from datetime import datetime

class DurationMetrics:
    username = ''
    password = ''
    previousvalue = ''
    updatedvalue = ''
    input = ''
    totalBuildDuration = 0.0
    numberOfBuilds = 0.0
    buildDurations = []
    buildTimestamps = []
    server = None

    # defining variables
    def __init__(self, username, password,previousvalue,updatedvalue,input):
        self.username = username
        self.password = password
        self.previousvalue = previousvalue
        self.updatedvalue = updatedvalue
        self.input = input

    def getJobDuration(self):
        # get job duration
        jenkinsJobs = self.server.get_all_jobs()
        #print(jenkinsJobs)
        myJob = self.server.get_job_info('sample-job', 0, True)
        print(myJob)
        myJobBuilds = myJob.get('builds')
        for build in myJobBuilds:
            buildNumber = build.get('number')
            buildInfo = self.server.get_build_info('sample-job', buildNumber)
            buildDuration = buildInfo.get('duration')
            self.buildDurations.append((buildDuration / 1000))
            self.totalBuildDuration += buildDuration
            self.numberOfBuilds += 1.0
            buildTimestamp = buildInfo.get('timestamp')
            self.buildTimestamps.append(buildTimestamp)

    def getJobConfig(self):
        #get the job configuration
        jobs = self.server.get_all_jobs(folder_depth=None)
        regex = self.input
        print(regex)
        for job in jobs:
            job = job['name']
            #print(job)
            if re.search(regex, job):
                print("Matched Job :"+job)
                myJob = self.server.get_job_config(job)
                print(self.input)
                print(self.previousvalue)
                print(self.updatedvalue)
                new = myJob.replace(self.previousvalue, self.updatedvalue)
                #print(new)
                myJob = self.server.reconfig_job(job, new)
                #print(myJob)
            else:
                print("Out of scope jobs:"+job)

    def connectToJenkins(self):

        # connect to Jenkins server
        self.server = jenkins.Jenkins('http://54.202.6.181:8080/', username=self.username, password=self.password)
        user = self.server.get_whoami()
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))
        
def main(argv):
    # passing id, pass to login into jenkins and previousvalue, updatedvalue as arguments to set required job schedule
    username = ''
    password = ''
    previousvalue = sys.argv[5]
    updatedvalue = sys.argv[6]
    input = sys.argv[7]
    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["username=", "password="])
    except getopt.GetoptError:
        print
        'python Job-Duration-Metrics.py -u <username> -p <password>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'python Job-Duration-Metrics.py -u <username> -p <password>'
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    durationMetrics = DurationMetrics(username, password,previousvalue,updatedvalue, input)
    durationMetrics.connectToJenkins()
    durationMetrics.getJobConfig()

if __name__ == "__main__":
    #sys args helps passing argumentsas parameter
    main(sys.argv[1:])
