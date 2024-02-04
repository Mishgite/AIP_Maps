def get_scale_params(object_longitude, object_latitude, delta1, delta2, l, pt=None):
    ll = f"{object_longitude},{object_latitude}"
    spn = f"{delta1},{delta2}"
    dct = {
        'll': ll,
        'spn': spn,
        'l': l,
    }

    if pt is not None:
        dct['pt'] = f'{",".join(pt)},round'

    return dct
