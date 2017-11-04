from craigslist import CraigslistHousing
import yaml

with open('coordinates.yaml', 'r') as coord_lookup:
    coordinates = yaml.load(coord_lookup) 

housing = CraigslistHousing(site='sfbay', area='sfc', category='apa',
        filters={'max_price': 1600, 'min_price':1000,
                 'has_image': True})

        
def get_housing_results():
    """
    Get the search results
    """
    housing_found = housing.get_results(sort_by='newest', geotagged=True, limit=20)
    results = []
    for result in housing_found:
        results.append(result)

    return results

def in_location_specified(search_result, bounding_box):
    """
    Check if location is in the bounding box for an area
    """
    if search_result['geotag']:
        coordinates = search_result['geotag'] 
    else:
        return False

    lat = coordinates[0]
    lon = coordinales[1]

    bb_lat_low = bounding_box[0][0]
    bb_lat_up = bounding_box[1][0]
    bb_lon_low = bounding_box[0][1]
    bb_lon_up = bounding_box[1][1]

    if bb_lat_low < lat < bb_lat_up:
        if bb_lon_low < lon < bb_lon_up:
            return True

    return False

def in_neighborhood(search_result, neighborhood):
    """
    Check if location is in the neighborhood
    """
    if search_result['where']:
        hood = search_result['where'].lower()
    else:
        return False

    if neighborhood in hood:
        # neighborhood is often more specific than the posting
        return True

    return False

    


