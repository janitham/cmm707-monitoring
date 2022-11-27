import subprocess
import time

def executeCommand(command, directory):
    return  subprocess.check_output(command, shell=True, cwd=directory)
    
def buildDockerImage():
    print("Building Docker Image....")
    
def updatingGitOpsRepo():
    print("Updating the GitOPs repository....")
    
def waitUntilSync():
    print("Waiting until the version is synced")
    
def runIntegrationTests():
    print("Executing Integration Tests....")
    
def job():
    result = executeCommand("git pull", r"C:\workspace\CMM707\sync-repos\registration-service")
    
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