set.seed(2)
x <- 1:100

y <- 20 + 3 * x
e <- rnorm(100, 0, 60)
y <- 20 + 3 * x + e

plot(x,y)
yx.lm <- lm(y ~ x)
lines(x, predict(yx.lm), col="red")

xy.lm <- lm(x ~ y)
lines(predict(xy.lm), y, col="blue")
#normalize means and cbind together
xyNorm <- cbind(x=x-mean(x), y=y-mean(y))
plot(xyNorm)

#covariance
xyCov <- cov(xyNorm)
eigenValues <- eigen(xyCov)$values
eigenVectors <- eigen(xyCov)$vectors

plot(xyNorm, ylim=c(-200,200), xlim=c(-200,200))
lines(xyNorm[x], eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[x])
lines(xyNorm[x], eigenVectors[2,2]/eigenVectors[1,2] * xyNorm[x])

# the largest eigenValue is the first one
# so that's our principal component.
# but the principal component is in normalized terms (mean=0)
# and we want it back in real terms like our starting data
# so let's denormalize it
plot(x,y)
lines(x, (eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[x]) + mean(y))
# that looks right. line through the middle as expected

# what if we bring back our other two regressions?
lines(x, predict(yx.lm), col="red")
lines(predict(xy.lm), y, col="blue")


--------------------
df2 <- df[,2:3]
df2 <- df2[order(df2$completion_male),] 
x =df2[,1]
y =df2[,2]


plot(x,y)
yx.lm <- lm(y ~ x)
lines(x, predict(yx.lm), col="red")


xyNorm <- cbind(x=x-mean(x), y=y-mean(y))
#xyNorm <- cbind(x=(x-mean(x))/sd(x), y=(y-mean(y))/sd(y))
plot(xyNorm)

xyCov <- cov(xyNorm)
eigenValues <- eigen(xyCov)$values
eigenVectors <- eigen(xyCov)$vectors

plot(xyNorm)#, ylim=c(-60,60), xlim=c(-60,60))

lines(xyNorm[,1], eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[,1])
lines(xyNorm[,2], eigenVectors[2,2]/eigenVectors[1,2] * xyNorm[,2])


plot(x,y)
lines(x, (eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[,1]) + mean(y))



# what if we bring back our other two regressions?
lines(x, predict(yx.lm), col="red")



df


df2 <- read.csv ("cleaned.csv")#
df2 <- df2[,c("income_per_person", "life_expectancy")]
df2 <- df2[order(df2$income_per_person),] 
x =df2[,1]
y =df2[,2]


plot (x,y)
fit_x<- lm(y ~ x)
lines(x, predict(fit_x), col="red")


xyNorm <- cbind(x=df2[,1]-mean(df2[,1]), y=df2[,2]-mean(df2[,2]))
plot(xyNorm)


pca<-prcomp(xyNorm,center = FALSE,scale = FALSE) #
summary(pca)
pca[2]

lines(xyNorm[,1], pca[2]$rotation[2,1]/pca[2]$rotation[1,1]  * xyNorm[,1])
lines(xyNorm[,2], pca[2]$rotation[2,2]/pca[2]$rotation[1,2] * xyNorm[,2])



plot(x,y)
lines(x, (eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[,1]) + mean(y))



# what if we bring back our other two regressions?
lines(x, predict(fit_x), col="red")
