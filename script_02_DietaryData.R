system("java -version")
system("echo %JAVA_HOME%")

# note: 应该是如下的顺序安装
# install.packages("xlsxjars")
# install.packages("xlsx")

# 删包方式
# .libPaths()
# remove.packages("xlsx")

# check env and set env;
library(rJava)
options(java.parameters = "-Xmx16g")
library(rJava)
.jinit()

rm(list = ls())

currend_wd <- getwd()

str <- "Hello, World!"
print(str)

setwd("C:\\Users\\lvshu\\Desktop\\2024\\NHANES-2003-2004\\DietaryData")

library("foreign")
mydata1<-read.xport("DR1IFF_C.XPT")


library("xlsx")
write.xlsx(mydata1,file="DR1IFF_C.xlsx")
