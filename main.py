import re
from xml.etree import ElementTree
import jenkins
import sys
import getopt
from datetime import datetime
import xml.etree.ElementTree as ET

# this function has variables that will be used in the script
class DurationMetrics:
    username = ''
    password = ''
    existingvalue = ''
    updatedvalue = ''
    input = ''
    mystr = ''

    # variables will be passed using this constructor
    def __init__(self, username, password, existingvalue, updatedvalue, input, mystr):
        self.username = username
        self.password = password
        self.existingvalue = existingvalue
        self.updatedvalue = updatedvalue
        self.input = input
        self.mystr = mystr

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
                tree = ET.fromstring(myJob)              
                print("Input : ", self.input)
                print("Existing Value : ", self.existingvalue)
                print("Updated Value : ", self.updatedvalue)

                # declaring array
                xml_values = []

                # condition for empty existing value
                if self.existingvalue == "None":
                    # iterating through config file for PipelineTriggersJobProperty
                    for node in tree.iter('org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty'):
                        # print('\n')
                        for elem in node.iter():
                            # storing build tags
                            buildTrigger = elem.tag
                            # print(type(var1), "var1")
                            # sorting build values in buildTrigger & storing in xml_values
                            xml_values.append(buildTrigger)
                    print(xml_values)
                  
                    # searching for spec in xml values
                    if "spec" in xml_values:
                        print("spec found")
                        self.existingvalue = "<spec/>"
                        # storing updated values
                        checked_updatedValue = "<spec>" + self.updatedvalue + "</spec>"
                        print(checked_updatedValue)
                        # replacing existing value with updated value
                        replace_value1 = myJob.replace(self.existingvalue, checked_updatedValue)
                        # reconfiguring the config file
                        myJob = self.server.reconfig_job(job, replace_value1)                      
                    # searching for triggers in xml values
                    elif "triggers" in xml_values:
                        print("Triggers found")
                        self.existingvalue = "<triggers/>"
                        # storing updated values
                        unChecked_updatedValue = "<triggers><hudson.triggers.TimerTrigger><spec>" + self.updatedvalue + "</spec></hudson.triggers.TimerTrigger></triggers> "
                        print(unChecked_updatedValue)
                        # replacing existing value with updated value
                        replace_value2 = myJob.replace(self.existingvalue, unChecked_updatedValue)
                        # reconfiguring the config file
                        myJob = self.server.reconfig_job(job, replace_value2)                            
                else:
                    # replace will replace previous value of schedule with new one
                    new = myJob.replace(self.existingvalue, self.updatedvalue)
                    # print(new)
                    # reconfig_job will reconfigure the changes
                    myJob = self.server.reconfig_job(job, new)
                    # print(myJob)
            else:
                print("Out of scope jobs:" + job)

    def connectToJenkins(self):
        # connect to Jenkins server
        self.server = jenkins.Jenkins('http://35.93.122.162:8080/', username=self.username, password=self.password)
        # will return the current user
        user = self.server.get_whoami()
        # will return the version of jenkins
        version = self.server.get_version()
        print('Hello %s from Jenkins %s' % (user['fullName'], version))

def main(argv, mystr=None):
    # in the main fuction passing, id, password to login into jenkins and existingvalue, updatedvalue as arguments to
    # set required job schedule
    username = ''
    password = ''
    existingvalue = sys.argv[5]
    print(existingvalue)
    updatedvalue = sys.argv[6]
    print(updatedvalue)
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
    # calling functions
    durationMetrics = DurationMetrics(username, password, existingvalue, updatedvalue, input, mystr)
    durationMetrics.connectToJenkins()
    durationMetrics.getJobConfig()
 
# calling main functions
if __name__ == "__main__":
    # sys args helps passing arguments as parameter
    main(sys.argv[1:])
