#setwd("C:/git/mytools/learning/PCA/")  
df2 <- read.csv ("cleaned.csv")
df2 <- df2[,c("income_per_person", "life_expectancy")]
#df2 <- df2[order(df2$income_per_person),] 

#df2 <- df2[,c("completion_male", "employment")]
#df2 <- df2[order(df2$completion_male),] 
x =df2[,1]
y =df2[,2]


plot (x,y)
fit_x<- lm(y ~ x)
lines(x, predict(fit_x), col="red")


xyNormSD <- cbind(x= (x-mean(x))/sd(x), y= (y-mean(y))/sd(y) ) #center and scale
xyNorm <- cbind(x= (x-mean(x)), y= (y-mean(y)) ) #center and scale



  #pca<-prcomp(xyNormSD,center = FALSE,scale = FALSE) #
prcomp(xyNormSD,center = FALSE,scale = FALSE) 
prcomp(xyNormSD,center =FALSE,scale =TRUE) 

prcomp(df2,center =TRUE,scale =TRUE) 
  #prcomp(xyNormSD,center = TRUE,scale = TRUE) #
  #summary(pca)
  #pca[2]
  #pca[5]
#         components <- pca[2]
#         pca1<-components$rotation[,1]
#         pca2<-components$rotation[,2]
#         arrow_size = 2
#       
#         pca$x[,1]
#         plot(pca$x[,1], pca$x[,2])
#         arrows(0,0,pca1[1]* arrow_size,pca2[1]* arrow_size) 
#         arrows(0,0,pca2[1]* arrow_size,pca2[2]* arrow_size) 
  
  #lines(xyNormSD[,1], pca[2]$rotation[2,1]/pca[2]$rotation[1,1] * xyNormSD[,1])
  #lines(xyNormSD[,1], pca[2]$rotation[2,2]/pca[2]$rotation[1,2] * xyNormSD[,1])


#DATA centered and scaled:
  xyCovSD <- cov(xyNormSD)
  eigenValuesSD <- eigen(xyCovSD)$values
  eigenVectorsSD <- eigen(xyCovSD)$vectors
  
  plot(xyNormSD)
  
  lines(xyNormSD[,1], eigenVectorsSD[2,1]/eigenVectorsSD[1,1] * xyNormSD[,1])
  lines(xyNormSD[,1], eigenVectorsSD[2,2]/eigenVectorsSD[1,2] * xyNormSD[,1])



fit_plot <- function(df){
  plot (df$x, df$y, xlim=c(-2, 2), ylim=c(-2, 2))
  fit_x<- lm(df$y ~ df$x)
  lines(df$x, predict(fit_x), col="red")
}

fit_plot(as.data.frame(xyNormSD))
lines(xyNormSD[,1], eigenVectorsSD[2,1]/eigenVectorsSD[1,1] * xyNormSD[,1])
lines(xyNormSD[,1], eigenVectorsSD[2,2]/eigenVectorsSD[1,2] * xyNormSD[,1])





#DATA centered:
xyCov <- cov(xyNormMean)
eigenValues <- eigen(xyCov)$values
eigenVectors <- eigen(xyCov)$vectors

plot(xyNormMean)

lines(xyNormMean[,1], eigenVectors[2,1]/eigenVectors[1,1] * xyNormMean[,1])
lines(xyNormMean[,1], eigenVectors[2,2]/eigenVectors[1,2] * xyNormMean[,1])