# python-project-template

A python project template for GitHub Repos. This project has a mirror in our private Gitlab server here: https://git.oxolo.com/development/github/python-project-template
You can check the status of the CI pipelines there. never push a change to the mirror!

## Formatting
To format the python files in the project run the following command in the root folder:
```shell
# black formatting
black .

# comments and docstring formatting
docformatter --in-place -r .

# imports formatting
isort .

# run hadolint for Dockerfile linting - consider addressing errors before pushing
docker run --rm -i hadolint/hadolint < Dockerfile
# 
```

## Documentation:
The static website will be hosted on S3 bucket. For each new project:
1. Create a new S3 bucket and enable public access
2. enable website hosting from Bucket Properties => Static website hosting 
3. enable new bucket policy from permissions => Bucket policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::BUCKET-NAME/*"
        }
    ]
}
```
`BUCET-NAME` for this project is `github-python-project-template-doc`
5. Change the upload-to-s3 job in `.gitlab-ci.yml` file and use the BUCKET-NAME you created
6. Check the website endpoint from the Bucket Properties => Static website hosting. 

The URL to pages for this template is http://github-python-project-template-doc.s3-website-us-east-1.amazonaws.com/

7. You can also configure static domain name as explained here: https://docs.aws.amazon.com/AmazonS3/latest/userguide/website-hosting-custom-domain-walkthrough.html

## Package Versioning
for each new change please update the package version in `setup.py`. Please follow  [semantic versioning](https://semver.org/): Given a version number `MAJOR.MINOR.PATCH`, increment the:

      1. **MAJOR** version when you make incompatible API changes,
      2. **MINOR** version when you add functionality in a backwards compatible manner, and
      3. **PATCH** version when you make backwards compatible bug fixes.