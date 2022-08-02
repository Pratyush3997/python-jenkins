import re
import xml.etree.ElementTree as ET
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
            # print(buildInfo)
            buildDuration = buildInfo.get('duration')
            self.buildDurations.append((buildDuration / 1000))
            self.totalBuildDuration += buildDuration
            self.numberOfBuilds += 1.0
            buildTimestamp = buildInfo.get('timestamp')
            self.buildTimestamps.append(buildTimestamp)



    def getJobConfig(self):

        jobs = self.server.get_all_jobs(folder_depth=None)
        # build_info = self.server.build_job('sample-python-job-1')
        # # self.server.build_job('api-test', {'param1': 'QXMgr', 'param2': 'QXOne'})
        # # last_build_number = self.server.get_job_info('api-test')['lastCompletedBuild']['number']
        # # build_info = self.server.get_build_info('api-test', last_build_number)
        # print(build_info)
        #print(jobs)
        # regex_input = self.input
        # #regex_var = 'r"' + regex_input+'"'
        # regex_var = "r"+regex_input+'"'
        regex = self.input
        print(regex)
        for job in jobs:
            #assert re.match(regex, job), f'Failed on {job=} with {regex=}'
            #myJob = self.server.get_job_config(job['name'])
            #myJob = re.findall(r'(QXMGR)',myJob)
            job = job['name']
            #print(job)
            if re.search(regex, job):
                print("Matched Job :"+job)
                myJob = self.server.get_job_config(job)
                #myConfig = myJob.get_config()
                #print(myJob)
                print(self.input)
                print(self.previousvalue)
                print(self.updatedvalue)
                new = myJob.replace(self.previousvalue, self.updatedvalue)
                #myJob.update_config(new)
                #print(new)
                myJob = self.server.reconfig_job(job, new)
                #print(myJob)

            else:
                print("Out of scope jobs:"+job)

    # def getAllJobs(self):
    #     jobs = self.server.get_all_jobs(folder_depth=None)
    #     for job in jobs:
    #         print(job['name'])
    #         myJob = self.server.get_job_config(job['name'])
    #         print(myJob)
    #         new = myJob.replace('<spec>H 1 * * *</spec>', '<spec>H 3 * * *</spec>')
    #         myJob = self.server.reconfig_job(job['name'], new)
    #         print(myJob)
    # def build(self):
    #     #build_info = self.server.build_job('test-demo')
    #     jobs = self.server.get_jobs("API-TEST - test-demo")
    #     job = jobs.build_job(TEXT1="QXMgr", TEXT2="QXMgr")
    #     print(job)
    #     # self.server.build_job('api-test', {'param1': 'QXMgr', 'param2': 'QXMgr'})
    #     # last_build_number = self.server.get_job_info('api-test')['lastCompletedBuild']['number']
    #     # build_info = self.server.get_build_info('api-test', last_build_number)
    #     #print(build_info)


    def connectToJenkins(self):

        # connect to Jenkins server
        self.server = jenkins.Jenkins('http://35.164.255.6:8080/', username=self.username, password=self.password)
        user = self.server.get_whoami()
        version = self.server.get_version()

        print('Hello %s from Jenkins %s' % (user['fullName'], version))


    def convertTimestamps(self):
        dates = []
        for timestamp in self.buildTimestamps:
            dateTimeObj = datetime.fromtimestamp((timestamp / 1000))
            dates.append(dateTimeObj)
        return dates


def main(argv):
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
    #durationMetrics.getJobDuration()
    durationMetrics.getJobConfig()
    #durationMetrics.getAllJobs()
    #durationMetrics.get_value_from_string()
    #durationMetrics.newargs()
    #durationMetrics.build()



if __name__ == "__main__":
    main(sys.argv[1:])
