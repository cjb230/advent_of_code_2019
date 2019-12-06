SOURCE_FILE = 'day_6_input.txt'


def main():
    satellite_parents = dict()
    satellite_depths = dict()

    with open(SOURCE_FILE) as f:
        orbits = [orbit.rstrip() for orbit in f.readlines()]
    #print(str(orbits))

    for orbit in orbits:
        #if orbit[3] != ')':
        #    print('ERROR: ' + orbit)
        satellite_parents[orbit[4:]] = orbit[0:3]
    #print('SATELLITE PARENTS: ' + str(satellite_parents))

    unfound_depths = list(satellite_parents.keys())
    #print(len(unfound_depths))
    #print('UNFOUND DEPTHS: ' + str(unfound_depths))
    satellite_depths['COM'] = 0
    #print('SATELLITE DEPTHS: ' + str(satellite_depths))

    while len(unfound_depths) > 0:
        newly_found_satellite = ''
        newly_found_depth = -1
        for this_satellite in unfound_depths:
            this_sat_parent = satellite_parents[this_satellite]
            if this_sat_parent in satellite_depths.keys():
                newly_found_satellite = this_satellite
                newly_found_depth = satellite_depths[this_sat_parent] + 1
                break

        if newly_found_satellite != '':
            #print('Found: ' + newly_found_satellite + ', depth = ' + str(newly_found_depth))
            satellite_depths[newly_found_satellite] = newly_found_depth
            unfound_depths.remove(newly_found_satellite)

    total_depths = 0
    for this_depth in satellite_depths.values():
        total_depths += this_depth

    print(str(total_depths))


if __name__ == "__main__":
    main()
