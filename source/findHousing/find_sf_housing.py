# Extended Python
from craigslist import CraigslistHousing
import yaml

# Created Python
from utilities import dist_coords

with open('neighborhood_bounds.yaml', 'r') as coord_lookup:
    neighborhood_coords = yaml.load(coord_lookup) 

with open('shuttle_coordinates.yaml', 'r') as coord_lookup:
    shuttle_coords = yaml.load(coord_lookup)

sf_housing = CraigslistHousing(site='sfbay', area='sfc', category='apa',
        filters={'max_price': 1700, 'min_price':1000,
                 'has_image': True})

pen_housing = CraigslistHousing(site='sfbay', area='pen', category='apa',
        filters={'max_price': 1700, 'min_price':1000,
                 'has_image': True})

def get_housing_results(location):
    """
    Get the search results
    """
    if location == 'sf':
       housing_found = sf_housing.get_results(sort_by='newest', geotagged=True, limit=20)
       results = []
       for result in housing_found:
          results.append(result)
    if location == 'pen':
       housing_found = pen_housing.get_results(sort_by='newest', geotagged=True, limit=20)
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
    lon = coordinates[1]

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

def shuttle_stop_nearby(search_result, stop, max_distance):
    """
    Check if location is nearby a shuttle stop
    """
    if search_result['geotag']:
        coordinates = search_result['geotag'] 
    else:
        return False

    lat = coordinates[0]
    lon = coordinales[1]
     
    stop_lat = shuttle_coords[stop][0]
    stop_lon = shuttle_coords[stop][1]

    distance = dist_coords(lat, lon, stop_lat, stop_lon)

    if distance < max_distance:
        return True

def find_sf_neighborhood_housing():
    """
    San Francisco Housing BB
    """
    filtered_results = []
    housing_results = get_housing_results('sf')
    sf_hoods = neighborhood_coords['sf']

    for hood in sf_hoods:
        for result in housing_results:
            if in_location_specified(result, sf_hoods[hood]):
                filtered_results.append(result)
    
    for hood in sf_hoods:
        for result in housing_results:
            if in_neighborhood(result, hood):
                filtered_results.append(result)

    return filtered_results

def find_pen_neighborhood_housing():
    """
    San Francisco Housing BB
    """
    filtered_results = []
    housing_results = get_housing_results('pen')
    pen_hoods = neighborhood_coords['south_bay']

    for hood in pen_hoods:
        for result in housing_results:
            if in_location_specified(result, pen_hoods[hood]):
                filtered_results.append(result)
    
    for hood in pen_hoods:
        for result in housing_results:
            if in_neighborhood(result, hood):
                filtered_results.append(result)

    return filtered_results
