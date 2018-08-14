from csirtg_ipsml_tf.geo import asndb, citydb
import ipaddress
from csirtg_ipsml_tf.features import tz_data, cc_data
import arrow


def extract_features(indicator, ts):
    ts = arrow.get(ts)
    ts = ts.hour

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

    # v6???
    try:
        indicator = int(ipaddress.ip_address(indicator))
    except:
        indicator = int(ipaddress.ip_address(indicator.decode('utf-8')))

    if city is None:
        #yield [ts, indicator, 0, 0, 'NA', 'NA', 0]
        yield [ts, tz_data.transform(['NA'])[0], cc_data.transform(['NA'])[0]]

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

        tz = tz_data.transform([tz])[0]
        cc = cc_data.transform([cc])[0]
        # hour, src, dest, client, tz, cc, success
        #yield ts, indicator, lat, long, tz, cc, int(asn)
        #yield ts, lat, long, tz, cc, int(asn)
        yield [ts, tz, cc]


def normalize_ips(indicators):
    return indicators
