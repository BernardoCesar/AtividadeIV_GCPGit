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
  "private_key_id": "81f0793dbcf0cfc3434483a6689434421dab0397",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMgtMywwU8UtsY\nTWKfXDhQ71421LnSxY5bZ4MvD4xal3B1pf6ftf0+3weQ25mx14qv0eNNxrVXK3Vp\n3a55eIO0uKvDADxdplSXl6ilrMJ4zW9W0umUFzxf8CbFhI0U9VsKDQTcnpZZOTqj\naz4h7LDWIwGHmS9Uxc763eyQH924nhhmdf96ibAkI4mVZMgcNY9nxY+pyjADRHHY\np2g5v3KuW5pAlg4QTC83j3In6MtPTA2WNeeZ3npSq6fTwdDVeOa7IRP5ZDKe7FlK\nH2XZulCNCOVUkojIciFU0+IUci8nLpRN7tMiL5CPkVwsEK+R1VFQ+Ls4lOMhaGlR\nQ/CyL/KnAgMBAAECggEADu1DKJxVYH7HrdfQHMOO+x4aT7Q2tlL9cSx2X1P2/l6G\nGQAub04wMSUqmM1+dupXHaTn8bOEMg8vX04mP7vZ5eUb6RXphTuKE+DZsIxe5JEe\n0RGzdllv0OAAl6Z1Sa25OsJfTXibW3qZQUSnLbPoTRwTyE4YLbIDMApMpVEkgY0r\nruXgWqApsDv3RHEZX5yhweDvVNEmtl98Jy1p867w/2CeYu+iqsJcfZtSjXHPaiYz\nvx/qZZW0zgH66beDMjcGo31IMXJuIAlOrX9DkFtSigsunHEUo86z9xnYY0/hGra4\nkrN/E967lpKkxpmCghXu6ipY8SnfsLGqjUTKTXyD2QKBgQD/OlQf6eRksaFQASd7\nZfjSR4PYcMEXJYF6OiRj/P9O8uRPtbmNH5PYJn4fYQgUPVIDnter0LHcF8JtL7aq\nsCWpzRWr+GyxfngtAYofXWfb7Ztb41gyNVaVaLdv7nKnc4QHcH0Bx24s8+tzgsLW\nQi5Y++kmB0tJtzaBM7Xrj09kjQKBgQDNITd7M6rPzGqunNuS/zxw0wDXFFw8hjdf\nsBFN7U2FLBmX01A7UudIpoiAFlrJlvrTbJoq7BLP45zUljEOLyOlhSRaJXRVDl+g\nYtpiwMG/UJwztxi8JduwmobunPdMTrUso0Fy8GntGhQKsl2T2C+qsXOlUSmHNack\nRgzGTTAZAwKBgDoTysrMTVWAeiWbbaGNzbYD4gOhfL7IoRLwIhHCo1ISwVNGFegA\nFINuFusLCGyam4wJXChTv/VGTs7LubRTiu59pX3RdOJa1fvfys9iUNzhz6V0MUCT\nlJVBE+TbjKmABr4uobOC7xY5lw1c5vscajGDeUVXCZHHqBZ0buQgYz+NAoGBAMRU\nB2r2b4TFLFIFNS7C9REzErnH9ePDvdnqhRVli21rYO9sQ30UAuMI6NpXCvuoclbK\nud9c5UBtpBvfyAHAYki4Xquc73O89w9lrYkY3hcCyw3AL39caKDltUFJoHM7XbHk\nau7cZTWWYRo/zsqC/lRL1NikDrAnTNqt5Ooi1GcLAoGATm05vQjp8MCGNioWXQft\nF4YFdT3kUQwxCM/njXMZB0P4D5OQfFZ354kpe3HxGPRf3hZAu0+JcB5s/IUJIFzB\nax8WcV9cWhVSC6ySLqUd71ND8owyeXIdfTtfwgaVzfZbI1JpnLvoZvA5EulZfOlb\nnz0LcP4w2r0S3zRYSg8Y0sc=\n-----END PRIVATE KEY-----\n",
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
