"""Unit tests for core._resolver module."""

from __future__ import annotations

from pathlib import Path

import pytest

from core._errors import DependencyError
from core._manifest import DomainManifest
from core._resolver import DependencyGraph, build_graph, resolve_order


def _manifest(
    id: str,
    name: str | None = None,
    depends_on: list[str] | None = None,
) -> DomainManifest:
    """Helper to create a DomainManifest quickly."""
    return DomainManifest(
        path=Path(f"/tmp/{id}.yaml"),
        id=id,
        name=name or id,
        version="1.0.0",
        depends_on=depends_on or [],
    )


class TestBuildGraph:
    """Tests for build_graph()."""

    def test_simple_graph(self) -> None:
        """build_graph creates graph with correct nodes and edges."""
        m1 = _manifest("core")
        m2 = _manifest("plugin", depends_on=["core"])
        graph = build_graph([m1, m2])
        assert "core" in graph.nodes
        assert "plugin" in graph.nodes
        assert ("plugin", "core") in graph.edges

    def test_no_dependencies(self) -> None:
        """build_graph handles manifests with no dependencies."""
        m1 = _manifest("a")
        m2 = _manifest("b")
        graph = build_graph([m1, m2])
        assert len(graph.nodes) == 2
        assert graph.edges == []

    def test_single_domain(self) -> None:
        """build_graph handles a single domain with no deps."""
        m = _manifest("standalone")
        graph = build_graph([m])
        assert len(graph.nodes) == 1
        assert graph.edges == []

    def test_missing_dependency(self) -> None:
        """build_graph raises DependencyError for missing dependency."""
        m1 = _manifest("plugin", depends_on=["nonexistent"])
        with pytest.raises(DependencyError, match="nonexistent"):
            build_graph([m1])

    def test_self_reference(self) -> None:
        """build_graph raises DependencyError for self-referencing domain."""
        m1 = _manifest("selfref", depends_on=["selfref"])
        with pytest.raises(DependencyError, match="self-referenc|selfref"):
            build_graph([m1])

    def test_empty_manifests(self) -> None:
        """build_graph handles empty manifest list."""
        graph = build_graph([])
        assert graph.nodes == {}
        assert graph.edges == []


class TestResolveOrder:
    """Tests for resolve_order()."""

    def test_topological_sort_simple(self) -> None:
        """resolve_order returns correct order for linear deps."""
        m1 = _manifest("core")
        m2 = _manifest("plugin", depends_on=["core"])
        m3 = _manifest("app", depends_on=["plugin"])
        graph = build_graph([m1, m2, m3])
        order = resolve_order(graph)
        assert order == ["core", "plugin", "app"]

    def test_topological_sort_diamond(self) -> None:
        """resolve_order handles diamond-shaped dependencies."""
        core = _manifest("core")
        left = _manifest("left", depends_on=["core"])
        right = _manifest("right", depends_on=["core"])
        app = _manifest("app", depends_on=["left", "right"])
        graph = build_graph([core, left, right, app])
        order = resolve_order(graph)
        assert order.index("core") < order.index("left")
        assert order.index("core") < order.index("right")
        assert order.index("left") < order.index("app")
        assert order.index("right") < order.index("app")

    def test_no_dependencies_order(self) -> None:
        """resolve_order returns all domains for graph with no edges."""
        m1 = _manifest("a")
        m2 = _manifest("b")
        graph = build_graph([m1, m2])
        order = resolve_order(graph)
        assert set(order) == {"a", "b"}

    def test_circular_dependency(self) -> None:
        """resolve_order raises DependencyError for circular deps."""
        m1 = _manifest("a", depends_on=["b"])
        m2 = _manifest("b", depends_on=["a"])
        graph = build_graph([m1, m2])
        with pytest.raises(DependencyError, match="(?i)circular|cycle"):
            resolve_order(graph)

    def test_self_reference_in_graph(self) -> None:
        """build_graph raises DependencyError for self-referencing node."""
        m1 = _manifest("a", depends_on=["a"])
        with pytest.raises(DependencyError, match="self-referenc"):
            build_graph([m1])

    def test_empty_graph(self) -> None:
        """resolve_order returns empty list for empty graph."""
        graph = DependencyGraph()
        assert resolve_order(graph) == []
