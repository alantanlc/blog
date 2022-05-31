
# Implementing A Workflow Framework

## Overview

1. Introduction
1. Use Cases
1. The Framework

## Introduction

TODO

## Use Cases

1. Payment processors
1. Job application processors

## The Framework

We can design a framework using `Flows`, `Stages`, and `Tasks`.

1. A __Flow__ executes a list of __Stages__ in sequence
1. A __Stage__ executes a list of __Tasks__ in sequence
1. A __Task__ contains the actual implementation

### Flow

Attributes:

1. Flow Id
1. Default Flow Id
1. Description

Consider `Flow Id` as a product name derived from unique combination of product attributes.

For example...

### Stage

Attributes:

1. Stage Id
1. Stage Name
1. Stage Description
1. Stage Order
1. Flow Id

### Task

Attributes:

1. Task Id
1. Task Name
1. Task Description
1. Task Order
1. Stage Id
