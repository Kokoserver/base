from uvicorn import run

from base.settings import DEBUG

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   run("base:app", reload=True, workers=4, debug=DEBUG)
