# (Under Testing as getting some errors using podman, docker not able to use~ Error: preparing container for attach: crun: open executable: Permission denied: OCI permission denied)
## Part of Task6
echo "Starting api server..."
cd $APP_HOME # Changing directory to app/ folder inside which all our source code is copied and has our logic files app.py, database folder, etc etc.
uvicorn app:app --host 0.0.0.0 --port 8900 --reload ## & uvicorn sampleService.main:app --host 0.0.0.0 --port 8901 --reload ## Note using only single & to join them or execute both commands
