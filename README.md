# The Cloud Resume Challenge
June 16, 2025

I'm taking on the Cloud Resume Challenge, using AWS to build a fully automated, serverless resume site. This project sharpens my skills in cloud architecture, infrastructure as code, CI/CD, and monitoring while showcasing my ability to integrate scalable AWS solutions.

Link to the dev challenge: https://cloudresumechallenge.dev/

## Architecture Diagram

![Image](https://github.com/user-attachments/assets/e0c0a45b-e1be-4598-aab8-ddb732be0603)

## Tools, Services and Integration

- HTML and CSS to write and style the resume.
- S3 to deploy the static website.
- HTTPS and CloudFront to secure the S3 URL.
- DNS and Route 53 to access the website.
- Javascript - For writing the visitor counter.
- DynamoDB - For retrieving and updating the count.
- API - Bridge to communicate between Javascript and DynamoDB. Will use AWS’s API Gateway and Lambda for this step.
- Python to code and test the Lambda function.
- IaC - The DynamoDB table, API Gateway and Lambda function should be defined in a SAM or Terraform template.
- GitHub Repo for the back-end code (CI/CD).
- CI/CD Back-end via GitHub actions - Pushing updates to the Python code should get the tests to run. If the test passes, the SAM/Terraform application will get packaged and deployed.
- CI/CD Front-end - Pushing new website code should get the S3 bucket updated. CloudFront cache should be invalidated for this step.
- NOTE: AWS credentials must not be committed to source control.
- Blog post - Final testing and documentation.

Step-by-step project summary: https://drive.google.com/file/d/15bihRgbjwJ7gOwyHrcavxLwxeTvpc1lZ/view
