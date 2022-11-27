import subprocess
import time

def executeCommand(command, directory):
    return  subprocess.check_output(command, shell=True, cwd=directory)
    
def job():
    result = executeCommand("git pull", r"C:\workspace\CMM707\sync-repos\registration-service")
    
    if 'Already up to date' in result.decode("utf-8") :
        print("Do not trigger the pipeline")    
    else:
        print("Triggering the pipeline")
    

if __name__ == "__main__":
    while True:
        job()
        time.sleep(10)