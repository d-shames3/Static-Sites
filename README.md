# Static Sites

Static site generator written in Python. Takes MarkDown files and renders them as HTML using local server.

## Steps to Run Locally

1. Clone the the repo
1. Make sure you are in the root directory of the repo
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. Run the `local_deploy.sh` script
1. Open [localhost](https://localhost:8888) to see the site

## Steps to Deploy to Hosted Static Site via S3

1. Clone/fork the the repo
1. Follow the [AWS tutorial](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/getting-started-secure-static-website-cloudformation-template.html) on setting up infra for a static website hosted on AWS s3
1. Add your environment variables in Github Secrets (see the aws_s3_deploy.yml file to see how these env vars should be named)
1. Run the `s3_deploy.sh` script
1. Nav to your domain to see the site
