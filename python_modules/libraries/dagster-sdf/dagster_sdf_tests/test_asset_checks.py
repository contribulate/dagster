import os

from dagster import AssetExecutionContext, AssetKey, materialize
from dagster_sdf.asset_decorator import sdf_assets
from dagster_sdf.dagster_sdf_translator import DagsterSdfTranslator, DagsterSdfTranslatorSettings
from dagster_sdf.resource import SdfCliResource
from dagster_sdf.sdf_workspace import SdfWorkspace

from dagster_sdf_tests.sdf_workspaces import lineage_asset_checks_path


def test_asset_checks_passing() -> None:
    sdf = SdfCliResource(
        workspace_dir=os.fspath(lineage_asset_checks_path),
        global_config_flags=["--log-form=nested"],
    )
    environment = "passing_tests"
    sdf_cli_invocation = sdf.cli(["compile", "--save", "table-deps"], environment=environment)
    assert sdf_cli_invocation.is_successful()
    target_dir = sdf_cli_invocation.target_dir
    dagster_sdf_translator = DagsterSdfTranslator(
        settings=DagsterSdfTranslatorSettings(enable_asset_checks=True)
    )

    @sdf_assets(
        workspace=SdfWorkspace(
            workspace_dir=lineage_asset_checks_path, target_dir=target_dir, environment=environment
        ),
        dagster_sdf_translator=dagster_sdf_translator,
    )
    def my_sdf_assets(context: AssetExecutionContext, sdf: SdfCliResource):
        yield from sdf.cli(
            ["test", "--save", "info-schema"],
            target_dir=target_dir,
            environment=environment,
            dagster_sdf_translator=dagster_sdf_translator,
            context=context,
        ).stream()

    result = materialize(
        [my_sdf_assets],
        resources={"sdf": SdfCliResource(workspace_dir=lineage_asset_checks_path)},
    )

    assert result.success
    assert len(result.get_asset_check_evaluations()) > 0
    evaluation = result.get_asset_check_evaluations()[0]
    assert evaluation.asset_key == AssetKey(["lineage", "pub", "middle"])
    assert evaluation.passed


def test_asset_checks_failing() -> None:
    sdf = SdfCliResource(
        workspace_dir=os.fspath(lineage_asset_checks_path),
        global_config_flags=["--log-form=nested"],
    )
    dagster_sdf_translator = DagsterSdfTranslator(
        settings=DagsterSdfTranslatorSettings(enable_asset_checks=True)
    )
    environment = "failing_tests"
    sdf_cli_invocation = sdf.cli(["compile", "--save", "table-deps"], environment=environment)
    assert sdf_cli_invocation.is_successful()
    target_dir = sdf_cli_invocation.target_dir

    @sdf_assets(
        workspace=SdfWorkspace(
            workspace_dir=lineage_asset_checks_path, target_dir=target_dir, environment=environment
        ),
        dagster_sdf_translator=dagster_sdf_translator,
    )
    def my_sdf_assets(context: AssetExecutionContext, sdf: SdfCliResource):
        yield from sdf.cli(
            ["test", "--save", "info-schema"],
            target_dir=target_dir,
            environment=environment,
            context=context,
            dagster_sdf_translator=dagster_sdf_translator,
            raise_on_error=False,
        ).stream()

    result = materialize(
        [my_sdf_assets],
        resources={"sdf": SdfCliResource(workspace_dir=lineage_asset_checks_path)},
    )

    assert result.success
    assert len(result.get_asset_check_evaluations()) > 0
    evaluation = result.get_asset_check_evaluations()[0]
    assert evaluation.asset_key == AssetKey(["lineage", "pub", "middle"])
    assert not evaluation.passed
