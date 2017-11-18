setwd("~/projects/dissertation/uncategorized/physiology/CTminmax/data/")

alldata <- read.csv("CTminmax_processed_final.csv")

hot <- subset(alldata, alldata$treatment == "hot")
cold <- subset(alldata, alldata$treatment == "cold")

allrange <- read.csv("CTminmax_both_final.csv")
allrange <- na.omit(allrange)

setwd("~/projects/dissertation/uncategorized/physiology/CTminmax/analysis/")

spnames <- c("virgulatus", "conjunctus", "hallani", "clypeatus", "pugillis", "geronimoi")
spcols <- c("green", "pink", "purple", "red", "blue", "orange")

cly <- subset(alldata, alldata$species == "clypeatus")
pug <- subset(alldata, alldata$species == "pugillis")
vir <- subset(alldata, alldata$species == "virgulatus")
ger <- subset(alldata, alldata$species == "geronimoi")
con <- subset(alldata, alldata$species == "conjunctus")
hal <- subset(alldata, alldata$species == "hallani")

clycold <- subset(cly, cly$treatment == "cold")
pugcold <- subset(pug, pug$treatment == "cold")
vircold <- subset(vir, vir$treatment == "cold")
gercold <- subset(ger, ger$treatment == "cold")
concold <- subset(con, con$treatment == "cold")
halcold <- subset(hal, hal$treatment == "cold")

clyhot <- subset(cly, cly$treatment == "hot")
pughot <- subset(pug, pug$treatment == "hot")
virhot <- subset(vir, vir$treatment == "hot")
gerhot <- subset(ger, ger$treatment == "hot")
conhot <- subset(con, con$treatment == "hot")
halhot <- subset(hal, hal$treatment == "hot")

clyrange <- subset(allrange, allrange$species == "clypeatus")
pugrange <- subset(allrange, allrange$species == "pugillis")
virrange <- subset(allrange, allrange$species == "virgulatus")
gerrange <- subset(allrange, allrange$species == "geronimoi")
conrange <- subset(allrange, allrange$species == "conjunctus")
halrange <- subset(allrange, allrange$species == "hallani")

clyrangecold <- subset(clyrange, clyrange$treatment == "cold")
pugrangecold <- subset(pugrange, pugrange$treatment == "cold")
virrangecold <- subset(virrange, virrange$treatment == "cold")
gerrangecold <- subset(gerrange, gerrange$treatment == "cold")
conrangecold <- subset(conrange, conrange$treatment == "cold")
halrangecold <- subset(halrange, halrange$treatment == "cold")

clyrangehot <- subset(clyrange, clyrange$treatment == "hot")
pugrangehot <- subset(pugrange, pugrange$treatment == "hot")
virrangehot <- subset(virrange, virrange$treatment == "hot")
gerrangehot <- subset(gerrange, gerrange$treatment == "hot")
conrangehot <- subset(conrange, conrange$treatment == "hot")
halrangehot <- subset(halrange, halrange$treatment == "hot")

par(mfrow=c(1,1))
boxplot(vircold$down_20sec, concold$down_20sec, halcold$down_20sec, clycold$down_20sec, pugcold$down_20sec, gercold$down_20sec, col = spcols, names = spnames, ylim = c(0, 60), ylab = expression(paste("Thermal Limit (",degree,"C)")), xlab = "Species")
boxplot(virhot$down_20sec, conhot$down_20sec, halhot$down_20sec, clyhot$down_20sec, pughot$down_20sec, gerhot$down_20sec, col = spcols, add = TRUE, axes = FALSE)
boxplot(virrange$range_20, conrange$range_20, halrange$range_20, clyrange$range_20, pugrange$range_20, gerrange$range_20, col = spcols, names = spnames, las =2, ylab = expression(paste("Thermal Range (",degree,"C)")))

aovcold <- aov(cold$down_20sec~cold$species)

aovhot <- aov(hot$down_20sec~hot$species)


rangecheck <- aov(allrange$range_20~allrange$species)

plot(virrange$mass_cold~virrange$range_20, xlim = c(30, 50), ylim = c(0,40), col = "green")
lines(gerrange$mass_cold~gerrange$range_20, col = "orange", type = "p")
lines(clyrange$mass_cold~clyrange$range_20, col = "red", type = "p")
lines(pugrange$mass_cold~pugrange$range_20, col = "blue", type = "p")
lines(halrange$mass_cold~halrange$range_20, col = "pink", type = "p")
lines(conrange$mass_cold~conrange$range_20, col = "purple", type = "p")


plot(hot$mass~hot$down_20sec, col = "red", xlim = c(0,60))
lines(cold$mass~cold$down_20sec, col = "blue", type = "p")

#check for effects of sex
aovhotsex <- aov(hot$down_20sec~hot$sex)
summary(aovhotsex)

aovcoldsex <- aov(cold$down_20sec~cold$sex)
summary(aovcoldsex)

aovrangesex <- aov(allrange$range_20~allrange$sex)
summary(aovrangesex)

#effects of mass

aovhotmass <- aov(hot$down_20sec~hot$mass)
summary(aovhotmass)

aovcoldmass <- aov(cold$down_20sec~cold$mass)
summary(aovcoldmass)

aovrangemass <- aov(allrange$range_20~allrange$mass_cold)
summary(aovrangemass)

sink("statsout.txt", append=FALSE, split=FALSE)

#Species
summary(aovhot)
TukeyHSD(aovhot)

summary(aovcold)
TukeyHSD(aovcold)

summary(rangecheck)
TukeyHSD(rangecheck)

#Sex

sink()