class color(object):
    def __init__(this, r, g, b) -> None:
        this.r = r
        this.g = g
        this.b = b

    def __add__(this, other):
        return color(
            this.r + other.r,
            this.g + other.g,
            this.b + other.b
        )

    def __mul__(this, other):
        if type(other) is color:
            return color(
                this.r * other.r,
                this.g * other.g,
                this.b * other.b
            )
        else:
            return color(
                this.r * other,
                this.g * other,
                this.b * other
            )

    def toBytes(this) -> bytes:
        if this.b > 255:
            this.b = 255
        if this.g > 255:
            this.g = 255
        if this.r > 255:
            this.r = 255

        if this.b <0:
            this.b = 0
        if this.g <0:
            this.g = 0
        if this.r <0:
            this.r = 0

        return bytes([int(this.b), int(this.g), int(this.r)])