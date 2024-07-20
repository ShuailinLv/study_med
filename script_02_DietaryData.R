rm(list = ls())
rm(mydata1)
currend_wd <- getwd()

str <- "Hello, World!"
print(str)

setwd("C:/Users/Lenovo/Desktop/2024/NHANES-2003-2004/DietaryData")

library("foreign")
mydata1<-read.xport("DR1IFF_C.XPT")


library("xlsx")
write.xlsx(mydata1,file="DR1IFF_C.xlsx")
# data doc https://wwwn.cdc.gov/Nchs/Nhanes/2003-2004/DEMO_C.htm 


