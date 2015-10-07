library(RODBC)
library(data.table)
library(plyr)
library(dplyr)
library(foreach)
library(doParallel)


rm(list=ls()) 

#list of unique identifiers to be plugged on the where clause
uniqueIdentifiers = c(
  123,
  456,
  789)

while (1==1)
{
  
  p = c('RODBC','data.table') # necessary libraries 
  cl <- makeCluster(4) # Number of tasks
  registerDoParallel(cl)
  result <- foreach(i=1:12, .packages=p) %dopar% { #number of queries
    myconn <-odbcConnect("odbc_connection_name")
    un <- sample(uniqueIdentifiers, size=1) # sample from the list
    
    
    query <- sprintf(
      'select uniqueIdentifier
       from ....
       where uniqueIdentifier= %d
       group by ....
       order by ....', un)
    result <-data.table(sqlQuery(myconn, query));
  }
  stopCluster(cl)
  
  result<- rbindlist(result)
  this_result <- result
  
  
  if (!exists("full_result")){ 
      full_result<-this_result
  } else {
      full_result <- rbind(full_result, this_result)
  }
  
  #group by uniqueIdentifier and executionid taking the row average to avoid double counting if the same uniqueIdentifier was queried twice on the same process
  group <- group_by (full_result, uniqueIdentifier, executionid)
  summary <-summarise(group, nrows = mean(nrows))
  
  
  group <- group_by (summary, uniqueIdentifier)
  summary <-summarise(group, n_runs = n(), rows_per_group  = mean(nrows), total_rows = sum(nrows))
  print(summary[order(summary$rows_per_group)])
                            
}