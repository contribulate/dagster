# start_asset_marker

from dagster_aws.pipes import PipesECSClient
from docutils.nodes import entry

from dagster import AssetExecutionContext, asset


@asset
def ecs_pipes_asset(context: AssetExecutionContext, pipes_ecs_client: PipesECSClient):
    return pipes_ecs_client.run(
        context=context,
        task_definition="my-task",
    ).get_materialize_result()


# end_asset_marker

# start_definitions_marker

from dagster import Definitions  # noqa
from dagster_aws.pipes import PipesS3MessageReader


defs = Definitions(
    assets=[ecs_pipes_asset],
    resources={"pipes_ecs_client": PipesECSClient()},
)

# end_definitions_marker
