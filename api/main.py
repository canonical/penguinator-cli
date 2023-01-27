import requests
import click
import os
import urllib
import json

API_BASE_URL = 'https://penguinatorapi2.azure-api.net/'

TENANT_ID = os.getenv("AZURE_TENANT_ID")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")


def auth() -> str:
    auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    scope = "api://7395f717-3e16-4e02-b95f-802a15a82d47/.default"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": scope,
    }
    resp = requests.post(auth_url, data=data)
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    resp_json = resp.json()
    token = resp_json['access_token']
    return token


@click.group()
@click.pass_context
def cli(ctx):
    """
    CLI client for the Penguinator API (https://penguinatorstarter.powerappsportals.com/webapis2/)
    """
    token = auth()
    ctx.obj = dict()
    session = requests.session()
    session.headers.update({'Authorization': f'Bearer {token}'})
    ctx.obj['session'] = session


@cli.command()
@click.pass_context
def list_projects(ctx):
    """
    List all the test projects
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "projects")

    session = ctx.obj['session']

    resp = session.get(endpoint)
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
@click.option('--project-id', '-p', required=True)
def get_projects(ctx, project_id: str):
    """
    Get a test project
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "projects")

    session = ctx.obj['session']

    resp = session.get(
        endpoint,
        params={'id': project_id}
    )
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
def list_jobs(ctx):
    """
    List all the test jobs
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "jobs")

    session = ctx.obj['session']

    resp = session.get(endpoint)
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
@click.option('--job-id', '-j', required=True)
def get_job(ctx, job_id: str):
    """
    Get a test job. Can be used to get the current status of the job.
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "jobs")

    session = ctx.obj['session']

    resp = session.get(
        endpoint,
        params={'id': job_id}
    )
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
def list_subscriptions(ctx):
    """
    List the subscriptions that can be used for testing
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "subscriptions")

    session = ctx.obj['session']

    resp = session.get(
        endpoint,
    )
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
def list_test_suites(ctx):
    """
    List the test suite available
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "suites")

    session = ctx.obj['session']

    resp = session.get(
        endpoint,
    )
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


@cli.command()
@click.pass_context
@click.option('--project', '-p', required=True, help='ID of the test project to use')
@click.option('--test-suite', '-t', required=True, help='Test suite to use')
@click.option('--subscription', '-s', required=True, help='Internal penguinator ID of the "subscription" to use')
@click.option('--marketplace-image-urn', '-u', type=str, help='URN of the image ("az vm image list -p Canonical --all")')
@click.option('--vhd-sas-url', '-v', type=str, help='SAS URL of a VHD to test')
@click.option('--vm-generation', '-g', default=2, type=int, help="Hyper-V generation (1 or 2)")
def create_job(ctx, project: str, test_suite: str, subscription: str, marketplace_image_urn: str, vhd_sas_url: str, vm_generation: int):
    """
    Create a new test job
    """
    endpoint = urllib.parse.urljoin(API_BASE_URL, "jobs")

    session = ctx.obj['session']
    payload = {
        'test_project': project,
        'test_suite': test_suite,
        'subscription': subscription,
        'vm_generation': vm_generation,
    }

    if marketplace_image_urn:
        payload['marketplace_image_urn'] = marketplace_image_urn
    elif vhd_sas_url:
        payload['vhd_sas_url'] = vhd_sas_url
    else:
        raise ValueError(
            "One of --vhd-sas-url or --marketplace-image-urn should be passed."
        )

    resp = session.post(
        endpoint,
        json=payload
    )
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json()))


if __name__ == "___main__":
    main()
