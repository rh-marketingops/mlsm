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

Using a Python framework offers the following solutions:
- _Limited modeling options; usually only simple "if-then" statements_
  - Python offers direct access to data science standards, such as linear regression, random forests, and machine learning
- _Slow processing times_
  - By running Python on a server, we can add more resources to speed up processing as needed
- _Lack of flexibility to quickly deploy new models_
  - With a standardized architecture designed for multiple concurrent models, deploying new models is easy
- _Lack of version control_
  - By deploying with a Git-based system, can easily view changes and roll back to older code; architecture for multiple models allows easier comparison of outputs against live data

# Architecture

## `Model` class

`Model` is a high-level wrapper for functions that run models. This not only puts functions in a framework to be more consistently applied, it also facilitates easier storage of results by model name/version, better validation of input data, and simplifying any script which actually applies models.

The inputs for executing a function, `data` and `results`, are expected to a single record (the function `RunModelsAll` is used to apply across multiple records).

`Model` also collects a `fields` dict, used to validate input values before execution (future enhancements will include extreme unit/case/exception handling).

## `SummaryModel` class

`SummaryModel` is an extension of `Model` - it expects output of previously run `Model`s to be passed (via `results`) for the purpose of running a second-level computation. For example, if three `Model`s are run, a `SummaryModel` could then be used to determine which score 'wins' (or, which score is passed back to business users).

When passed to `RunModelsAll`, every `SummaryModel` will be run _after_ all `Model`s have run.

## Data Flow

### Pre-run

- An ETL script prepares data for processing (not part of the `mlsm` package)
  - Each record is a dict
  - Each record has a unique identifier (which can later be passed as a parameter to `RunModelsAll`)
  - Data for each record is structured in sub-dictionaries
    - `data` top-level dict
    - `Model.name` sub-level
    - `Model.version` sub-level - data values contained here
  - When running a `Model`, the data passed to the underlying function will be taken from the path `data[Model.name][Model.version]`

### `RunModelsAll`

- For each record passed (`records`):
  - For each `Model` passed (`models`):
    - Execute model
  - For each `SummaryModel` passed (`summaryModels`):
    - Execute summary model
  - If DB parameters passed:
    - Store output `results` object in MongoDB

# Setup Process

## Hosting  

We use Red Hat's Openshift (Python 3.3 cartridge), with an additional install script to run Anaconda for more advanced models

## Creating and deploying models

We follow this procedure for creating/deploying models (also workflow for passing models from data scientists to engineers for deployment):

### Data Scientists
1. Create a new local git repo (and a remote for backup)
2. Use git-flow for develop/release/feature management
3. When a new model is ready to be deployed, push to remote and inform engineering team with commit ID
  - If testing a model from the `develop` branch, then must set `Model.status='draft'`

### Engineers
1. Pull model repo to local
2. Add to deployment code repo
3. Import model to script which runs `RunModelsAll`
4. Add any additional requirements to existing ETL scripts

### Future
Implementation standard leveraging Jenkins, so Data Scientists can have their latest models pulled directly in from remote
