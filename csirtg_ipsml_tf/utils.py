from csirtg_ipsml_tf.geo import asndb, citydb


def extract_features(indicator, ts):
    # week?
    try:
        asn = asndb.asn(indicator)
    except:
        asn = None

    if asn:
        asn = asn.autonomous_system_number

    if asn is None:
        asn = 0

    try:
        city = citydb.city(indicator)
    except:
        city = None

    if city is None:
        yield [ts, indicator, 0, 0, 'NA', 'NA', 0]

    else:
        if not asn:
            asn = 0

        tz = city.location.time_zone
        if tz is None:
            tz = 'NA'

        cc = city.country.iso_code
        if cc is None:
            cc = 'NA'

        lat = city.location.latitude
        if lat:
            lat = int(lat)
        else:
            lat = 0

        long = city.location.longitude
        if long:
            long = int(long)
        else:
            long = 0

        # hour, src, dest, client, tz, cc, success
        yield [ts, indicator, lat, long, tz, cc, int(asn)]


def normalize_ips(indicators):
    return indicators
