# Penguinator CLI

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/penguinator-cli)

A Python API client for the Penguinator API: https://penguinatorstarter.powerappsportals.com/webapis2/

## Usage

```bash
Usage: penguinator-cli [OPTIONS] COMMAND [ARGS]...

  CLI client for the Penguinator API
  (https://penguinatorstarter.powerappsportals.com/webapis2/)

Options:
  --help  Show this message and exit.

Commands:
  create-job          Create a new test job
  get-job             Get a test job.
  get-projects        Get a test project
  list-jobs           List all the test jobs
  list-projects       List all the test projects
  list-subscriptions  List the subscriptions that can be used for testing
  list-test-suites    List the test suite available
```

## Installation

Install the snap from the store:

```bash
sudo snap install penguinator-cli
```

For developers:

```bash
git clone git@github.com:canonical/penguinator-cli.git
cd penguinator-cli
python3 -m venv .venv
source .venv/bin/activate
pip install --editable .
```

To build the snap locally:

```bash
sudo snap install --classic snapcraft
snapcraft
```
