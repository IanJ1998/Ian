GJR-GARCH

Its a GARCh model which can supply asymmteric/leveraged effect on vols.
Core concept ois that in a normal GARCH +/- residual results in the same impact since residuals are squared * epsilon and added  with squared standard deviation * thetaCoefficient + constant(Which is the vols component)
GJR fixes this by adding an indicator function.

Is GJR CARSH only valid for asymmteric commodities?
No, its valiud for all commodities, bnecause GJR term goes to 0 when its not asymmetric. 

How to determine whether a commodity needs GJR?
> Method 1: Model selection using BIC and AIC
            i. Fix the data into GARCH (1,1) model and measure BIC_i
            ii. Fix data into GJR GARCH (1,1,1) and measure BIC_ii
            iii. If BIC_i <> BIC_ii, select GARCH and choose GJR GARCH otherwise --> Smaller the better
> Method 2: 