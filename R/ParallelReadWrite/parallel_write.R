library(foreach)
library(doParallel)


uniqueIdentifiers = c(
  123,
  456,
  789)


library(RODBC)
library(data.table)
library(foreach)
library(doParallel)

?makeCluster

clw <- makeCluster(30)
registerDoParallel(clw)
a<- foreach(i=1:50) %dopar% { 
  un <- sample(uniqueIdentifiers, size=1)
  #calls the write command; in this case using an SSIS package on the file system, but could be a procedure on the server
  command<- sprintf('dtexec /file package.dtsx /SET "\\Package.Variables[User::uniqueIdentifier].Properties[Value]";"%d"', un)
  r <- system(command, intern = TRUE)
 
}
stopCluster(clw)
warnings()

a

