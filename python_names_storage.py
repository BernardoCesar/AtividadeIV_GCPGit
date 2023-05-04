from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "andre-382123",
  "private_key_id": "2dde6e0551eec342477c50f08d3b4e00f2aceca1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+qKeU1FrinRqx\nD1oA9YY0zZSTVav2owkODMhj1OoCP1sElweCGILGlPz8tiYFmWDxioIMaCJa+ZHY\n3qhPebfPomkjO/Xoi8cceJNEKgLyGtCy8vlbsD5YkBOa1yl8DclTWtPXCToduLWh\nuvKVoeMgmKZDlujy8N4zxEKoqK8NzZchiKwYnkajb5nTomfpQBVSfnrLxLlWcMe0\nT2fz9O9NqKL35b8PNV8XxFEoBd0Q0tDJxo55BjqU7wygd0k8FCDbHoN4bo34ZGrv\n7YFYg/QGgOL2kDWwd7oJVyr+FXCgjz1KQXrgBmPdvlqV7STPYe0lRYcviMZdXVYg\neaWkiMujAgMBAAECggEABdwG+henYn8YAq5pU/CsI7mSog9INXNluG9SC6fEFYgN\nkYzz+odClrzMddC2XoYjQxY0yrS69NdDVxXLRFWo/Y81vhMPuVvWX6sgzVb+d7pA\n+XV+Gh1p1o/EcnpioSPkPJT8EZ9GSqYA6ZHasNLY/v2CA1aUkeyjnK04CTvs1Px8\nb8v/z7b1gSveBs9pxlABY3GeEsu7rAWjLMinvDrvrdDp1oSniW/BOKNInuJSE4Dh\nkk4hc1T3PSY+AtNHimfXS/tu5qEAxXv0U4QNFenNjw0lUVMWMBONs4ilrxZrwIcb\n/FQGGSGBW+I1tA+ZctlNUij9aWqliCmBKgMQTwqghQKBgQD7tdvPrnNcDBgjD4fE\nkJ5lJ/8EfxZ51GExcqejWk0ANJVKNHAHxkHkb3bV/zA/HLqwQ9M0zTJ+p5IiDxUk\nqiaUamTkcnIZFJ8GtOhXqasof9C346PQuZArUwlMT0IU5vEQE3lTKin7JSRGqNf6\noelh/PKn3Ahiy0oME+QeG2Z8LQKBgQDB6HH26scG7gkUo2rusc9Nu3TgNZWVORad\ntSv/WOehE9XYOetkvPyX0tW5awELaoeNDNTq2V/w+MIe6156zt12O0jGjMQ7iiWz\nbKbPx8vJuYsSPC+SYfCL4Dt4YG/SzX4DLiBNvYaiVF+eC54vU3crjBf5iFVt60Xf\n6s3LcNe5DwKBgA21JKhVtsCPhAz8vocM3SNjHzcueJnf3/8iYFC8DS9yraKh4mv5\n9wKqs00KHaWCOgR5XRomBpbxJzslmSArB/jTJnVuahpFjjd+SJzlh4WoGES7Z+Np\nB5nkZsA6HL4oqX4XoWbPCAQ+TJBwh3qFsMD+VnSfvfErYvfvaV/eXCFtAoGAeGOJ\nxiSTtxC4oJCpRlMtAvTcpot+OGx+RyIBlAKtpMs83IdxR1UyekyTFxCBUIYubHtI\nAhs9vs2jMDEvso2W394E3AjvmIu3xoMxuhUwyCijWIn3eynFgAKSybUOGFIu52iO\n89U0rro1t1k9N+LZPTc4d1uWtqz48AHHDYUc2i8CgYAdQF3+aVp4Cx/CuE6v0MQQ\n4kUBfwNyGe4fTdCybhsmdFDcun3f7Vx/AX9LWWGkMhZ0TF+Rqd2Ybx3vCqlvj6rL\nH2qkyitYQC+S9rsy+cMX9m+uKXFFXD7mlu+JSH/+AO7roQm00romioyZqwn13Rib\nfu8SGCJmSSlkJT/3KnWxCA==\n-----END PRIVATE KEY-----\n",
  "client_email": "be-142@andre-382123.iam.gserviceaccount.com",
  "client_id": "102920429431012575836",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/be-142%40andre-382123.iam.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atividadeiv') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex)
