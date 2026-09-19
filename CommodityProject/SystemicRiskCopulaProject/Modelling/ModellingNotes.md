Modelling:

> The objective is to model the vols in GJR-GARCH model inorder to capture assymmetric returns of  commodities 

> GJR-GARCH (p,o,q) 
    where p is the ARCH parameter -- Or the squared difference between actual return and return given past information
          o is the indicator for assymetric return
          q is the GARCH volatility component--Or how past vol persist onto current observation

> How to find parameters of GJR-GARCH?

Finding the optimal lag orders for a GJR-GARCH model does not rely on looking at a visual plot (like ACF or PACF) in the way a standard ARIMA model does. Instead, it is found through a structured statistical workflow: 

Step 1: 

Filter the Mean Equation Before modeling volatility, you must strip away any trends or patterns in the asset's returns. Fit a mean model—typically an ARMA(P, Q) or just a constant—to your return series. Extract the residuals (\[\varepsilon _{t}\]), which represent the unexplained "shocks" or white noise. 

Step 2: 

Test for ARCH & Asymmetry Effects Ensure a GJR-GARCH model is actually necessary: 

             (i)GrantEngle's ARCH-LM Test: Run this test on your residuals to verify that variance changes over time (heteroskedasticity). If significant, a GARCH framework is valid. 

            (ii)Sign Bias Test: Run a sign bias test to check if negative and positive innovations impact the residuals differently. If they do, it justifies using an asymmetric GJR model over a symmetric standard GARCH. 
            
Step 3: 

Establish the Baseline GJR-GARCH(1, 1, 1) In financial econometrics, GJR-GARCH(1, 1, 1) is the gold standard baseline. Because financial markets absorb information rapidly, higher lags rarely provide better out-of-sample forecasts and heavily risk overfitting the model. Start by estimating a \((1, 1, 1)\) model using maximum likelihood estimation (MLE)

Step 4: 

Iterative Optimization via Information Criteria (AIC / BIC) If you want to test whether higher order lags—such as \((2,1,1)\) or \((1,1,2)\)—yield better performance, execute a grid search. Estimate multiple combinations of \(p, o,\) and \[q\] (typically keeping lags \[\le 2\]) and record their information criteria scores: 
        AIC (Akaike Information Criterion): Focuses on maximizing explanatory power.
        BIC (Bayesian Information Criterion): Places a harsher penalty on adding parameters, making it excellent for avoiding overfitting.

Step 5: 

Residual Diagnostics (The Final Check) Once you find the lowest-scoring model, extract its standardized residuals (\(z_t = \varepsilon_t / \sigma_t\)). Run a Ljung-Box test or plot the ACF of these standardized residuals and their squares. If the model correctly captured the dynamics, there should be zero remaining autocorrelation left in the errors