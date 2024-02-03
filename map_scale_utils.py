def get_scale_params(object_longitude, object_latitude, z, l):
    ll = f"{object_longitude},{object_latitude}"
    return {"ll": ll, "z": z, "l": l}
