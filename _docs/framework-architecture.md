# Architecture

> Version: 0.1
>
> Phase: 0 – Product, UX & UI Domain Integration

---

# Vision

The Specification Orchestration Framework (SOF) extends Specification Driven Development (SDD) into a domain-oriented orchestration framework.

Instead of producing a single software specification, SOF orchestrates a sequence of domain specifications that collectively become the project's single source of truth.

Each domain contributes specialized knowledge while maintaining traceability to upstream specifications.

The framework is designed to support AI-assisted development, structured specifications, and external tool synchronization.

---

# Core Principles

## Constitution First

Every project begins with a constitution.

The constitution defines the project's immutable principles.

Every domain must comply with the constitution.

---

## Domain Driven Specifications

Every discipline is represented by an independent domain.

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

Domains are isolated.

Domains never duplicate information.

Domains only extend upstream specifications.

---

## Structured Before Generated

The canonical specification is machine-readable.

YAML is the source of truth.

Markdown is a generated human-readable representation.

```
YAML
    ↓
Validation
    ↓
Markdown
    ↓
External Tools
```

---

## Traceability

Every object has a permanent identifier.

Objects remain traceable throughout the entire project lifecycle.

Example

```
Requirement
    ↓
Journey
    ↓
Screen
    ↓
Component
    ↓
API
    ↓
Infrastructure
    ↓
Test
```

---

## Extensibility

New domains can be introduced without modifying the framework core.

Every domain implements the same contract.

---

# Framework Architecture

The framework consists of four layers.

```
            User Commands
                  │
                  ▼
        Orchestration Engine
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
    Domain Plugins      Adapters
        │                   │
        └─────────┬─────────┘
                  ▼
          Canonical Specification
```

---

# Repository Structure

```
specs/

    constitution/

    product/

    ux/

    ui/

pipeline.yaml

architecture.md

```

Future domains will extend the same structure.

---

# Pipeline

The project lifecycle is defined by a configurable pipeline.

Example

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

The framework never hardcodes execution order.

The pipeline defines:

- execution sequence
- dependencies
- validation order

---

# Domain Contract

Every domain implements the same interface.

```
domain/

    domain.yaml

    spec.md

    objects/

    validation/

    artifacts/

    exports/
```

The orchestrator interacts only with this contract.

---

# Domain Manifest

Every domain contains a manifest.

Example

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

The framework loads domains dynamically.

---

# Domain Lifecycle

Every domain follows the same execution lifecycle.

```
Read Upstream

        ↓

Validate Inputs

        ↓

Generate Domain Objects

        ↓

Run Validators

        ↓

Export Specification

        ↓

Publish Outputs
```

---

# Canonical Object Model

Every object follows the same schema.

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

Example

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

---

# Orchestration Engine

The orchestrator is responsible for

- loading domains
- resolving dependencies
- executing pipeline stages
- validating specifications
- synchronizing adapters
- generating documentation

The orchestrator never contains domain-specific logic.

All domain behavior is delegated to plugins.

---

# User Interaction Model

The framework preserves the familiar Specification Driven Development workflow.

```
/init

/constitution

/spec

/plan

/tasks

/implement
```

These commands are pipeline-aware.

The current domain determines their behavior.

Example

```
Current Domain

↓

UX

↓

/spec

↓

Generate UX Specification
```

Later

```
Current Domain

↓

UI

↓

/spec

↓

Generate UI Specification
```

The user always executes the same commands.

The framework determines which domain is active.

---

# Additional Framework Commands

The framework introduces only four new commands.

## /domain

Displays or changes the active domain.

Example

```
/domain

Current Domain

UX

Completed

✓ Product

In Progress

UX

Next

UI
```

---

## /sync

Synchronizes external tools.

Example

```
/sync figma
```

```
Import Changes

↓

Validate

↓

Update YAML

↓

Regenerate Markdown
```

Adapters never become the source of truth.

---

## /validate

Runs all validators for the current domain.

Checks include

- dependency validation
- orphan objects
- broken references
- schema validation

---

## /export

Exports specifications into external formats.

Examples

- Markdown
- JSON
- HTML
- Storybook
- Figma metadata

---

# Adapter Architecture

External tools interact with the framework through adapters.

Phase 0 adapters

## Product

- Markdown
- Notion
- Confluence

## UX

- FigJam
- Miro

## UI

- Figma
- Penpot
- Storybook

Adapters synchronize external artifacts with the canonical specification.

They never become the source of truth.

---

# Phase 0 Scope

Phase 0 introduces three domains.

```
Constitution

↓

Product

↓

UX

↓

UI
```

Deliverables

- Pipeline engine
- Domain plugin system
- Canonical YAML model
- Markdown generation
- Product domain
- UX domain
- UI domain
- Adapter framework
- Validation engine

Subsequent phases will introduce

- Architecture
- Backend
- Frontend
- Infrastructure
- Security
- QA
- Planning
- Tasks
- Implementation

without requiring changes to the framework core.

---

# Long-Term Goal

The long-term objective is to create a domain-agnostic specification orchestration framework.

Every discipline contributes to a unified specification graph.

AI agents, developers, designers, architects and QA engineers collaborate on the same canonical specification while using their preferred external tools.

The framework—not the external tools—remains the project's single source of truth.



—— framework.yml ——-

version: 0.1

pipeline: pipeline.yaml

canonical_format: yaml

markdown_generation: true

plugins:

  - product

  - ux

  - ui

adapters:

  figma: enabled

  storybook: enabled

  miro: disabled

validation:

  strict: true



——- roadmap ——-

v0.1

✓ Fork Spec Kit

✓ Preserve compatibility

✓ Document architecture

--------------------------

v0.2

Pipeline Engine

framework.yaml

pipeline.yaml

--------------------------

v0.3

Product Domain

--------------------------

v0.4

UX Domain

--------------------------

v0.5

UI Domain

--------------------------

v0.6

Figma Adapter

--------------------------

v1.0

Architecture Domain

Backend Domain

QA Domain


--- additional infos --- 

New repository structure

I’d avoid modifying the existing structure until necessary. Instead, introduce new directories alongside the existing ones:


spec-kit/

docs/

framework/

    architecture.md

    framework.yaml

pipeline.yaml

domains/

    product/

    ux/

    ui/

templates/

plugins/

adapters/

tests/


Keep backward compatibility

One of the biggest advantages of starting from Spec Kit is its existing user base. I’d aim for existing users to continue using:


/constitution

/spec

/plan

/tasks

/implement


If pipeline.yaml exists, the orchestrator switches to the multi-domain workflow:


Constitution

↓

Product

↓

UX

↓

UI

↓

...

↓

Implementation
