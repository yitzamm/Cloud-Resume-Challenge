.PHONY: build

build:
	sam build

login:
	aws-vault exec yitza --no-session

deploy-infra:
	sam build; aws-vault exec yitza --no-session -- sam deploy

deploy-site:
	aws-vault exec yitza --no-session -- aws s3 sync ./resume-site s3://yitza-resume-app

post:
	Invoke-WebRequest -Uri "https://2vc19emnea.execute-api.us-east-1.amazonaws.com/Prod/put" -Method POST

invoke-put:
	sam local invoke PutFunction --event .\event.json --env-vars .\env.json

invoke-get:
	sam build; aws-vault exec yitza --no-session -- sam local invoke GetFunction

commit:
	git commit -m "Update files"
	git push