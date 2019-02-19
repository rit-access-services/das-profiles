# Department of Access Services Profiles

DAS Profiles is a microservice built with [API Star](https://github.com/tomchristie/apistar) and [Zappa](https://github.com/Miserlou/Zappa). The service offers an endpoint that connects to a serverless AWS Lambda function and returns a JSON response containing all of the Department of Access Services profile data [scraped](https://www.ntid.rit.edu/das/directory) from the staff website.

## API Endpoint

Access the data by visiting the following endpoint:

https://sla8ppnryg.execute-api.us-east-1.amazonaws.com/production


## Format

The JSON Response conforms to the following PropTypes contract:

```javascript
Profile = PropTypes.shape({
  'photo': PropTypes.string,
  'first_name': PropTypes.string,
  'last_name': PropTypes.string,
  'office': PropTypes.string,
  'job_title': PropTypes.string,
  'phone': PropTypes.string,
})
Profiles = PropTypes.objectOf(Profile)
```

A sample output would look like:

```
{
   "rkmdis":{
      "photo":"https://www.ntid.rit.edu/directory/newphotos/JJVHRZZTSZKTV.jpg",
      "first_name":"Rachel",
      "last_name":"Abbett",
      "office":"Office: HLC-1103",
      "job_title":"Interpreter",
      "phone":"5854754632"
   },
   "ajadis":{
      "photo":"https://www.ntid.rit.edu/directory/newphotos/MZNLTZZVJLJVN.jpg",
      "first_name":"Abie",
      "last_name":"Abrams",
      "office":"Office: HLC-2222",
      "job_title":"Associate Interpreter",
      "phone":"5854752251"
   },

   ...
}

```

## Development

You do not need AWS to develop all parts of this application, for instance you can work on the `scraper.py` and create tests that do not rely on the AWS functions. If you want full access to develop you will need valid [AWS credentials](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/) that authenticate through `IAM` to this service, meaning I would need to add you. Alternatively you can fork and set up your own AWS account. When you add an IAM policy for Zappa, the [following worked for me](https://github.com/Miserlou/Zappa/issues/244#issuecomment-303697308).

## Deploy

This is deployed as an AWS Lambda function through Zappa. The app is a wsgi app that exposes a `/` and `/profiles` endpoint that have the same functionality. They read the json data from S3 and return it. Zappa is setup to call the `app.refresh_profile_data` function according to the interval rate defined in `zappa_settings.json`. This function invocation scrapes the NTID website and updates profile information, storing the result on S3.

To deploy a new update:

```shell
$ zappa update production
```

If you are changing any routes in the app you will need to do a fresh deploy:
```shell
$ zappa deploy production
```

