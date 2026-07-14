"""Dependency resolver — graph building and topological sort.

Provides build_graph() to construct a dependency graph from domain manifests
and resolve_order() to produce a deterministic execution order using Kahn's
algorithm.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core._errors import DependencyError

if TYPE_CHECKING:
    from core._manifest import DomainManifest


@dataclass
class DependencyGraph:
    """Resolved dependency graph for a set of domains.

    Attributes:
        nodes: Domain ID to DomainManifest mapping.
        edges: List of (dependent, dependency) pairs.
        order: Topologically sorted domain IDs (computed).
    """

    nodes: dict[str, DomainManifest] = field(default_factory=dict)
    edges: list[tuple[str, str]] = field(default_factory=list)
    order: list[str] = field(default_factory=list)


def build_graph(manifests: list[DomainManifest]) -> DependencyGraph:
    """Build a dependency graph from domain manifests.

    Args:
        manifests: List of DomainManifest objects.

    Returns:
        DependencyGraph with nodes and edges populated.

    Raises:
        DependencyError: If circular or missing dependencies detected.
    """
    graph = DependencyGraph()

    for m in manifests:
        graph.nodes[m.id] = m

    for m in manifests:
        for dep in m.depends_on:
            if dep == m.id:
                raise DependencyError(
                    f"Domain '{m.id}' has a self-referencing dependency"
                )
            if dep not in graph.nodes:
                raise DependencyError(
                    f"Domain '{m.id}' depends on '{dep}' which is not in the "
                    f"manifest set"
                )
            graph.edges.append((m.id, dep))

    return graph


def resolve_order(graph: DependencyGraph) -> list[str]:
    """Topologically sort domains by dependency order.

    Uses Kahn's algorithm for topological sort.

    Args:
        graph: The DependencyGraph to sort.

    Returns:
        List of domain IDs in execution order.

    Raises:
        DependencyError: If graph contains cycles.
    """
    if not graph.nodes:
        return []

    # Build adjacency list and in-degree count
    in_degree: dict[str, int] = {nid: 0 for nid in graph.nodes}
    adjacency: dict[str, list[str]] = {nid: [] for nid in graph.nodes}

    for dependent, dependency in graph.edges:
        adjacency[dependency].append(dependent)
        in_degree[dependent] = in_degree.get(dependent, 0) + 1

    # Start with nodes that have no dependencies
    queue: deque[str] = deque(
        nid for nid, deg in in_degree.items() if deg == 0
    )

    sorted_order: list[str] = []
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbor in adjacency[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(graph.nodes):
        # Find the cycle path for the error message
        remaining = set(graph.nodes.keys()) - set(sorted_order)
        raise DependencyError(
            f"Circular dependency detected involving domains: "
            f"{', '.join(sorted(remaining))}"
        )

    graph.order = sorted_order
    return sorted_order
