## Sidih helper functions

## Scraper
# Function to make a call to sidih
fetchSidihData <- function(indicator_id = 631,
                           user = 'siconpaz',
                           password = 's1conpaz',
                           date = '1950-1-1') {
  # url parameters
  burl = 'http://sidih.salahumanitaria.co/sissh/api/dato_sector.php'
  uparam = paste0('?user=', user)
  passparam = paste0('&password=', password)
  idparam = paste0('&ID_DATO=', indicator_id)
  upparam = paste0('&ACTUALIZACION=', date)
  
  # building url
  qurl = paste0(burl, uparam, passparam, idparam, upparam)
  
  # querying the url
  doc = fromJSON(getURL(qurl))
  
  # returning json
  return(doc)
}

# Fetch a list of indicators from SIDIH
# TODO: fix error handler. 
fetchSidihIndicatorMetadata <- function(indicator = NULL, all = F) {
  
  # determining how many indicators to iterate  
  if (all == TRUE) {
    total = 700  # Unknown number of indicators.
  }
  else total <- length(indicator)
  
  # iterating over the list of indicators
  pb <- txtProgressBar(min = 0, max = total, style = 3, char = '.')
  
  for (i in 1:total) {
    r = 1
    setTxtProgressBar(pb, i)
    
    tryCatch({
      doc = fetchSidihData(indicator[i])
    },
    error = function(e) {
      message(paste(i, ': indicator code does not exist.'))
      next
    }
    )
    
    
    # error handler function: tries 3 times per url / indicator
    # if all fail, it skips to the next indicator in the array
    tryCatch({
      it <- data.frame(
        indicator_id = doc[[1]]$metadato$ID_DATO,
        indicator_name = doc[[1]]$metadato$NOM_DATO,
        indicator_source = doc[[1]]$metadato$NOM_CON,
        maximum_disaggregation = doc[[1]]$metadato$DEFINICION_DATO,
        last_update_date = doc[[1]]$metadato$DESAGREG_GEO,
        number_of_datapoints = length(doc[[1]]$valores)
      )
      
      # assembling data.frame
      if (i == 1) out <- it
      else out <- rbind(out, it)
      
    },
    
    # If error occurs:
    error = function() {
      if (r >= 3) {
        message('Error fetching url. Trying again.')
        i = i - 1
        r = r + 1
      }
      else {
        message('Skipping.')
        next
      }
    }
    )
  }
  
  # returning output
  return(out)
}

# Function to query and download indicator
# data from Sidih.
fetchSidihIndicatorValues <- function(indicator = 631) {
  
  # iterating over the list of indicators
  for (j in 1:length(indicator)) {
    # fetching data
    cat(paste('Indicator:', indicator[j], '\n'))
    doc = fetchSidihData(indicator[j])
    
    # iterating over the results
    total <- length(doc[[1]]$valores)
    pb <- txtProgressBar(min = 0, max = total, style = 3, char = '.')
    for (i in 1:total) {
      setTxtProgressBar(pb, i)
      it <- data.frame(
        indicator_id = doc[[1]]$metadato$ID_DATO, 
        indicator_name = doc[[1]]$metadato$NOM_DATO,
        ID_VALDA = ifelse(is.null(doc[[1]]$valores[[i]]$ID_VALDA), NA, doc[[1]]$valores[[i]]$ID_VALDA),
        ID_MUN = ifelse(is.null(doc[[1]]$valores[[i]]$ID_MUN), NA, doc[[1]]$valores[[i]]$ID_MUN),
        ID_DEPTO = ifelse(is.null(doc[[1]]$valores[[i]]$ID_DEPTO), NA, doc[[1]]$valores[[i]]$ID_DEPTO),
        ID_UNIDAD = ifelse(is.null(doc[[1]]$valores[[i]]$ID_UNIDAD), NA, doc[[1]]$valores[[i]]$ID_UNIDAD),
        INI_VALDA = ifelse(is.null(doc[[1]]$valores[[i]]$INI_VALDA), NA, doc[[1]]$valores[[i]]$INI_VALDA),
        FIN_VALDA = ifelse(is.null(doc[[1]]$valores[[i]]$FIN_VALDA), NA, doc[[1]]$valores[[i]]$FIN_VALDA),
        VAL_VALDA = ifelse(is.null(doc[[1]]$valores[[i]]$VAL_VALDA), NA, doc[[1]]$valores[[i]]$VAL_VALDA)
      )
      
      # assembling data.frame
      if (i == 1) out <- it
      else out <- rbind(out, it)
    }
    # assembling overrall dataframe
    if (j == 1) nindicators <- out
    else nindicators <- rbind(nindicators, out)
  }
  
  # return output
  return(nindicators)
}