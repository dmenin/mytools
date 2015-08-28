install.packages("fpp")
library(fpp)
#2
----------------------------------------------------------------------------------------
plot(melsyd[,"Economy.Class"], 
     main="Economy class passengers: Melbourne-Sydney",
     xlab="Year",ylab="Thousands")
----------------------------------------------------------------------------------------
plot(a10, ylab="$ million", xlab="Year", main="Antidiabetic drug sales")
----------------------------------------------------------------------------------------
seasonplot(a10,ylab="$ million", xlab="Year", 
           main="Seasonal plot: antidiabetic drug sales",
           year.labels=TRUE, year.labels.left=TRUE, col=1:20, pch=19)
----------------------------------------------------------------------------------------
monthplot(a10,ylab="$ million",xlab="Month",xaxt="n",
            main="Seasonal deviation plot: antidiabetic drug sales")
axis(1,at=1:12,labels=month.abb,cex=0.8)
----------------------------------------------------------------------------------------
plot(jitter(fuel[,5]), jitter(fuel[,8]), xlab="City mpg", ylab="Carbon footprint")
----------------------------------------------------------------------------------------
pairs(fuel[,-c(1:2,4,7)], pch=19)  
----------------------------------------------------------------------------------------
#AUTO CORRELATION ?????
beer2 <- window(ausbeer, start=1992, end=2006-.1)
lag.plot(beer2, lags=9, do.lines=FALSE)
Acf(beer2)
----------------------------------------------------------------------------------------
#White noise
#Time series that show no autocorrelation are called "white noise". 
set.seed(30)
x <- ts(rnorm(10))
plot(x, main="White noise")
Acf(x)
----------------------------------------------------------------------------------------
#2.3 Some simple forecasting methods
#Average method:
  #The forecasts of all future values are equal to the mean of the historical data.
  nile.fcast <- meanf(Nile, h=10)
  plot(nile.fcast)

#Naïve method:
  #This method is only appropriate for time series data. All forecasts are simply set to be the value of the last observation.
  plot(naive(gold,h=50),include=200)
  plot(rwf(gold[1:60],h=50))

#Seasonal naïve method
  #For highly seasonal data. Each forecast is equal to the last observed value from the same season of the year (e.g., the same month of the previous year).
  plot(snaive(wineind))

#Drift method
  #Allow the forecasts to increase or decrease over time, where the amount of change
  #over time (called the drift) is set to be the average change seen in the historical data. 
  #Equivalent to drawing a line between the first and last observation, and extrapolating it into the future.

#Examples
beer2 <- window(ausbeer,start=1992,end=2006-.1)
beerfit1 <- meanf(beer2, h=11)
beerfit2 <- naive(beer2, h=11)
beerfit3 <- snaive(beer2, h=11)

plot(beerfit1, plot.conf=FALSE, 
     main="Forecasts for quarterly beer production")
lines(beerfit2$mean,col=2)
lines(beerfit3$mean,col=3)
legend("topright",lty=1,col=c(4,2,3),
       legend=c("Mean method","Naive method","Seasonal naive method"))



dj2 <- window(dj,end=250)
plot(dj2,main="Dow Jones Index (daily ending 15 Jul 94)",
     ylab="",xlab="Day",xlim=c(2,290))
lines(meanf(dj2,h=42)$mean,col=4)
lines(rwf(dj2,h=42)$mean,col=2)
lines(rwf(dj2,drift=TRUE,h=42)$mean,col=3)
legend("topleft",lty=1,col=c(4,2,3),
       legend=c("Mean method","Naive method","Drift method"))
----------------------------------------------------------------------------------------
#2.4 Transformations and adjustments  
plot(log(elec), ylab="Transformed electricity demand",
    xlab="Year", main="Transformed monthly electricity demand")
    title(main="Log",line=-1)

lambda <- BoxCox.lambda(elec) # = 0.27
plot(BoxCox(elec,lambda))

monthdays <- rep(c(31,28,31,30,31,30,31,31,30,31,30,31),14)
monthdays[26 + (4*12)*(0:2)] <- 29
par(mfrow=c(2,1))
plot(milk, main="Monthly milk production per cow",
     ylab="Pounds",xlab="Years")
plot(milk/monthdays, main="Average milk production per cow per day", 
     ylab="Pounds", xlab="Years")

----------------------------------------------------------------------------------------
#2.5 Evaluating forecast accuracy
beer2 <- window(ausbeer,start=1992,end=2006-.1)

beerfit1 <- meanf(beer2,h=11)
beerfit2 <- rwf(beer2,h=11)
beerfit3 <- snaive(beer2,h=11)

plot(beerfit1, plot.conf=FALSE,
     main="Forecasts for quarterly beer production")
lines(beerfit2$mean,col=2)
lines(beerfit3$mean,col=3)
lines(ausbeer)
legend("topright", lty=1, col=c(4,2,3),
       legend=c("Mean method","Naive method","Seasonal naive method"))

beer3 <- window(ausbeer, start=2006)
accuracy(beerfit1, beer3)
accuracy(beerfit2, beer3)
accuracy(beerfit3, beer3)
-----------------------------------
  dj2 <- window(dj, end=250)
plot(dj2, main="Dow Jones Index (daily ending 15 Jul 94)",
     ylab="", xlab="Day", xlim=c(2,290))
lines(meanf(dj2,h=42)$mean, col=4)
lines(rwf(dj2,h=42)$mean, col=2)
lines(rwf(dj2,drift=TRUE,h=42)$mean, col=3)
legend("topleft", lty=1, col=c(4,2,3),
       legend=c("Mean method","Naive method","Drift method"))
lines(dj)  

dj3 <- window(dj, start=251)
accuracy(meanf(dj2,h=42), dj3)
accuracy(rwf(dj2,h=42), dj3)
accuracy(rwf(dj2,drift=TRUE,h=42), dj3)

----------------------------------------------------------------------------------------
#2.6 Residual diagnostics
dj2 <- window(dj, end=250)
plot(dj2, main="Dow Jones Index (daily ending 15 Jul 94)", ylab="", xlab="Day")
res <- residuals(naive(dj2))
plot(res, main="Residuals from naive method",  ylab="", xlab="Day")
Acf(res, main="ACF of residuals")
hist(res, nclass="FD", main="Histogram of residuals")


# lag=h and fitdf=K
Box.test(res, lag=10, fitdf=0)
Box.test(res,lag=10, fitdf=0, type="Lj")



#----------------------------------------------------------------------------------------
#2.7 Prediction intervals
  #Consider a naïve forecast for the Dow-Jones Index. The last value of the observed series is 3830, 
  #so the forecast of the next value of the DJI is 3830. The standard deviation of the residuals 
  #from the naïve method is 21.99. Hence, a 95% prediction intervalfor the next value of the DJI is:
  3830±1.96(21.99)=[3787,3873]

#Similarly, an 80% prediction interval is given by
  3830±1.28(21.99)=[3802,3858].
----------------------------------------------------------------------------------------