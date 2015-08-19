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
setwd("C:/git/mytools/learning/PCA/")    #
df <- read.csv ("cleaned.csv")#
head(df)#

?prcomp
prcomp(df[,2:6],center = TRUE,scale = TRUE) #


  df$completion_male <- ((df$completion_male - mean(df$completion_male)) / sd(df$completion_male))#
  df$completion_female <- ((df$completion_female - mean(df$completion_female)) / sd(df$completion_female))#
  df$income_per_person <- ((df$income_per_person - mean(df$income_per_person)) / sd(df$income_per_person))#
  df$employment <- ((df$employment - mean(df$employment)) / sd(df$employment))#
  df$life_expectancy <- ((df$life_expectancy - mean(df$life_expectancy)) / sd(df$life_expectancy))#
  head(df)#
  prcomp(df[,2:6],center = FALSE,scale = FALSE) #
  


pca <- prcomp(df[,2:6],center = FALSE,scale = FALSE)#

summary(pca)
prcomp(df[,2:6],center = FALSE,scale = FALSE, tol=0.5)#


#running prcomp(df[,2:6],center = TRUE,scale = TRUE) from the original data frame would produce the same result

summary(pca)
pca[1] #$sdev
pca[2] #$rotation
pca[3] #$center ?
pca[4] #$scale  ?
pca[5] # transformed data

this in the element loadings.

x  


foo<- as.data.frame(components$rotation)#
foo2<- as.data.frame(pca$x[1:5,])#

?prcomp


df[1,2:6]

components <- pca[2]
pca1<-components$rotation[,1]
pca2<-components$rotation[,2]


as.data.frame(pca$x[1:5,])


summary(pca)

components <- pca[2]

#Components are orthogonal to each other (dot product = 0)
components$rotation[,3] %*% components$rotation[,1]

#Components are normaled to have length 1.
sum(components$rotation[,1]**2)




#lloking at 1st and econd component only
pca1<-components$rotation[,4]
pca2<-components$rotation[,5]



pca1<-components$rotation[,1]
pca2<-components$rotation[,2]

plot(pca$x[,1],  pca$x[,2])
arrow_size=2
arrows(0,0,pca1[1]* arrow_size,pca2[1]* arrow_size) 
arrows(0,0,pca1[2]* arrow_size,pca2[2]* arrow_size)
arrows(0,0,pca1[3]* arrow_size,pca2[3]* arrow_size)
arrows(0,0,pca1[4]* arrow_size,pca2[4]* arrow_size)
text(pca1[4]* arrow_size,pca2[4]* arrow_size, row.names(pca$rotation)[4])
arrows(0,0,pca1[5]* arrow_size,pca2[5]* arrow_size)


foo<-pca$rotation
row.names(pca1[1])



components$rotation

xyNorm <- cbind(((df$completion_male - mean(df$completion_male)) / sd(df$completion_male)), 
                ((df$completion_female - mean(df$completion_female)) / sd(df$completion_female)),
                ((df$income_per_person - mean(df$income_per_person)) / sd(df$income_per_person)),
                ((df$employment - mean(df$employment)) / sd(df$employment)),
                ((df$life_expectancy - mean(df$life_expectancy)) / sd(df$life_expectancy))
)


xyNorm <- cbind((df$completion_male), 
                (df$completion_female),
                (df$income_per_person),
                (df$employment),
                (df$life_expectancy)
)


xyCov <- cov(xyNorm)
eigenValues <- eigen(xyCov)$values
eigenVectors <- eigen(xyCov)$vectors # contains the pca[2] object



xyNorm <- cbind(((df2$completion_male - mean(df2$completion_male)) ), 
                ((df2$completion_female - mean(df2$completion_female)) ),
                ((df2$income_per_person - mean(df2$income_per_person)) ),
                ((df2$employment - mean(df2$employment)) ),
                ((df2$life_expectancy - mean(df2$life_expectancy)) )
)




----------------------------DIF with LR
df2 <- read.csv ("cleaned.csv")#
df2 <- df2[,2:3]
df2 <- df2[order(df2$completion_male),] 
x =df2[,1]
y =df2[,2]


plot(x,y)
yx.lm <- lm(y ~ x)
lines(x, predict(yx.lm), col="red")


xyNorm <- cbind(x=x-mean(x), y=y-mean(y))
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

----------------------------
df2 <- read.csv ("cleaned.csv")#
df2 <- df2[,2:3]
df2 <- df2[order(df2$completion_male),] 
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

lines(xyNorm[,1],  pca[2]$rotation[2,1]/pca[2]$rotation[1,1]  * xyNorm[,1])
lines(xyNorm[,2], pca[2]$rotation[2,2]/pca[2]$rotation[1,2] * xyNorm[,2])



plot(x,y)
lines(x, (eigenVectors[2,1]/eigenVectors[1,1] * xyNorm[,1]) + mean(y))



# what if we bring back our other two regressions?
lines(x, predict(yx.lm), col="red")

