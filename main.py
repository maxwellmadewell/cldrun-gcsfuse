import pandas as pd

# from settings import ArgParser
from cloudapi import list_blobs, download_blob, upload_blob
# from readConfig import metadata_creator

# from google.cloud import storage
# import pandas as pd
from datetime import datetime as dt
import base64
import os

from flask import Flask, request

app = Flask(__name__)

# Input = ArgParser()
# # Config_Address="config/params.conf"
# InputFolder_Address = Input.parse_args().input_folder
# Config_Address = Input.parse_args().config
# OutputFolder_Address = Input.parse_args().output_folder
# rewirte_Tag = Input.parse_args().write
# if rewirte_Tag == 'False' or rewirte_Tag == 'false' or rewirte_Tag == False:
#     rewirte_Tag = False
# elif rewirte_Tag == 'True' or rewirte_Tag == 'true' or rewirte_Tag == True:
#     rewirte_Tag = True
# else:
#     raise ValueError("-w is not a correct. Please user either True or False.")


@app.route("/", methods=["POST"])
def index():
    print("starting index-------------")
    BUCKET_IN = "erm-predict-input"
    BUCKET_OUT = "erm-predict-output"
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    name = "pub message had no data value"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"Running engine {name}...")

    gs_df = pd.read_csv("gs://erm-predict-input/input/raw/simple.csv")
    download_blob(BUCKET_IN, "input/raw/simple.csv", "/app/output/raw.csv")
    filename = dt.now().strftime("%Y%m%d-%H%M%S")
    upload_blob(BUCKET_OUT, "/app/output/raw.csv", filename)
    city = ["nashville", "atlanta", "bangalore", "london", "seoul"]
    gs_df["newcity"] =city
    gs_df.to_csv("gs://erm-predict-input/output/_latest.csv")
    print(f"Completed engine {name}.")

    return ("", 204)


if __name__ == "__main__":
    print("starting main#######################")
    os.system('gcsfuse erm-predict-input /app')
    filelist = os.system('ls $pwd/input/')
    print(filelist)
    BUCKET_IN = "erm-predict-input"
    BUCKET_OUT = "erm-predict-output"
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # app.run for local hosting
    # Gunicorn entrypoint will be set in dockerfile
    print("about to run app")
    app.run(host="127.0.0.1", port=PORT, debug=True)
