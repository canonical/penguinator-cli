# Azure Image Testing for Linux CLI

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/aitl-cli)

A Python client for the Azure Image Testing for Linux API. (Azure Image Testing for Linux is a Microsoft Azure Service.)

## Usage

First, set the following environment variables:

```bash
export AZURE_TENANT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
export AZURE_CLIENT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
export AZURE_CLIENT_SECRET='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
export AZURE_SUBSCRIPTION_ID=
export AZURE_RESOURCE_GROUP=
```

```bash
Usage: aitl-cli [OPTIONS] COMMAND [ARGS]...

  CLI client for the Azure Image Testing for Linux API

Options:
  --help  Show this message and exit.

Commands:
  create-job       Create a new test job
  create-template  Create a new test job template
  get-job          Get a test job.
  get-template     Get a test job template.
  list-jobs        List all the test jobs.
  list-templates   List all the test job templates.
```

## Installation

Install the snap from the store:

```bash
sudo snap install aitl-cli
```

For developers:

```bash
git clone git@github.com:canonical/aitl-cli.git
cd aitl-cli
python3 -m venv .venv
source .venv/bin/activate
pip install --editable .
```

To build the snap locally:

```bash
sudo snap install --classic snapcraft
snapcraft
```
