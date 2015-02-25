## Collection of functions to query
## the SIDIH indicator API.

# dependencies
library(RCurl)
library(rjson)

# Configuration
ind_list = c(631)  # add the indicator codes here

# deploy function
onSw <- function(a = F, d = '~/tool/') {
	if (a == T) return(d)
	else return('')
}

# helper functions
source(paste0(onSw(), 'code/write_tables.R'))
source(paste0(onSw(), 'code/sw_status.R'))
source(paste0(onSw(), 'code/sidih.R'))

# wrapper for the scraper
runScraper <- function(test = F) {
  # Data collection
  indicators_data <- fetchSidihIndicatorValues(ind_list)
  
  # Writing output in database
  writeTables(indicators_data, 'indicators_data', 'scraperwiki')
  
  # Storing the data (and running tests)
  if (test == T) cat('No tests yet.\n')
}

# Changing the status of SW.
tryCatch(runScraper(),
         error = function(e) {
           cat('Error detected ... sending notification.')
           system('mail -s "SIDIH failed" luiscape@gmail.com')
           changeSwStatus(type = "error", message = "Scraper failed.")
{ stop("!!") }
         }
)
# If success:
changeSwStatus(type = 'ok')

