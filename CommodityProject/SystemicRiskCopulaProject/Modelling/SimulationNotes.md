How the Co-Simulation Actually Unfolds (Step-by-Step)

Suppose you are simulating tomorrow ($t = T+1$) for $C_1$ (Brent) and $C_2$ (WTI).

Step A: Determine the deterministic environment

    Before tomorrow's trading bell rings, you already know today's closing prices.
        * You calculate $\mu_{1, T+1}$ and $\mu_{2, T+1}$ using their respective ARMA equations.
        * You calculate $\sigma_{1, T+1}$ and $\sigma_{2, T+1}$ using their respective GARCH equations.
                (Notice: these numbers are fixed. No random number generator is called here.)
Step B: Call the Copula for the Joint Shock
    To see what unexpected shock hits the market tomorrow, you sample from the fitted multivariate Copula:
        * The Copula draws correlated uniform numbers:$$(u_1, u_2)  ~ \text{Copula}$$
        
            (If Brent plunges in the copula draw, $u_1 = 0.01$; because of tail dependence, $u_2$ is automatically drawn as $0.012$.)
        * Invert each $u_i$ back through its individual Skewed-$t$ CDF (the inverse Probability Integral Transform, $F_i^{-1}$):
        
            $$\eta_1 = F_{\text{Skew-}t, 1}^{-1}(u_1) = -3.8\sigma$$
            $$\eta_2 = F_{\text{Skew-}t, 2}^{-1}(u_2) = -3.5\sigma$$
                                (-3.8 = F_-1(0.01) and -3.5 = F-1) Those numbers (-3.8 and -3.5) were hypothetical examples I used to illustrate what a "joint crash" looks like mathematically.
                We are transforming CDF(0,1) back to real world shock here. 
                The shocks $(\eta_1, \eta_2)$ now contain all the non-linear tail dependence, joint crash correlation, and cross-asset linkage.

Step C: Synthesize Tomorrow's Return
    Now, scale and shift the shocks using the pre-computed deterministic volatility and mean:
    
    $$R_{1, T+1} = \mu_{1, T+1} + \sigma_{1, T+1} \cdot \eta_1$$
    $$R_{2, T+1} = \mu_{2, T+1} + \sigma_{2, T+1} \cdot \eta_2$$
    
    Because $\eta_1$ and $\eta_2$ plummeted together in the simulation, $R_1$ and $R_2$ plunge together.
    
What Happens at Step $t = T+2$ (Dynamic Feedback)?

    This is where the magic happens over multi-day simulations.
    When you advance to the next day ($T+2$):
        
        $C_1$'s new conditional volatility $\sigma_{1, T+2}$ is calculated using $\epsilon_{1, T+1} = \sigma_{1, T+1} \cdot \eta_1$.
        
        $C_2$'s new conditional volatility $\sigma_{2, T+2}$ is calculated using $\epsilon_{2, T+1} = \sigma_{2, T+1} \cdot \eta_2$.
        
    Because both assets took a joint crash in step $T+1$ through the copula shocks ($\eta_1, \eta_2$), both assets' GARCH models automatically spike their volatility forecasts simultaneously for step $T+2$.