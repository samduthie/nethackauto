"""Checks docs/tech_tree.json, so that edits keep the plan valid."""

import json
from graphlib import TopologicalSorter
from pathlib import Path
from typing import Any

import pytest

TECH_TREE_PATH = Path(__file__).parents[2] / "docs" / "tech_tree.json"
STATUSES = {"done", "doing", "todo"}


@pytest.fixture(scope="module")
def tree() -> dict[str, Any]:
    return dict(json.loads(TECH_TREE_PATH.read_text()))


@pytest.fixture(scope="module")
def nodes(tree: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {node["id"]: node for node in tree["nodes"]}


def test_node_ids_are_unique(tree: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    assert len(nodes) == len(tree["nodes"])


def test_each_need_names_a_node(nodes: dict[str, dict[str, Any]]) -> None:
    assert {need for node in nodes.values() for need in node["needs"]} <= nodes.keys()


def test_each_lane_is_known(tree: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    assert {node["lane"] for node in nodes.values()} <= {lane["id"] for lane in tree["lanes"]}


def test_each_phase_is_known(tree: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    assert {node["phase"] for node in nodes.values()} <= {phase["id"] for phase in tree["phases"]}


def test_each_status_is_known(nodes: dict[str, dict[str, Any]]) -> None:
    assert {node["status"] for node in nodes.values()} <= STATUSES


def test_no_need_is_in_a_later_phase(nodes: dict[str, dict[str, Any]]) -> None:
    late = [
        (n["id"], need)
        for n in nodes.values()
        for need in n["needs"]
        if nodes[need]["phase"] > n["phase"]
    ]
    assert late == []


def test_a_built_node_needs_only_built_nodes(nodes: dict[str, dict[str, Any]]) -> None:
    built = {node_id for node_id, node in nodes.items() if node["status"] == "done"}
    assert {need for node_id in built for need in nodes[node_id]["needs"]} <= built


def test_each_goal_is_a_milestone(tree: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    assert {nodes[goal].get("kind") for goal in tree["goals"]} == {"milestone"}


def test_the_tree_has_no_cycles(nodes: dict[str, dict[str, Any]]) -> None:
    order = list(
        TopologicalSorter(
            {node_id: node["needs"] for node_id, node in nodes.items()}
        ).static_order()
    )
    assert len(order) == len(nodes)
