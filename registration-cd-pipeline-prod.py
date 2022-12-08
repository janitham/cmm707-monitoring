import subprocess
import time
import fileinput
import re
import requests
import json

GITOPS_SYNC_REPO = "C:/workspace/CMM707/sync-repos/registration-service"
GITOPS_REPOSITORY = "C:/workspace/CMM707/implementation/argocd-gitops"
GITOPS_BRANCH = "prod"

SERVICE_NAME = "registration"
BUILD_VERSION = ""

DEPLOYMENT_PORT = "8080"
headers = {
    'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ=',
    'Content-Type': 'application/json'
}

def executeCommand(command, directory):
    return  subprocess.check_output(command, shell=True, cwd=directory)
    
def replaceFileLine(file, startswith, repl_str):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for l in lines:
            f.write(repl_str if l.startswith(startswith) else l)            
    
def updatingGitOpsRepo():
    print("Updating the GitOPs repository....")
    executeCommand("git checkout " + GITOPS_BRANCH, GITOPS_REPOSITORY)
    values_path = GITOPS_REPOSITORY + "/charts/" + SERVICE_NAME + "/values.yaml"
    BUILD_VERSION = executeCommand("kubectl get deploy registration -n test -o jsonpath='{.metadata.labels.version}'", GITOPS_SYNC_REPO).decode("utf-8").replace("'", "")
    print(BUILD_VERSION)
    replaceFileLine(values_path, "  tag:", "  tag: "+BUILD_VERSION)
    print("Updated version in the git ops")
    executeCommand("git add  charts/*", GITOPS_REPOSITORY)
    executeCommand("git commit -m \"Updated Version to "+BUILD_VERSION+"\"", GITOPS_REPOSITORY)
    executeCommand("git push", GITOPS_REPOSITORY)
    
    
def waitUntilSync():
    print("Waiting until the version is synced")
    BUILD_VERSION = executeCommand("kubectl get deploy registration -n test -o jsonpath='{.metadata.labels.version}'", GITOPS_SYNC_REPO).decode("utf-8").replace("'", "").strip()
    url = "http://localhost:"+DEPLOYMENT_PORT+"/actuator/info"
    while True:
        try:
            response = requests.request("GET", url, headers=headers, data={})
            versionDeployed = str(json.loads(response.text)['build']['version']).replace("+", "_").strip()
            if BUILD_VERSION == versionDeployed:
                print("Deployment sucessful")
                break
            time.sleep(10)
        except:
            print("Inturrpution notified")
    
    
def runIntegrationTests():
    print("Executing Integration Tests....")
    print(executeCommand("python.exe registration-test-suite.py", ".").decode("utf-8").strip())
    
def job():
    result = executeCommand("git pull", GITOPS_SYNC_REPO)
    
    print("Triggering CD pipeline...")
    updatingGitOpsRepo()
    waitUntilSync()
    runIntegrationTests()
    

if __name__ == "__main__":
    job()