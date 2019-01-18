SHELL = /usr/bin/env bash -xeuo pipefail

localstack-up:
	@docker-compose up -d localstack

localstack-stop:
	@docker-compose stop localstack

lint:
	@python -m flake8 \
		src \
		tests

unit-test:
	@for test_dir in $$(find tests/unit -maxdepth 1 -type d); do \
		handler=$$(basename $$test_dir); \
		if [[ $$handler =~ unit|__pycache__|fixtures ]]; then continue; fi; \
		python_path=src/handlers/$$handler; \
		proj=src/handlers/$$handler; \
		AWS_DEFAULT_REGION=ap-northeast-1 \
		AWS_ACCESS_KEY_ID=dummy \
		AWS_SECRET_ACCESS_KEY=dummy \
		PYTHONPATH=$$python_path \
			python -m pytest tests/unit/$$handler --cov-config=./setup.cfg --cov=$$proj -vv; \
	done

validate:
	@aws cloudformation validate-template \
		--template-body file://sam.yml

deploy:
	@aws cloudformation package \
						--template-file sam.yml \
						--s3-bucket sam-artifacts-$$(aws sts get-caller-identity | jq .Account | sed 's/\"//g')-ap-northeast-1 \
						--output-template-file template.yml

	@aws cloudformation deploy \
						--template-file template.yml \
						--stack-name iot-button-functions \
						--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
						--role-arn arn:aws:iam::$$(aws sts get-caller-identity | jq .Account | sed 's/\"//g'):role/sam-deploy/sam-deploy-role \
						--no-fail-on-empty-changeset

.PHONY: \
	localstack-up \
	localstack-down \
	lint \
	unit-test \
	validate \
	deploy
