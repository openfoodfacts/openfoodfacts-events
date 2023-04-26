from pytest_alembic.runner import MigrationContext
from pytest_alembic.tests import test_single_head_revision
from pytest_alembic.tests import test_upgrade
from pytest_alembic.tests import test_model_definitions_match_ddl
from pytest_alembic.tests import test_up_down_consistency
def test_migration_c5920d3da32f(alembic_runner: MigrationContext):
        alembic_runner.migrate_up_to("c5920d3da32f")
        events_table = alembic_runner.table_at_revision("events")
        badges_table = alembic_runner.table_at_revision("badges")
        assert events_table is not None
        assert badges_table is not None
        assert len(events_table.columns) == 7
        assert len(badges_table.columns) == 5