import requests
import json

SERVICE_NAME = "registration"
BUILD_VERSION = ""
DEPLOYMENT_PORT = "8080"
HOST="localhost"

defaultPayload = json.dumps({
      "name": "charurika",
      "description": "Indian"
})
    
headers = {
    'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ=',
    'Content-Type': 'application/json'
}

class Tester:
    outputJson = None

    def __init__(self):
       self.msg = "Default constructor"
       
    def createVoter(self):
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/voters"
        response = requests.request("POST", url, headers=headers, data=defaultPayload)
        if response.status_code != 201:
            raise "Error creating voter"
        self.response = response.text
        
    def updateUser(self) :
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/voters"
        response = requests.request("PUT", url, headers=headers, data=self.response)
        if response.status_code != 200:
            raise "Error updating voter"
        
    def deleteUser(self):
        user = json.loads(self.response)['id']
        url = "http://"+HOST+":"+DEPLOYMENT_PORT+"/voters/" + user
        response = requests.request("DELETE", url, headers=headers, data={})
        if response.status_code != 200:
            raise "Error deleting voter"
        
if __name__ == "__main__":
    tester = Tester()
    tester.createVoter()
    tester.updateUser()
    tester.deleteUser()
    print("Successfully ran the tests....")