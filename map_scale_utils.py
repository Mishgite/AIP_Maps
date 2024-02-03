def get_scale_params(object_longitude, object_latitude, z, l, pt=None):
    ll = f"{object_longitude},{object_latitude}"
    dct = {
        'll': ll,
        'z': z,
        'l': l,
    }

    if pt is not None:
        dct['pt'] = f'{",".join(pt)},round'

    return dct
