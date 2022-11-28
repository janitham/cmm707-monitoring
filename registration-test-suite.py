import requests
import json

GITOPS_SYNC_REPO = "C:/workspace/CMM707/sync-repos/registration-service"
GITOPS_REPOSITORY = "C:/workspace/CMM707/argocd-example-apps"
GITOPS_BRANCH = "master"

SERVICE_NAME = "registration"
BUILD_VERSION = ""

DEPLOYMENT_PORT = "8080"

defaultPayload = json.dumps({
      "name": "charurika",
      "description": "Indian"
    })
    

headers = {
  'Content-Type': 'application/json'
}

class Tester:
    outputJson = None

    def __init__(self):
       self.msg = "Default constructor"
       
    def createVoter(self):
        url = "http://localhost:8080/voters"
        response = requests.request("POST", url, headers=headers, data=defaultPayload)
        if response.status_code != 201:
            raise "Error creating voter"
        self.response = response.text
        
    def updateUser(self) :
        url = "http://localhost:8080/voters"
        response = requests.request("PUT", url, headers=headers, data=self.response)
        if response.status_code != 200:
            raise "Error updating voter"
        
    def deleteUser(self):
        user = json.loads(self.response)['id']
        url = "http://localhost:8080/voters/" + user
        response = requests.request("DELETE", url, headers=headers, data={})
        if response.status_code != 200:
            raise "Error deleting voter"
        
if __name__ == "__main__":
    tester = Tester()
    tester.createVoter()
    tester.updateUser()
    tester.deleteUser()