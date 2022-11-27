import subprocess
import time
import fileinput
import re

GITOPS_SYNC_REPO = "C:/workspace/CMM707/sync-repos/registration-service"
GITOPS_REPOSITORY = "C:/workspace/CMM707/argocd-example-apps"
GITOPS_BRANCH = "master"

SERVICE_NAME = "registration"
BUILD_VERSION = ""

def executeCommand(command, directory):
    return  subprocess.check_output(command, shell=True, cwd=directory)
    
def replaceFileLine(file, startswith, repl_str):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for l in lines:
            f.write(repl_str if l.startswith(startswith) else l)    
        
def buildDockerImage():
    print("Building Docker Image....")
    executeCommand("gradle build -x test jibDockerBuild devVersion", GITOPS_SYNC_REPO)
    BUILD_VERSION = executeCommand("powershell.exe cat ./dVersion", GITOPS_SYNC_REPO).decode("utf-8")
    print("Docker image version is %s" % BUILD_VERSION)
    
def updatingGitOpsRepo():
    print("Updating the GitOPs repository....")
    executeCommand("git checkout " + GITOPS_BRANCH, GITOPS_REPOSITORY)
    values_path = GITOPS_REPOSITORY + "/charts/" + SERVICE_NAME + "/values.yaml"
    BUILD_VERSION = executeCommand("powershell.exe cat ./dVersion", GITOPS_SYNC_REPO).decode("utf-8")
    replaceFileLine(values_path, "  tag:", "  tag: "+BUILD_VERSION)
    print("Updated version in the git ops")
    executeCommand("git add  charts/*", GITOPS_REPOSITORY)
    executeCommand("git commit -m \"Updated Version\"", GITOPS_REPOSITORY)
    executeCommand("git push", GITOPS_REPOSITORY)
    
    
def waitUntilSync():
    print("Waiting until the version is synced")
    
def runIntegrationTests():
    print("Executing Integration Tests....")
    
def job():
    result = executeCommand("git pull", GITOPS_SYNC_REPO)
    
    if 'Already up to date' in result.decode("utf-8") :
        print("Do not trigger the pipeline")    
    else:
        print("Triggering the pipeline")
        buildDockerImage()
        updatingGitOpsRepo()
        waitUntilSync()
        runIntegrationTests()
    

if __name__ == "__main__":
    while True:
        job()
        time.sleep(10)