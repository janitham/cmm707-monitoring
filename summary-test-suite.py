import requests
import json

SERVICE_NAME = "summary"
BUILD_VERSION = ""
DEPLOYMENT_PORT = "8081"
HOST="localhost"

headers = {
  'Content-Type': 'application/json'
}

class Tester:
    outputJson = None

    def __init__(self):
       self.msg = "Default constructor"
       
    def createdSummary(self):
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/summary/created"
        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code != 200:
            raise "Error summary created"
        
    def updatedSummary(self) :
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/summary/updated"
        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code != 200:
            raise "Error summary updated"
        
    def deletedSummary(self):
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/summary/deleted"
        response = requests.request("GET", url, headers=headers, data={})
        if response.status_code != 200:
            raise "Error summary deleted"
        
if __name__ == "__main__":
    tester = Tester()
    tester.createdSummary()
    tester.updatedSummary()
    tester.deletedSummary()
    print("Successfully ran the tests....")