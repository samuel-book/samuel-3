# Planned experiments

## Descriptive statistics

## Treatment effects

[ ] Run thrombolysis effect on late arrivals or unkown stroke onset time; use perfusion imaging
[ ] Run thrombectomy effect on late arrivals or unkown stroke onset time; use perfusion imaging
[ ] Single causal forest
[ ] Double ML causal forest## Bayesian Additive Regression Trees (BART)
For implementing BART in Python, there are two primary packages:

## Causal AI

[ ] Reduce simulated data set size and perform replicate runs (diff random seed)
[ ] Compare Causal Forest to XGBoost + SHAP
[ ] Add nuisance models to Causal Forest

## Notes on Bayesian methods

### Bayesian Additive Regression Trees (BART)

- **PyMC-BART**: This is a powerful extension to the PyMC probabilistic programming framework, allowing you to use BART as a random variable within larger probabilistic models. It offers a high level of flexibility for building complex models, performing variable selection, and generating partial dependence plots. [subscription.packtpub](https://subscription.packtpub.com/book/data/9781805127161/9/ch09lvl1sec01/92-bart-models)

- **BartPy**: This is a pure Python implementation of the BART model. It is designed to be highly extensible and features a scikit-learn compatible API (e.g., `model.fit(X, y)` and `model.predict(X_test)`), making it easy to plug into existing cross-validation and grid search workflows. It also includes convenience features like `ResidualBART` for predicting the residuals of a base model like a linear regression. [github](https://github.com/JakeColtman/bartpy)

### Bayesian Causal Forests (BCF)
For BCF—a model that builds upon BART to specifically estimate conditional average treatment effects (CATE) by modeling the response and treatment effect separately —the primary Python option is **StochTree**. [github](https://github.com/jaredsmurray/bcf)

- **StochTree**: This is a modern, actively maintained C++ library with full Python bindings for Bayesian tree ensemble models, including BART and BCF. It supports both a scikit-learn style API for easy implementation and a low-level interface for custom sampling. Crucially, StochTree natively handles BCF models for causal effect estimation  and can even serialize models to JSON, which is useful for saving and loading models across your remote SSH environments. [stochtree](https://stochtree.ai/python_docs/demo/index.html)

Another historical option is the Python implementation of **Accelerated Bayesian Causal Forests (XBCF)**, but its developers have formally migrated the project and its active maintenance over to the StochTree repository. [johaupt.github](https://johaupt.github.io/blog/xbcf.html)

If you encounter limitations with these native Python implementations for highly specialized tasks, you can also leverage your existing proficiency with `rpy2` to call the robust R package `bcf` directly within your Python scripts.
