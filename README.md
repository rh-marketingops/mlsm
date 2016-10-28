# MLSM - Multiple Lead Score Models
Red Hat's implementation of multiple data science models against input data sets.

# Introduction

Operationalizing outputs from data science efforts is a tricky art. With so much data science relying on cutting-edge techniques, it can be difficult to balance that with the need for a stable infrastructure. Running a static analysis to provide either a spreadsheet or slide deck is fairly straightforward, but also prone to human error, time constraints, and limited resources. If you're trying to make real-time decisions based on data science models, the engine for processing models has to be reliable.

Our original use case for this package was deploying lead scoring models: given information we know about one person (based on marketing data), how should they be prioritized when being passed over to sales? If we implement a model for scoring leads, and the infrastructure breaks (due to deploying a new model, uncaught exceptions, etc), there are immediate downstream impacts to other groups who depend on this information.

Challenges with other platforms:
- Limited modeling options; usually only simple "if-then" statements
- Slow processing times
- Lack of flexibility to change model types quickly
- Lack of version control

To address these challenges, we built the `mlsm` package.

## Everything is a model

# Architecture

## Data Flow

### RunModelsAll

# Setup Process

## Hosting  

## Creating and deploying models
