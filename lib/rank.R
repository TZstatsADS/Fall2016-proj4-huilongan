'''
Huilong An -> project 4

you need to download similarity matrix file first.
Main idea behind my algorithm:
1.leave out matrix features first
2.randomly generate a sample as a baseline
3.calculate the Pearson correlation coefficients between one song with the baseline to get 
  a 13-d vector
4.use the Pearson correlation to calculate the similairy between new song and songs in database
5.finally get the ranked songs for each new song
6.rank the words
'''


# get in the data
sampleF <- read.csv('/users/andy/desktop/sample_submission.csv',header = T,encoding = 'UTF-8',stringsAsFactors = F)
simimat <- read.csv('/users/andy/desktop/similarity.csv',header = T)
lyric <- lyr
# fix the data
colnames(sampleF) <- c('ind',colnames(lyric))
sampleF <- sampleF[,2:ncol(sampleF)]
sampleF <- sampleF[1:100,]

# get word from similar songs 

# low efficiency algo  <abandoned>
findunion = function(i){
  record <- sort(simimat[i,],decreasing = T)
  nameid <- record[1]
  result <- c()
  for (j in seq(2,length(record))){
    similarsong <- names(record[j])
    songfind <- sort(lyric[lyric$`dat2$track_id`==similarsong,],decreasing = T)[-1]
    nonzero <- names(songfind[which(songfind != 0)])
    result <- union(result,nonzero)
    if (length(result) == 5000){
      return(result)
    }
  }
  return(result)
}
a <- findunion(1)


# use join -> focus on the first most similar songs only
simialgo = function(rown){
  tr <- sort(simimat[rown,],decreasing = T)
  trname <- tr[1]
  dictbook <- NULL
  count = 1
  for (i in names(tr[2:length(tr)])){
    dictbook[i] = count
    count = count + 1
  }
  temp <- lyr
  ranks = c()
  for (k in temp[,1]){
    ranks = c(ranks,dictbook[k])
  }
  temp$ranks <- ranks
  temp <- temp[order(temp$ranks),]
  temp2 <- temp
  a = 0
  begin = Sys.time()
  for (i in seq(300)){
    l <- length(temp2[i,])-1
    a = a + temp2[i,2:l] * (100/temp2[i,]$ranks)
    end <- Sys.time()  
    if (as.numeric(end-begin) >= 10){
      break
    }
  }
  return(list(name = trname,ranks = rank(a)))
}

# get the rank
names = sampleF$dat2.track_id
for (i in seq(1,100)){
  s <- simialgo(i)
  chose <- which(names==as.character(s$name$songid))
  print(chose)
  sampleF[chose,2:5001] = s$ranks
}

# write into csv

write.csv(sampleF,'/Users/andy/desktop/result_ha2399.csv')
