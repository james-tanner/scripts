## Add AudioBNC dialect information
## James Tanner
## July 2019

library(plyr)
library(tidyverse)
library(argparse)

parser <- ArgumentParser(description = "Read AudioBNC speaker CSV and return updated dialect information")
parser$add_argument('inputfile', help = "Original CSV file")
parser$add_argument('outputfile', help = "Where to write the new file")
args <- parser$parse_args()

cat("Reading", args$inputfile, "\n")
audioBNC <- read.csv(args$inputfile)

audioBNC <- audioBNC %>% rename(dialect_code = dialect)

## expand the dialect information based on the 3-letter code
## taken from http://www.natcorp.ox.ac.uk/docs/URG.xml
audioBNC$dialect <- NA
audioBNC$dialect[audioBNC$dialect_code == "CAN"] <- "Canadian"
audioBNC$dialect[audioBNC$dialect_code == "NONE"] <- "None"
audioBNC$dialect[audioBNC$dialect_code == "XDE"] <- "German"
audioBNC$dialect[audioBNC$dialect_code == "XEA"] <- "East Anglian"
audioBNC$dialect[audioBNC$dialect_code == "XFR"] <- "French"
audioBNC$dialect[audioBNC$dialect_code == "XHC"] <- "Home Counties"
audioBNC$dialect[audioBNC$dialect_code == "XHM"] <- "Humberside"
audioBNC$dialect[audioBNC$dialect_code == "XIR"] <- "Irish"
audioBNC$dialect[audioBNC$dialect_code == "XIS"] <- "Indian subcontinent"
audioBNC$dialect[audioBNC$dialect_code == "XLC"] <- "Lancashire"
audioBNC$dialect[audioBNC$dialect_code == "XLO"] <- "London"
audioBNC$dialect[audioBNC$dialect_code == "XMC"] <- "Central Midlands"
audioBNC$dialect[audioBNC$dialect_code == "XMD"] <- "Merseyside"
audioBNC$dialect[audioBNC$dialect_code == "XME"] <- "North-east Midlands"
audioBNC$dialect[audioBNC$dialect_code == "XMI"] <- "Midlands"
audioBNC$dialect[audioBNC$dialect_code == "XMS"] <- "South Midlands"
audioBNC$dialect[audioBNC$dialect_code == "XMW"] <- "North-west Midlands"
audioBNC$dialect[audioBNC$dialect_code == "XNC"] <- "Central Northern England"
audioBNC$dialect[audioBNC$dialect_code == "XNE"] <- "North-east England"
audioBNC$dialect[audioBNC$dialect_code == "XNO"] <- "Northern England"
audioBNC$dialect[audioBNC$dialect_code %in% c("XOT", "x")] <- "Other"
audioBNC$dialect[audioBNC$dialect_code == "XSD"] <- "Scottish"
audioBNC$dialect[audioBNC$dialect_code == "XSL"] <- "Lower south-west England"
audioBNC$dialect[audioBNC$dialect_code == "XSS"] <- "Central south-west England"
audioBNC$dialect[audioBNC$dialect_code == "XSU"] <- "Upper south-west England"
audioBNC$dialect[audioBNC$dialect_code == "XUR"] <- "European"
audioBNC$dialect[audioBNC$dialect_code == "XUS"] <- "American"
audioBNC$dialect[audioBNC$dialect_code == "XWA"] <- "Welsh"
audioBNC$dialect[audioBNC$dialect_code == "XWE"] <- "West Indian"

## add dialect regions based off of Trudgill's (1999) modern dialects
audioBNC$region[audioBNC$dialect %in% c(
	"Central Midlands",
	"North-east Midlands",
	"East Midlands",
	"Midlands")] <- "East Central England"
audioBNC$region[audioBNC$dialect %in% c(
	"North-west Midlands",
	"West Midlands",
	"Merseyside")] <- "West Central England"
audioBNC$region[audioBNC$dialect %in% c(
	"Humberside",
	"Lancashire",
	"Central Northern England",
	"Northern England")] <- "Lower North England"
audioBNC$region[audioBNC$dialect %in% c(
	"South Midlands",
	"East Anglian",
	"Home Counties",
	"London")] <- "East England"
audioBNC$region[audioBNC$dialect == "North-east England"] <- "North East England"
audioBNC$region[audioBNC$dialect %in% c(
	"Upper south-west England",
	"Lower south-west England",
	"Central south-west England")] <- "South West England"
audioBNC$region[audioBNC$dialect == "Irish"] <- "Ireland"
audioBNC$region[audioBNC$dialect == "Scottish"] <- "Scotland"
audioBNC$region[audioBNC$dialect == "Welsh"] <- "Wales"
audioBNC$region[audioBNC$dialect %in% c(
	"Indian subcontinent",
	"West Indian")] <- "India"
audioBNC$region[audioBNC$dialect %in% c(
	"European",
	"French",
	"German")] <- "Europe"
audioBNC$region[audioBNC$dialect %in% c(
	"Canadian",
	"American")] <- "North America"
audioBNC$region[audioBNC$dialect %in% c(
	"Other",
	"None")] <- "Other"

cat("Writing CSV to", args$outputfile, "\n")
write.csv(audioBNC, file = args$outputfile, quote = FALSE)