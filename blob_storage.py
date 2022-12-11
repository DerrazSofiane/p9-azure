from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")


class AzureBlobStorage:
    def __init__(self, conn_str:str):
        try:
            print("Trying to connect...")
            self.blob_service_client = BlobServiceClient.from_connection_string(
                conn_str
            )
            print("\nSuccessfully connected")
        except Exception as e:
            print("\nFailed to connect")
            print(e)
        
    def create_container(self, container_name:str):
        try:
            print("\nTrying to create container", container_name)
            self.container_client = self.blob_service_client.create_container(container_name)
            print("\nSuccessfully created the container\n")
        except Exception as e:
            print("\nFailed to create the container")
            print(e)        
    
    def upload_file_to_container(self, container_name:str, file_path:str):
        try:
            # Create a blob client using the local file name as the name for the blob
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_path)
            
            # Upload the created file
            print("\nUploading to Azure Storage as blob:\n\t" + file_path)
            dataframe = pd.read_csv(file_path)
            output = dataframe.to_csv(index=False, encoding="utf-8-sig")
            blob_client.upload_blob(output, overwrite=True)
            print("\nSuccessfuly uploaded file")
        except Exception as e:
            print("\nFailed to upload file")
            print(e)

        # List the blobs in the container
        print("\nListing blobs...")
        blob_client = self.blob_service_client.get_container_client(container_name)
        blob_list = blob_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
    
    def delete_file_from_container(self, container_name:str, file_name:str):
        todelete_blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=file_name)
        try:
            # Check if the blob exists
            if todelete_blob_client.exists():
                # Delete blob
                print("\nDeleting blob", file_name)
                todelete_blob_client.delete_blob()
                print("\nBlob deleted successfully!")
            else:
                print("\nBlob does not exist!\n")
        except Exception as e:
            print("\nFailed to delete blobstr")
            print(e)
    
    def delete_container(self, container_name):
        try:
            container_client = self.blob_service_client.get_container_client(
                container=container_name)
            print("\nDeleting blob container:\n\t" + container_name)
            container_client.delete_container()
            print("\nSuccessfuly deleted container")
        except Exception as e:
            print("\nFailed deleting container")
            print(e)
