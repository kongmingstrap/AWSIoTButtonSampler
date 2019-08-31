SHELL = /usr/bin/env bash -xeuo pipefail

localstack-up:
	@docker-compose up -d localstack

localstack-stop:
	@docker-compose stop localstack

build:
	@for handler in $$(find src/layers -maxdepth 2 -type f -name 'Pipfile'); do \
		package_dir=$$(dirname $$handler); \
		pwd_dir=$$PWD; \
		docker_name=lot-button-sampler-$$(basename $$package_dir); \
		cd $$package_dir; \
		mkdir -p python/lib/python3.7; \
		pipenv lock --python $$(which python) --requirements > requirements.txt; \
		docker image build --tag $$docker_name .; \
		docker container run -it --name $$docker_name $$docker_name; \
		rm requirements.txt; \
		cd python/lib/python3.7; \
		docker container cp $$docker_name:/workdir site-packages; \
		docker container rm $$docker_name; \
		docker image rm $$docker_name; \
		cd $$pwd_dir; \
	done

build-for-mac:
	@for handler in $$(find src/layers -maxdepth 2 -type f -name 'Pipfile'); do \
		package_dir=$$(dirname $$handler); \
		pwd_dir=$$PWD; \
		docker_name=lot-button-sampler-$$(basename $$package_dir); \
		cd $$package_dir; \
		pipenv lock --python $$(which python) --requirements > requirements.txt; \
		pip install -r requirements.txt -t python/lib/python3.7/site-packages; \
		rm requirements.txt; \
		cd $$pwd_dir; \
	done

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
		PYTHONPATH=src/layers/utils/python:$$python_path \
			python -m pytest tests/unit/$$handler --cov-config=./setup.cfg --cov=$$proj -vv; \
	done

validate:
	@aws cloudformation validate-template \
		--template-body file://sam.yml

install:
	@pip install requests -t src/handlers/message_notifier

clean:
	@rm -rf src/handlers/message_notifier/bin
	rm -rf src/handlers/message_notifier/certifi*
	rm -rf src/handlers/message_notifier/chardet*
	rm -rf src/handlers/message_notifier/idna*
	rm -rf src/handlers/message_notifier/requests*
	rm -rf src/handlers/message_notifier/urllib3*

deploy: install
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

	make clean

.PHONY: \
	localstack-up \
	localstack-down \
	build \
	build-for-mac \
	lint \
	unit-test \
	validate \
	install \
	clean \
	deploy
