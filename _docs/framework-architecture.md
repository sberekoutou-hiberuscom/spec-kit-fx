# Architecture

> Version: 0.1
>
> Phase: 0 - Product, UX, and UI Domain Integration

## Framework Overview

The Specification Orchestration Framework (SOF) extends Specification Driven
Development (SDD) into a domain-oriented orchestration framework.

Instead of producing one static specification, SOF orchestrates a sequence of
related domain specifications that together form the canonical project model.

The framework is designed to support AI-assisted delivery, structured
specifications, and synchronization with external tools.

## Core Principles

### Constitution First

Every project begins with a constitution. The constitution defines immutable
project principles, and all domains must comply with it.

### Domain-Driven Specifications

Each discipline is represented by an independent domain.

Examples:

- Product
- UX
- UI
- Architecture
- Backend
- Frontend
- Infrastructure
- Security
- QA

Domains are isolated, avoid duplication, and extend upstream specifications.

### Structured Before Generated

Canonical specification data is machine-readable (YAML). Human-readable
Markdown is derived from canonical data.

```text
YAML
  -> Validation
  -> Markdown
  -> External Tools
```

### Traceability

Every object has a permanent identifier and remains traceable across the full
lifecycle.

```text
Requirement
  -> Journey
  -> Screen
  -> Component
  -> API
  -> Infrastructure
  -> Test
```

### Extensibility

New domains can be added without modifying framework core behavior.

## Architecture Layers

The framework has four primary layers:

```text
User Commands
  -> Orchestration Engine
  -> Domain Plugins and Adapters
  -> Canonical Specification
```

## Repository Structure

```text
specs/
  constitution/
  product/
  ux/
  ui/

pipeline.yaml
architecture.md
```

Future domains follow the same structure and contract.

## Pipeline

The project lifecycle is declared by configuration, not hardcoded behavior.

```yaml
pipeline:
  - constitution
  - product
  - ux
  - ui
  - architecture
  - backend
  - frontend
  - infrastructure
  - security
  - qa
  - planning
  - tasks
  - implementation
```

Pipeline configuration defines:

- execution sequence
- dependencies
- validation order

## Domain Contract

Each domain should conform to the same interface.

```text
domain/
  domain.yaml
  spec.md
  objects/
  validation/
  artifacts/
  exports/
```

## Domain Manifest

Every domain includes a manifest.

```yaml
name: ui
version: 1.0
depends_on:
  - ux
entrypoint: spec
exports:
  - screens
  - components
  - interactions
validators:
  - orphan_screens
  - missing_components
adapters:
  - figma
  - penpot
```

## Domain Lifecycle

```text
Read Upstream
  -> Validate Inputs
  -> Generate Domain Objects
  -> Run Validators
  -> Export Specification
  -> Publish Outputs
```

## Canonical Object Model

```yaml
id:
type:
name:
description:
status:
source:
references:
metadata:
```

Example:

```yaml
id: UI-SCREEN-LOGIN
type: screen
name: Login Screen
description: User authentication interface
references:
  - UX-FLOW-AUTH
metadata:
  owner: ui
  version: 1
```

## Command Model

The framework preserves the familiar command vocabulary:

```text
/init
/constitution
/spec
/plan
/tasks
/implement
```

Additional commands:

- /domain: display or change active domain
- /sync: synchronize external tools
- /validate: run domain validators
- /export: generate external output formats

## Adapter Direction

Adapters synchronize external artifacts with canonical YAML but do not become
source of truth.

## Phase 0 Scope

Phase 0 includes three domains:

```text
Constitution -> Product -> UX -> UI
```

Phase 0 deliverables:

- pipeline engine
- domain plugin system
- canonical YAML model
- markdown generation
- product domain
- ux domain
- ui domain
- adapter framework
- validation engine

## Long-Term Goal

The long-term objective is a domain-agnostic specification orchestration
framework where contributors collaborate on one canonical graph while using
preferred external tools.
