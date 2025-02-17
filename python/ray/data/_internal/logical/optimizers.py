from typing import List

from ray.data._internal.logical.interfaces import (
    Rule,
    Optimizer,
    LogicalPlan,
    PhysicalPlan,
)
from ray.data._internal.logical.rules import (
    OperatorFusionRule,
    ReorderRandomizeBlocksRule,
)
from ray.data._internal.logical.util import record_operators_usage
from ray.data._internal.planner.planner import Planner


class LogicalOptimizer(Optimizer):
    """The optimizer for logical operators."""

    @property
    def rules(self) -> List[Rule]:
        return [ReorderRandomizeBlocksRule()]


class PhysicalOptimizer(Optimizer):
    """The optimizer for physical operators."""

    @property
    def rules(self) -> List["Rule"]:
        return [OperatorFusionRule()]


def get_execution_plan(logical_plan: LogicalPlan) -> PhysicalPlan:
    """Get the physical execution plan for the provided logical plan.

    This process has 3 steps:
    (1) logical optimization: optimize logical operators.
    (2) planning: convert logical to physical operators.
    (3) physical optimization: optimize physical operators.
    """
    # Record usage of logical operators.
    record_operators_usage(logical_plan.dag)

    logical_plan = LogicalOptimizer().optimize(logical_plan)
    physical_plan = Planner().plan(logical_plan)
    return PhysicalOptimizer().optimize(physical_plan)
