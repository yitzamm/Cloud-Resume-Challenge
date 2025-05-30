.PHONY: build

build:
	sam build

deploy-infra:
	sam build && aws-vault exec yitza --no-session -- sam deploy

deploy-site:
	aws-vault exec yitza --no-session -- aws s3 sync ./resume-site s3://resume-app