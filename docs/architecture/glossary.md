# Architecture Glossary (v0.1)

Canonical terms used across the v0.1 architecture and roadmap.

- Domain: A focused area of specification ownership (e.g., product, ux, ui). Each domain provides canonical objects, validators, and exports.
- Manifest (Domain Manifest): A repository-level file declaring domains, canonical object references, adapters, and validators.
- Canonical Object: A versioned object model (id, name, fields) used as the lingua franca between domains and adapters.
- Orchestrator: The runtime that discovers manifests, validates inputs, orders domains, and executes lifecycle stages.
- Pipeline: An ordered list of domain stages that the orchestrator executes.
- Adapter: A bridge between external tools (Figma, Notion) and canonical YAML; adapters declare directionality and capabilities.
- Schema: A machine-readable specification (YAML/JSON Schema) that validates manifests and canonical objects.
- Validation: The act of checking schema conformance and graph-level constraints (orphan detection, reference resolution).
