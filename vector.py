import math

class Vector(object):
    """ This class represents a general-purpose vector class.  We'll
        add more to this in later labs.  For now, it represents a
        position and/or offset in n-dimensonal space. """

    def __init__(self, *args):
        """
        The constructor
        :param args: This is a variable-length argument-list.  In reality, you create a Vector like this:
               v = Vector(1, 2, 3)
        :return: N/A for constructors
        """
        self.mData = []
        for value in args:
            self.mData.append(float(value))
        self.mDim = len(args)

        # This is a little bit ugly, but if the user passes us one of the "special" number of elements in args,
        # use the specialized class.  For example, if there are 2 elements in args, make this new instance a Vector2 instead
        # of a generic Vector object.
        if len(args) == 2:
            self.__class__ = Vector2
        elif len(args) == 3:
            self.__class__ = Vector3

    def __str__(self):
        """
        Note: You don't normally call this directly.  It is called indirectly when you do something like:
            v = Vector(1, 2, 3)
            x = str(v)               # Same as x = v.__str__()
            print(v)                 # print calls str internally
        :return: The string-representation of this Vector
        """
        s = "<Vector" + str(len(self)) + ": "
        for i in range(len(self.mData)):
            s += str(self.mData[i])
            if i < len(self) - 1:
                s += ", "
        s += ">"
        return s

    def __len__(self):
        """
        Note: You don't normally call this method directly.  It's called by the built-in len function
            v = Vector(1, 2, 4)
            print(len(v))           # 3
        :return: An integer indicating the dimension of this vector
        """
        return self.mDim

    def __getitem__(self, index):
        """
        Note: You don't normally call this method directly.  It's called by using [] on a Vector
            v = Vector(1, 2, 3)
            print(v[0])                 # 1
            print(v[-1])                # 3
        :param index: An integer.  A python exception will be thrown if it's not a valid position in self.mData
        :return: The float value at position index.
        """
        return self.mData[index]

    def __setitem__(self, index, newval):
        """
        This method is similar to __getitem__, but it is called when we assign something to an index
           v = Vector(1, 2, 3)
           v[0] = 99
           print(v)                 # <Vector3: 1.0, 2.0, 99.0>
        :param index: An integer.  A python exception will be thrown if it's not a valid position in self.mData
        :param newval: A value that can be converted to a float using the float function
        :return: None
        """
        self.mData[index] = float(newval)

    def __eq__(self, other):
        """
        Note: This method isn't normally called directly.  Instead, it is called indirectly when a Vector
              is on the left-hand side of an ==.  It returns True if the values within the other vector
              are the same as those in this vector.
        :param other: any value
        :return: a boolean.  True if the other thing is a Vector *and* has the same values as this Vector.
        """
        if isinstance(other, Vector) and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        else:
            return False
        
        
    def __add__(self, otherV):
        """
        Adds this vector to the other vector (on the right-hand side of the '+' operator), producing a new vector
        :param otherV: A Vector of the same size as this vectorN
        :return: The Vector sum (of the same type as the left-hand side of the '+' operator)
        """
        if not isinstance(otherV, Vector) or len(otherV) != len(self):
            n = str(len(self))
            raise TypeError("You can only add another Vector" + n + " to this Vector" + n + " (you passed '" + str(otherV) + "')")
        r = self.copy()
        for i in range(self.mDim):
            r[i] += otherV[i]
        return r


    def __sub__(self, otherV):
        """
        Subtracts the other vector (on the right-hand side of the '+' operator) from this vector, producing a new vector
        :param otherV: A Vector of the same size as this vectorN
        :return: The Vector sum (of the same type as this object)
        """
        if not isinstance(otherV, Vector) or len(otherV) != len(self):
            n = str(len(self))
            raise TypeError("You can only subtract another Vector" + n + " from this Vector" + n + " (you subtracted '" + str(otherV) + "')")
        r = self.copy()
        for i in range(self.mDim):
            r[i] -= otherV[i]
        return r


    def __mul__(self, scalar):
        """
        Multiplies this vector with a scalar.
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] *= scalar
        return r


    def __rmul__(self, scalar):
        """
        This performs vector-scalar multiplication (like __mul__).  This method is necessary, though, in the
        case in which the scalar is on the left hand side of the '*' (rather than the right-hand side in the __mul__
        method.
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] *= scalar
        return r



    def __truediv__(self, scalar):
        """
        Returns a copy of this vector divided by the given scalar
        :param scalar: the value to multiply this vector by (integer or float)
        :return: a copy of this vector with all values multiplied by the scalar
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.mDim)
            raise TypeError("You can only divide this " + n + " by a scalar. You attempted to divide by '" + str(scalar) + "'")
        r = self.copy()
        for i in range(self.mDim):
            r[i] /= scalar
        return r



    def __neg__(self):
        """
        :return: A negated copy of this vector
        """
        r = self.copy()
        for i in range(self.mDim):
            r[i] = -r[i]
        return r

    @property
    def i(self):
        """
        returns a "fake" tuple of ints of our current vector
        :return:
        """
        # build the value for the FAKE-ATTRIBUTE i
        for i in range(len(self.mData)):
            self.mData[i] = int(self.mData[i])
        # I made it into a tuple because that's what was on the lab, I think
        # it would work as a list as well
        return tuple(self.mData)

    @property
    def magnitude(self):
        """
        :return: The scalar magnitude of this vector
        """
        m = 0.0
        for val in self.mData:
            m += val ** 2
        return m ** 0.5


    @property
    def magnitude_squared(self):
        """
        :return: The magnitude of this vector squared.  Wherever possible, use this method rather than
                 magnitude as this method doesn't involve a square root (which is costly to compute)
        """
        m = 0.0
        for val in self.mData:
            m += val ** 2
        return m


    @property
    def normalized(self):
        """
        :return: A normalized copy of this vector.   If this vector is a zero vector, a copy is returned.
        """
        r = self.copy()
        mag = self.magnitude
        if mag == 0.0:
            return r
        for i in range(self.mDim):
            r[i] /= mag
        return r


    @property
    def is_zero(self):
        """
        :return: True if this vector is a zero-vector.
        """
        for val in self.mData:
            if val != 0.0:
                return False
        return True


    def copy(self):
        """
        Creates a 'deep' copy of this Vector and returns it
        :return: a new Vector copy of this Vector
        """
        v = Vector(*self.mData)
        # This makes sure the copy is of the same type as the original (this is especially important if self
        # is a specialized vector class like Vector2.
        v.__class__ = self.__class__
        return v





class Vector2(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 2d applications and makes
        accessing the components (by name) a little easier as well as adding some polar conversion properties """
    def __init__(self, x, y):
        # Feed these elements to the base-class constructor
        super().__init__(x, y)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_val):
        self.mData[0] = float(new_val)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_val):
        self.mData[1] = float(new_val)

    @property
    def degrees(self):
        return math.degrees(math.atan2(self.mData[1], self.mData[0]))

    @property
    def radians(self):
        return math.atan2(self.mData[1], self.mData[0])





class Vector3(Vector):
    """ This is a specialization of Vector.  This will mainly be used for 3d applications and makes
            accessing the components (by name) a little easier """
    def __init__(self, x, y, z):
        # Feed these elements to the base-class constructor
        super().__init__(x, y, z)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_val):
        self.mData[0] = float(new_val)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_val):
        self.mData[1] = float(new_val)

    @property
    def z(self):
        return self.mData[2]

    @z.setter
    def z(self, new_val):
        self.mData[2] = float(new_val)



def polar_to_vector2(radians, hypotenuse):
    return Vector2(hypotenuse * math.cos(radians), hypotenuse * math.sin(radians))

def dot(v, w):
    # do error checking to make sure v and w are
    # both Vectors and same dimmension too, -raise exception
    if not isinstance(v, Vector):
        raise TypeError("Your entered values have to be vectors with the same dimensions...You entered" + str(v) + " " + str(v.mDim) +  " smh")
    if not isinstance(w, Vector):
        raise TypeError("Your entered values have to be vectors with the same dimensions...You entered" + str(w) + " " + str(w.mDim) + " smh")

    if v.mDim != w.mDim:
        raise ValueError("your entered values have to be vectors with the same dimmensions...You entered" + str(v.mDim) + " and " + str(w.mDim) + " smh")

    result = 0

    for i in range(v.mDim):
        result += v[i] * w[i]
    return result

def cross(v, w):
    # must be vector3's
    if not isinstance(v, Vector3):
        raise TypeError("Your entered values have to both be Vector 3s. You entered " + str(v))
    if not isinstance(w, Vector3):
        raise TypeError("Your entered values have to both be Vector 3s. You entered " + str(w))

    new_x = v.y * w.z - v.z * w.y
    new_y = v.z * w.x - v.x * w.z
    new_z = v.x * w.y - v.y * w.x
    new_vector = Vector3(new_x, new_y, new_z)
    return new_vector

if __name__ == "__main__":
    v = Vector(5, -2, 1, 0.5)
    w = Vector(7, 3, 4.5, 2.1)
    z = Vector(5, 0, 3)
    q = Vector(0, 0, 0)

    print("v =", v)                         # v = <Vector4: 5.0, -2.0, 1.0, 0.5>
    print("w =", w)                         # w = <Vector4: 7.0, 3.0, 4.5, 2.1>
    print("z =", z)                         # z = <Vector3: 5.0, 0.0, 3.0>
    print("q =", q)                         # q = <Vector3: 0.0, 0.0, 0.0>
    print("v + w =", v + w)                 # v + w = <Vector4: 12.0, 1.0, 5.5, 2.6>
    #print("v + 5 =", v + 5)                # TypeError: You can only add another Vector4 to this Vector4 (you passed '5')
    print("v =", v)                         # v = <Vector4: 5.0, -2.0, 1.0, 0.5> (unchanged by addition or similar methods)

    print("v - w =", v - w)                 # v - w = <Vector4: -2.0, -5.0, -3.5, -1.6>
    #print("v - 5 =", v - 5)                # TypeError: You can only subtract another Vector4 from this Vector4 (you subtracted '5')
    print("-v =", -v)                       # -v = <Vector4: -5.0, 2.0, -1.0, -0.5>
    print("2 * v =", 2 * v)                 # 2 * v = <Vector4: 10.0, -4.0, 2.0, 1.0>
    print("v * 2 =", v * 2)                 # v * 2 = <Vector4: 10.0, -4.0, 2.0, 1.0>
    print("v / 2 =", v / 2)                 # v / 2 = <Vector4: 2.5, -1.0, 0.5, 0.25>
    print("v * 1.5 =", v * 1.5)             # v * 1.5 = <Vector4: 7.5, -3.0, 1.5, 0.75>
    #print("v * w =", v * w)                # TypeError: You can only multiply this Vector4 and a scalar. You attempted to multiply
                                            #    by '<Vector4: 7.0, 3.0, 4.5, 2.1>'
    # print("2 / v =", 2 / v)               # TypeError: unsupported operand type(s) for /: 'int' and 'Vector'
    print("v.magnitude =", v.magnitude)     # v.magnitude = 5.5
    print("v.magnitude_squared =", v.magnitude_squared) # v.magnitude_squared = 30.25
    print("v.normalized =", v.normalized)   # v.normalized = <Vector4: 0.9090909090909091,
                                            # -0.36363636363636365, 0.18181818181818182, 0.09090909090909091>
    print("z.isZero =", z.is_zero)          # z.is_zero = False
    print("q.isZero =", q.is_zero)          # q.is_zero = True


