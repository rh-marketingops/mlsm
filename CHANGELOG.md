## TBD v0.0.4
- Added docs
- Improved Model.execute validation
  - Returns errors during `self.fcn()` in a results field `results/model/version/_error`
  - Also returns errors for input field validation in the same way
- Added initial model testing framework

## 2016-10-24 v0.0.3
- To the results stored in MongoDB, add `_timestamp` and `_current` fields to allow cleanup of old results and easy querying of current results
- To the results stored in MongoDB, under `model/version`, add `_status` to indicate whether or not, at runtime, the results were `active` or `draft`
- Major: Changed input data format for `RunModels`, `RunSummaryModels`, and `RunModelsAll`:
  - `data` argument of `record/records` now expects structure of `data/model.name/model.version`
  - Allows for querying different data sources/logic between different models

## 2016-10-19 v0.0.2
- Add optional functionality to store only results in a MongoDB

## 2016-10-14 v0.0.1
- Initial release
