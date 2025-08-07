import pymc as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arviz as az
import pytensor.tensor as pt  # ✅ pytensor instead of aesara


def compute_log_returns(df):
    df = df.copy()
    df['LogReturn'] = np.log(df['Price']).diff()
    return df.dropna()


def run_bayesian_change_point_model(returns):
    import pymc as pm
    import numpy as np

    n = len(returns)
    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
        mu1 = pm.Normal('mu1', mu=0, sigma=1)
        mu2 = pm.Normal('mu2', mu=0, sigma=1)
        sigma1 = pm.HalfNormal('sigma1', sigma=1)
        sigma2 = pm.HalfNormal('sigma2', sigma=1)

        idx = np.arange(n)
        mu = pm.math.switch(idx < tau, mu1, mu2)
        sigma = pm.math.switch(idx < tau, sigma1, sigma2)

        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=returns)

        trace = pm.sample(1000, tune=1000, cores=1, random_seed=42, progressbar=False)

    return model, trace

def plot_change_point(trace, df):
    tau_samples = trace.posterior['tau'].values.flatten()
    most_probable_tau = int(np.median(tau_samples))
    change_date = df['Date'].iloc[most_probable_tau]

    print(f"Most probable change point (τ): index {most_probable_tau} → Date: {change_date.date()}")

    az.plot_trace(trace, var_names=["tau", "mu_1", "mu_2"])
    plt.tight_layout()
    plt.show()

    return change_date
