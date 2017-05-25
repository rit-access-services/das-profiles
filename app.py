# Standard Library Imports
import json
import os
from datetime import datetime

# Third Party Library Imports
import boto3
from apistar import App, Route, environment, schema
from apistar.http import Response

from scraper import DasProfileScraper


BUCKET_NAME = os.environ.get('bucket_name', 'zappa-ena9mj25k')


def refresh_profile_data():
    scraper = DasProfileScraper()
    profiles = scraper.scrape()
    body = json.dumps(profiles).encode()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    try:
        res = bucket.put_object(
            Key='store/das-profiles.json',
            Body=body,
            Metadata={'uploaded': str(datetime.utcnow())})
    except Exception:
        return Response(data='', status=500)

    if res is None:
        return Response(data='', status=500)

    res = res.get()
    response_metadata = res.get('ResponseMetadata', {})
    status = response_metadata.get('HTTPStatusCode', 500)
    amazon_s3_headers = response_metadata.get('HTTPHeaders', {})
    status = 204 if status == 200 else status
    return Response(
        data='',
        status=status,
        headers={'ContentLength': 0,
                 'AmazonS3Headers': amazon_s3_headers})


def get_all_profiles():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    profiles = bucket.Object('store/das-profiles.json').get()['Body'].read()
    return profiles.decode()


class Env(environment.Environment):
    properties = {
        'DEBUG': schema.Boolean(default=False),
    }


env = Env()


settings = {
    'DEBUG': env['DEBUG'],
}

routes = [
    Route('/', 'GET', get_all_profiles),
    Route('/profiles', 'GET', get_all_profiles),
]

app = App(routes=routes, settings=settings)

wsgi_app = app.wsgi
