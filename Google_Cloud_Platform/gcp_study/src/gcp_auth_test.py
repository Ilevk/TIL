import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/Users/kyle/Documents/Git/TIL/Google_Cloud_Platform/gcp_study/key/gcp-study-252307-c1ad485219e2.json"
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


    
if __name__ == "__main__":
    # execute only if run as a script
    implicit()
