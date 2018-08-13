from csirtg_ipsml_tf.geo import asndb, citydb
import ipaddress
from csirtg_ipsml_tf.features import tz_data, cc_data


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


def fit_features(i):
    for l in i:
        try:
            l[1] = int(ipaddress.ip_address(l[1]))
        except:
            l[1] = int(ipaddress.ip_address(l[1].decode('utf-8')))

        l[4] = tz_data.transform([l[4]])[0]
        l[5] = cc_data.transform([l[5]])[0]

        yield l
