def get_scale_params(object_longitude, object_latitude, delta="0.005"):
    spn = ",".join([delta, delta])
    ll = f"{object_longitude},{object_latitude}"
    return {"ll": ll, "spn": spn}