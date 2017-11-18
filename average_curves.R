setwd("~/projects/dissertation/uncategorized/physiology/CTminmax/data/temp_data")


f3_1 <- read.csv("3-1.csv",nrows=1886)
f3_2 <- read.csv("3-2.csv",nrows=1886)
f3_3 <- read.csv("3-3.csv",nrows=1886)
f5_1 <- read.csv("5-1.csv",nrows=1886)
f5_2 <- read.csv("5-2.csv",nrows=1886)
f5_4 <- read.csv("5-4.csv",nrows=1886)
f6_1 <- read.csv("6-1.csv",nrows=1886)
f6_2 <- read.csv("6-2.csv",nrows=1886)
f6_3 <- read.csv("6-3.csv",nrows=1886)
f7_1 <- read.csv("7-1.csv",nrows=1886)
#f7_2 <- read.csv("7-2.csv")
f7_3 <- read.csv("7-3.csv",nrows=1886)
f7_4 <- read.csv("7-4.csv",nrows=1886)
f9_1 <- read.csv("9-1.csv",nrows=1886)
f9_2 <- read.csv("9-2.csv",nrows=1886)
f9_3 <- read.csv("9-3.csv",nrows=1886)
f9_4 <- read.csv("9-4.csv",nrows=1886)
f11_1 <- read.csv("11-1.csv",nrows=1886)
f11_3 <- read.csv("11-3.csv",nrows=1886)
f11_4 <- read.csv("11-4.csv",nrows=1886)

full7_1 <- read.csv("7-1.csv")
plot(full7_1$Channel.1~full7_1$Channel.1, xlim = c(0,1800) )

ch1 <- data.frame(f3_1$Channel.1, f3_2$Channel.1, f3_3$Channel.1, f5_1$Channel.1, f5_2$Channel.1,f5_4$Channel.1,f6_1$Channel.1, f6_2$Channel.1, f6_3$Channel.1, f7_1$Channel.1, f7_3$Channel.1, f7_4$Channel.1, f9_1$Channel.1,f9_2$Channel.1, f9_3$Channel.1,f9_4$Channel.1, f11_1$Channel.1, f11_3$Channel.1, f11_4$Channel.1)
ch1$avg <-rowMeans(ch1, na.rm = TRUE)
ch1$sd <- apply(ch1, 1, sd)
ch1$sdplus <- ch1$avg + ch1$sd
ch1$sdminus <- ch1$avg - ch1$sd

ch2 <- data.frame(f3_1$Channel.2, f3_2$Channel.2, f3_3$Channel.2, f5_1$Channel.2, f5_2$Channel.2,f5_4$Channel.2,f6_1$Channel.2, f6_2$Channel.2, f6_3$Channel.2, f7_1$Channel.2, f7_3$Channel.2, f7_4$Channel.2, f9_1$Channel.2,f9_2$Channel.2, f9_3$Channel.2,f9_4$Channel.2, f11_1$Channel.2, f11_3$Channel.2, f11_4$Channel.2)
ch2$avg <-rowMeans(ch2, na.rm = TRUE)

ch3 <- data.frame(f3_1$Channel.3, f3_2$Channel.3, f3_3$Channel.3, f5_1$Channel.3, f5_2$Channel.3,f5_4$Channel.3,f6_1$Channel.3, f6_2$Channel.3, f6_3$Channel.3, f7_1$Channel.3, f7_3$Channel.3, f7_4$Channel.3, f9_1$Channel.3,f9_2$Channel.3, f9_3$Channel.3,f9_4$Channel.3, f11_1$Channel.3, f11_3$Channel.3, f11_4$Channel.3)
ch3$avg <-rowMeans(ch3, na.rm = TRUE)

ch4 <- data.frame(f3_1$Channel.4, f3_2$Channel.4, f3_3$Channel.4, f5_1$Channel.4, f5_2$Channel.4,f5_4$Channel.4,f6_1$Channel.4, f6_2$Channel.4, f6_3$Channel.4, f7_1$Channel.4, f7_3$Channel.4, f7_4$Channel.4, f9_1$Channel.4,f9_2$Channel.4, f9_3$Channel.4,f9_4$Channel.4, f11_1$Channel.4, f11_3$Channel.4, f11_4$Channel.4)
ch4$avg <-rowMeans(ch4, na.rm = TRUE)

average <- data.frame(f3_1$Time,ch1$avg, ch2$avg, ch3$avg, ch4$avg)

plot(average$ch1.avg~average$f3_1.Time, type = "l", col = "red", lty = 1, ylim = c(37, 55))
lines(ch1$sdplus~average$f3_1.Time)
lines(ch1$sdminus~average$f3_1.Time)


lines(average$ch2.avg~average$f3_1.Time, col = "red")
lines(average$ch3.avg~average$f3_1.Time, col = "green")
lines(average$ch4.avg~average$f3_1.Time, col = "blue")


dev.off()




test7_1 <- read.csv("7-1.csv")


plot(test7_1$Channel.1~test7_1$Time)

