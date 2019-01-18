AWSIoTButtonSampler
=======

# Requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [Docker for Mac](https://www.docker.com/docker-mac)
- [yarn](https://yarnpkg.com)

# Development

## unit test

```
TODO
```

## lint

```
TODO
```

# Deploy

## 1. Configure AWS credentials

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

## 2. Construction of AWS SAM deployment environment

- [AWSSAMDeployEnvironmentConstruction](https://github.com/kongmingstrap/AWSSAMDeployEnvironmentConstruction)

## 3. Setting AWS

- Please set [SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)

| Parameter | Value |
| --- | --- |
| ChatWorkToken | <your_chatwork_token> |
| ChatworkRoomId | <your_chatwork_room_id> |
| SlackWebhookURL | <your_genarate_slack_hooks_url> |

## 4. Deploy to AWS

```bash
$ make deploy
```