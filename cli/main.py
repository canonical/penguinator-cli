import requests
import click
import os
import json


RESOURCE_PROVIDER = "Microsoft.AzureImageTestingForLinux"
API_VERSION = "2023-08-01-preview"

TENANT_ID = os.getenv("AZURE_TENANT_ID")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP")


def _get_endpoint(segment, **kwargs):
    resource_group = kwargs["resource_group"]
    return (
        f"https://eastus2euap.management.azure.com/subscriptions/{SUBSCRIPTION_ID}/"
        f"resourceGroups/{resource_group}/providers/{RESOURCE_PROVIDER}/"
        f"{segment}?api-version={API_VERSION}"
    )


def _common_options(func):
    options = [
        click.option(
            "--resource-group",
            "-rg",
            default=RESOURCE_GROUP,
            help="Azure Resource Group name"
        ),
    ]
    return _apply_options(func, options)


def _template_options(func):
    options = [
        click.option("--vm-size", "-s", help="VM size"),
        click.option("--priority", "-p", help="Test case priority"),
        click.option("--case-name", "-c", help="Test case names"),
        click.option(
            "--location",
            "-l",
            default="westus3",
            help="Job template location, it's not required to be changed",
        ),
        click.option(
            "--region",
            "-r",
            multiple=True,
            default=["westeurope"],
            help="Regions where the test resources will be provisioned",
        ),
    ]
    return _apply_options(func, options)


def _apply_options(func, options):
    for option in reversed(options):
        func = option(func)
    return func


def _create_template(vm_size, priority, case_name, location, regions):
    template = {
        "templateTags": [],
    }

    selection = {}
    if priority:
        selection["casePriority"] = [int(x) for x in priority.split(",") if x]
    if case_name:
        selection["caseName"] = [x for x in case_name.split(",") if x]

    if selection:
        template["selections"] = [selection]
    if regions:
        template["region"] = regions
    else:
        template["region"] = []
    if vm_size:
        template["vmSize"] = [vm_size]
    else:
        template["vmSize"] = []

    return template


def _output_result(resp):
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    print(json.dumps(resp.json(), indent=2))


def auth() -> str:
    auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
    resource = "https://management.azure.com/"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "resource": resource,
    }
    resp = requests.post(auth_url, data=data)
    try:
        resp.raise_for_status()
    except:
        print(resp.json())
        raise

    resp_json = resp.json()
    token = resp_json["access_token"]
    return token


@click.group()
@click.pass_context
def cli(ctx):
    """
    CLI client for the Azure Image Testing for Linux API
    """
    token = auth()
    ctx.obj = dict()
    session = requests.session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    ctx.obj["session"] = session


@cli.command()
@click.pass_context
@_common_options
def list_templates(ctx, **kwargs):
    """
    List all the test job templates.
    """
    endpoint = _get_endpoint("jobTemplates", **kwargs)

    session = ctx.obj["session"]

    resp = session.get(endpoint)
    _output_result(resp)


@cli.command()
@click.pass_context
@_common_options
@click.option("--name", "-n", help="Job template name", required=True)
def get_template(ctx, name: str, **kwargs):
    """
    Get a test job template.
    """
    endpoint = _get_endpoint(f"jobTemplates/{name}", **kwargs)

    session = ctx.obj["session"]

    resp = session.get(endpoint)
    _output_result(resp)


@cli.command()
@click.pass_context
@_common_options
@click.option("--name", "-n", help="Job template name", required=True)
@_template_options
def create_template(
    ctx, name: str, vm_size: str, priority: str, case_name: str, location: str, region: list[str], **kwargs
):
    """
    Create a new test job template
    """
    endpoint = _get_endpoint(f"jobTemplates/{name}", **kwargs)

    session = ctx.obj["session"]

    template = _create_template(vm_size, priority, case_name, location, region)

    payload = {"location": location, "name": name, "properties": template}
    resp = session.put(endpoint, json=payload)
    _output_result(resp)


@cli.command()
@click.pass_context
@_common_options
def list_jobs(ctx, **kwargs):
    """
    List all the test jobs.
    """
    endpoint = _get_endpoint("jobs", **kwargs)

    session = ctx.obj["session"]

    resp = session.get(endpoint)
    _output_result(resp)


@cli.command()
@click.pass_context
@_common_options
@click.option("--name", "-n", required=True)
def get_job(ctx, name: str, **kwargs):
    """
    Get a test job. Can be used to get the current status of the job.
    """
    endpoint = _get_endpoint(f"jobs/{name}", **kwargs)

    session = ctx.obj["session"]

    resp = session.get(endpoint)
    _output_result(resp)


@cli.command()
@click.pass_context
@_common_options
@click.option("--name", "-n", required=True, help="Job name")
@click.option(
    "--marketplace-image-urn",
    "-u",
    help='URN of the image ("az vm image list -p Canonical --all")',
)
@click.option("--vhd-sas-url", "-v", type=str, help="SAS URL of a VHD to test")
@click.option("--architecture", "-a", type=click.Choice(['x64', 'arm64']), help="Architecture of the image")
@click.option(
    "--vm-generation", "-g", default=2, type=int, help="Hyper-V generation (1 or 2)"
)
@click.option(
    "--region", "-r", default=["westeurope"], type=str, multiple=True, help="Provisioning region for test resources"
)
@click.option("--template-name", "-t", type=str, help="Job template name")
@_template_options
def create_job(
    ctx,
    name: str,
    marketplace_image_urn: str,
    vhd_sas_url: str,
    architecture: str,
    template_name: str,
    vm_generation: int,
    vm_size: str,
    priority: str,
    case_name: str,
    location: str,
    region: list[str],
    **kwargs,
):
    """
    Create a new test job
    """
    endpoint = _get_endpoint(f"jobs/{name}", **kwargs)

    session = ctx.obj["session"]

    image = {
        "vhdGeneration": vm_generation,
        "architecture": architecture,
    }
    if marketplace_image_urn:
        image["type"] = "marketplace"
        image_parts = marketplace_image_urn.split(":")
        if len(image_parts) != 4:
            raise ValueError(
                "marketplace_image_urn should be in the format of 'publisher:offer:sku:version'"
            )
        image["publisher"] = image_parts[0]
        image["offer"] = image_parts[1]
        image["sku"] = image_parts[2]
        image["version"] = image_parts[3]
    elif vhd_sas_url:
        image["type"] = "vhd"
        image["url"] = vhd_sas_url
    else:
        raise ValueError(
            "One of --vhd-sas-url or --marketplace-image-urn should be passed."
        )

    template = _create_template(vm_size, priority, case_name, location, region)

    payload = {
        "location": location,
        "properties": {
            "jobTemplateName": template_name,
            "jobTemplateInstance": template,
            "image": image,
        },
    }

    resp = session.put(endpoint, json=payload)
    _output_result(resp)


if __name__ == "___main__":
    main()
