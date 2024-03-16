#import uvicorn
import subprocess

if __name__ == "__main__":
    #uvicorn.run("app.main:app", host="localhost", port=8000, reload=True, workers=4)
    command = "gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --timeout 600 --reload"
    subprocess.run(command, shell=True)
