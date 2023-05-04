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
  "private_key_id": "e6d439e67a679e689b969ec1b83f6ce21600124d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDRK810n8vWA/KD\nci+CZEhras62l233jPMp7nF5CmEcsXySjO4gCTLmGEuqSP70+S9Y4g58lKY7xX45\n2IsGYOPwKCrEuntzptLODSQIS3UDp+fbzqgRic6lWGUK8Fu155kLjwy2W//dJjKs\nQ7QudayTrcRDT1jetD2BtAUchpJoIQsti9iijXgsEDl1pcJI3OK8T6Mm9MffiA0y\n7Qp9gCaU7irGGDXhLeRyvEhSCRyVXBAebgSDH8P0DJMb1LIReOjixRIGwYNxVMgc\nNw+ChElvCOZEDm+JQnlWv28jnnyXRKSuHzUedTp1qu4D3x8Xb2EkMTEuEe4aGXud\n93m6dFODAgMBAAECggEAY3nI5odeWcQbz+58cK7/j/JGJ6kBl8K1HAJ1faJ1h79S\n5qFWV+74AVyZk3zOn7NoFIXBbPcGzZNBUgJNL7XhgSOhH1kuf9RdGbg/JCC6oAf4\nqNzxqhGXMKRGvXqMqwhfDRO1cH51Qve5DprONHArKDpyBa7VLWibfbUe3y+Srij4\nHfoL6rBtftbHXbzPJ9w0Ugojn4ToiROIs5IaTg9dpP5efMoQ4xrW7wWEII6E6Wxt\nWBzYIlLv3hhhxKGIFhRj5fRHDgB7AKmOMvxobScj4h33ujI+0rXFstggkNK8CQfO\nZRjAggCkgDwEtGjHEl8Tk45KXDEjp7CAtGNQdJhL8QKBgQD5e0JQgIu/VNuYRHgH\nsobNvEx69HaMrCZZN4vTXduKIVkd0m/QXOaM4Akh3yUufQqejHnQ8uFE85P3b7J7\nLGkkdR8RkYKB65dTTMXT6m8ME4cxsWogU/qGlvtAdyc+1cmfXYxYZ8fTRGS40gC3\nHCuBOFBrSxq6orxZ2JZWF2jBkQKBgQDWoun6j1HfrlPza04wsczDoRIYrA0ews3o\naLa1XuY4agFFKB9M7XpJghzYxXlAQLoHxw3H6dzwy0CrgAP3O9O4qdpyMuQ+pLSG\naXKxAhiwaq7DRy/iZt3EPxFLCkFghreQfxUcG9s8RM5lMSqphGuNI4GcJRC0rmX2\nZkkNygu50wKBgAksmTGwqHLuweyFiAxwajiilgVne/yMUBSz0DaDmxEnTMml9Wqq\nH+hKTMusEwf0nTFbZRdj9xi8BFLzDpMs/OjUTcItoaj5auUrS5MRaef9x9jx9z8d\nF3dfkfm65/yNjA6KOCEAH/8K4tFRF6mkJY1o7rwjVOZMGbUMG+sqjTWhAoGBAJAD\nbaT95vyDlracSDFqCy8z8tV1E7SRFuGa6QTW8PfnQITrf9z49nU+BSb5kPqos2mm\niLubUfCLIBAya/bGQLAF35mCRh02HB6XwCm+c1xjqHFEYX+yb5hOjMbh0a33llEw\nw7RBiJ9ut2G0VKC7RgLEUSG4yPXCko16YggLikSbAoGAEgNJIUS9lQmnfYP9c4v9\nqEhGBHPiZu4DHTvNAyeI7UdHhWQ+aBXSE+F+E5dZ8JaFDMSFdRNo1VpqYQp1qG8Q\nOBdiI/AyItckXH7Yk/3cC1D0/krzpJA8qei7AoYOAtYNpQsTV/lFs8K8MGR1p5zB\n84z/FfQMz1ImpjGGI9JC+Uw=\n-----END PRIVATE KEY-----\n",
  "client_email": "be-atividadeiv@andre-382123.iam.gserviceaccount.com",
  "client_id": "101374428112688224604",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/be-atividadeiv%40andre-382123.iam.gserviceaccount.com"
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
