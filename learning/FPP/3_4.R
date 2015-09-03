#Judgmental forecasting is usually the only available method for new product forecasting as historical data are unavailable
#(Delphi and forecasting by analogy) 
#Scenario forecasting
library(fpp)
plot(jitter(Carbon) ~ jitter(City),xlab="City (mpg)",   ylab="Carbon footprint (tons per year)",data=fuel)
fit <- lm(Carbon ~ City, data=fuel)
abline(fit)

#plot residuals
res <- residuals(fit)
plot(jitter(res)~jitter(City), ylab="Residuals", xlab="City", data=fuel)
abline(0,0)


#4.4 Evaluating the regression model
#the value of R2 is also equal to the square of the correlation between y and x
fit <- lm(mpg ~ cyl, data=mtcars)
summary(fit)
cor(mtcars$cyl, mtcars$mpg)**2


#Standard error of the regression
sum(fit$residuals**2)/(nrow(mtcars)-2)


#4.5 Forecasting with regression
#tentar o exemplocalculo do forecasting with interval

fitted(fit)[1]
fcast <- forecast(fit, newdata=data.frame(City=30))
plot(fcast, xlab="City (mpg)", ylab="Carbon footprint (tons per year)")
# The displayed graph uses jittering, while the code above does not.




#4.6 Statistical inference

# If x and y are unrelated, then the slope parameter ??1=0. So we can construct a test to see if it is plausible that ??1=0 given the observed data.
#there is no relationship between x and y. This is called the "null hypothesis" and is stated as
#H0:??1=0.


foo<- mtcars
summary( lm(mpg ~ ., data=foo))

foo$extravariable <- foo$mpg/2
summary( lm(mpg ~ ., data=foo))
#rever of inal sobre Confidence intervals


