from geolib import geohash as gh # type: ignore

PRECISION = 9

def geohash(lat_lon: tuple[float,float]) -> str:
    return gh.encode(*lat_lon,PRECISION)


if __name__ == "__main__":
    shanghai = 31.2304, 121.4737
    print(f"The geohash of Shanghai: {geohash(shanghai)}")