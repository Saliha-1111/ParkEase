# ParkEase Automated Tests

A small in-memory model of the ParkEase exit payment (rules R1-R8),
tested with Gherkin scenarios and behave.

## Setup (Windows)

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

## Run all tests (one command)

    behave

## Run by tag

    behave --tags=@smoke
    behave --tags=@boundary
    behave --tags=@negative

## Files

- parkease.py - the ParkEase class
- features/*.feature - the scenarios
- features/steps/steps.py - step definitions
- features/environment.py - creates a fresh ParkEase before each scenario
