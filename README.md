AWSIoTButtonSampler
=======

# Requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [Docker for Mac](https://www.docker.com/docker-mac)
- [yarn](https://yarnpkg.com)

# Development

- [pyenv](https://github.com/pyenv/pyenv)
- [localstack](https://github.com/localstack/localstack)

## Setting

### Install [pyenv](https://github.com/pyenv/pyenv)

```bash
$ brew install pyenv
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
$ exec $SHELL -l
$ pyenv install 3.6.4
```

### Make of virtual environment and dependent libraries

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install pipenv
$ pipenv install
```

## Development environment

### Activate of virtual environment

- Activate

```bash
$ source .venv/bin/activate
```

- Deactivate

```bash
$ deactivate
```

### Using [localstack](https://github.com/localstack/localstack)

- Start-up

```bash
$ make localstack-up
```

- Stop

```bash
$ make localstack-stop
```

## Unit test

```bash
$ make unit-test
```

## Lint

```bash
$ make lint
```

# Deploy

## Configure AWS credentials

- `~/.aws/credentials`

```bash
[aws-iot-development]
aws_access_key_id = <your_aws_access_key_id>
aws_secret_access_key = <your_aws_secret_access_key>
```

- `~/.aws/config`

```bash
[profile aws-iot-development]
region = us-east-1
output = json
```

## Construction of AWS SAM deployment environment

- [AWSSAMDeployEnvironmentConstruction](https://github.com/kongmingstrap/AWSSAMDeployEnvironmentConstruction)

## Setting AWS

- Please set [SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)

| Parameter | Value |
| --- | --- |
| SlackWebhookURL | <your_genarate_slack_hooks_url> |

## Deploy to AWS

```bash
$ make deploy
```