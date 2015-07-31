rm(list=ls()) 
setwd('<WD>')
library(RODBC)
library(data.table)
myconn <-odbcConnect("ODBC_CONN_NAME", uid="user_name", pwd="password")

query_1 ='
query1
'

query_2 ='
query2 
'

query_3 ='
query3
'


rm()
snapshots ='select XXX as random_where from ....'
a <-sqlQuery(myconn, snapshots);
a <-data.table(a)

#save RDS each how many runs?(in case something fails - out of memory or something)
savecount=10
runcount=0

#object where the metrics are stored
if (exists("my_df")){
  rm(my_df)
}

for (i in 1:100 ) {
  runcount=runcount+1
  #get a random value from the "a" dataset that contains all possible values to be used on the where clause
  sample_snap = sample(x = min(a$random_where):max(a$random_where), size = 1)
  
  
  a = paste(query_1, sample_snap, sep="")
  b = paste(query_2, sample_snap, sep="")
  c = paste(query_3, sample_snap, sep="")
  
  
  begin <- Sys.time()
  begin_ = begin
  sqlQuery(myconn, a);
  end <- Sys.time()
  dur_a = as.numeric(end-begin,units="secs")
  
  begin <- Sys.time()
  sqlQuery(myconn, b);
  end <- Sys.time()
  dur_b = as.numeric(end-begin,units="secs")
  
  
  begin <- Sys.time()
  sqlQuery(myconn, c);
  end <- Sys.time()
  end_ = end
  dur_c = as.numeric(end-begin,units="secs")
  
  
  if (!exists("my_df")){
    my_df<-data.frame(begin_,sample_snap,dur_a, dur_b, dur_c,end_)
  } else {
    my_df<-rbind(my_df,data.frame(begin_,sample_snap,dur_a, dur_b, dur_c,end_))
  }
  
  if (runcount==savecount){
    name=gsub("[ ]","_",end_) 
    name=gsub("[:]","_",name) 
    saveRDS(my_df, name)
    runcount = 0
  }
}  

name=gsub("[ ]","_",end_) 
name=gsub("[:]","_",name) 
name=paste(name,"final",sep="_")
saveRDS(my_df, name)
