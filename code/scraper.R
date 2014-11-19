## Collection of functions to query
## the SIDIH indicator API.

# dependencies
library(RCurl)
library(rjson)

# deploy function
onSw <- function(a = T, d = '~/tool/') {
	if (a == T) return(b)
	else return('')
}

# helper functions
source(paste0(onSw(), 'code/write_tables.R'))
source(paste0(onSw(), 'code/sw_status.R'))
source(paste0(onSw(), 'code/sidih.R'))

# wrapper for the scraper
runScraper <- function(test = F) {
  # Data collection
  ind_list = c(631)  # add the indicator codes here
  fetchSidihIndicatorValues(ind_list)
  
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

