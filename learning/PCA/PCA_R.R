set.seed(2)
x <- 1:100
e <- rnorm(100, 0, 60)
y <- 20 + 3 * x + e

plot(x,y)
yx.lm <- lm(y ~ x)
lines(x, predict(yx.lm), col="red")


xy.lm <- lm(x ~ y)
lines(predict(xy.lm), y, col="blue")


xyNorm <- cbind(x=x-mean(x), y=y-mean(y))
plot(xyNorm)


xyCov <- cov(xyNorm)
eigenValues <- eigen(xyCov)$values
eigenVectors <- eigen(xyCov)$vectors


plot(xyNorm, ylim=c(-200,200), xlim=c(-200,200))
lines(xyNorm[x], eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[x])
lines(xyNorm[x], eigenVectors[2,2]/eigenVectors[1,2] * xyNorm[x])


plot(xy)
lines(x, (eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[x]) + mean(y))
# that looks right. line through the middle as expected

lines(x, predict(yx.lm), col="red")
lines(predict(xy.lm), y, col="blue")




set.seed(2)
f1 <- rnorm(100, 0, 60)

set.seed(22)
f2 <- rnorm(100, 0, 60)

df <- data.frame(f1,f2)

plot (df$f1, df$f2)


df$f1_minmax <- (df$f1 - min(df$f1))/(max(df$f1) - min(df$f1))
df$f2_minmax <- (df$f2 - min(df$f2))/(max(df$f2) - min(df$f2))
plot (df$f1_minmax, df$f2_minmax)


df$f1_norm <- (df$f1 - mean(df$f1))/(sd(df$f1))
df$f2_norm <- (df$f2 - mean(df$f2))/(sd(df$f2))
plot (df$f1_norm, df$f2_norm)



pc <- prcomp(df[,1:2],center = FALSE,scale = FALSE) 
pcMinMax <- prcomp(df[,3:4],center = FALSE,scale = FALSE) 
pcNorm <- prcomp(df[,5:6],center = FALSE,scale = FALSE) 



print(pc)
plot(pc, type='l')

?sweep
head(df[2:6])

--------------------------------
df <- read.csv ("C:/git/mytools/learning/PCA/cleaned.csv")  
prcomp(df[,2:6],center = TRUE,scale = TRUE) 


df$completion_male <- ((df$completion_male - mean(df$completion_male)) / sd(df$completion_male))
df$completion_female <- ((df$completion_female - mean(df$completion_female)) / sd(df$completion_female))
df$income_per_person <- ((df$income_per_person - mean(df$income_per_person)) / sd(df$income_per_person))
df$employment <- ((df$employment - mean(df$employment)) / sd(df$employment))
df$life_expectancy <- ((df$life_expectancy - mean(df$life_expectancy)) / sd(df$life_expectancy))
head(df)
prcomp(df[,2:6],center = FALSE,scale = FALSE) #or any other combination of center\scaling



