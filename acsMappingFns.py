def createNCPopulationShp(USCountiesShp,Year, ACSPASS):
    '''
    Summary
    --------- 
    Function that accepts a shapefile of US county boundaries from TigerLine Download, the desired Year
    of population data, and an ACS API pass key. The function cuts the shapefile to just NC counties, 
    pulls total and race/ethnicity population data from the year designated (the rough midpoint of outcome data),
    renames columns for clarity, and merges the population data to the NC county shapefile. A shapefile
    of NC counties with population data is returned.

    Parameters
    ----------
    USCountiesShp : GeoPandas Shapefile (Polygon)
        Shapefile of all county boundaries from https://www.census.gov/cgi-bin/geo/shapefiles/index.php.
    ACSPASS : API Key
        Obtain from https://api.census.gov/data/key_signup.html.
    Year : Year (XXXX)
        Year of data that will be used when pulling ACS population data.

    Returns
    -------
    NCcountiespop : GeoPandas Shapefile (Polygon)
        NC County boundaries, with NC race and ethnicity population data.

    '''
    import censusdata
    NCcounties= USCountiesShp[USCountiesShp['STATEFP']=='37'] #restrict to NC only
    ncpop = censusdata.download('acs5', Year,
                             censusdata.censusgeo([('state', '37'),('county','*')]),
                             ["GEO_ID","B02001_001E", "B02001_002E", "B02001_003E","B03002_012E"],ACSPASS,'detail') #download total, white, black, and hispanic population data
    ncpop= ncpop.rename(columns={'B02001_001E': 'Total Population','B02001_002E': 'White','B02001_003E':'Black', 'B03002_012E':'Hispanic'}) #rename columns
    ncpop['GEOID']= ncpop["GEO_ID"].str[-5:]  #create linking GEOID field to link to shp
    NCcountiespop = NCcounties.merge(ncpop, on='GEOID') #add population data to shapefile    
    return NCcountiespop #return NCcountiespop
