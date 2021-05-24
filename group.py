# this is a module written for groups and sets in terms of mathematics
import copy, sys, matrix, fractions, math, polynomial


def Z(n):
    element = [i for i in range(n)]
    return group(element, mod('+', n))


def U(n):
    element = [i for i in range(1, n) if math.gcd(i, n) == 1]
    return group(element, mod('*', n))


def mod(ope, num):
    def add(x, y, number=num):
        return (x + y) % number

    def mult(x, y, number=num):
        return (x * y) % number

    if ope == '+':
        return add
    elif ope == '*':
        return mult
    else:
        return lambda x, y: None


class PolygonValueError(Exception):
    pass


def D(n):
    if n < 3:
        raise PolygonValueError('a dihedral group Dn usually takes n >= 3')
    return polygon(n)


class Map:
    def __init__(self, G1, G2, func):
        # a Map object takes two groups G1 and G2 and a mapping method,
        # which represents a map from G1 to G2 defined by a function func.
        if not all(isinstance(x, group) for x in [G1, G2]):
            raise ValueError(
                'A map between groups takes two groups to establish, please ensure you use two group object to build.'
            )
        self.G1 = G1
        self.G2 = G2
        self.func = func

    def __str__(self):
        pass

    __repr__ = __str__

    def is_homomorphism(self):
        pass

    def is_isomorphism(self):
        pass

    def is_automorphism(self):
        pass

    def kernel(self):
        pass

    def image(self):
        pass

    def preimage(self):
        pass

    def is_monomorphism(self):
        pass

    def is_epimorphism(self):
        pass

    def is_endomorphism(self):
        pass

    def domain(self):
        pass

    def codomain(self):
        pass

    def is_injective(self):
        pass

    def is_surjective(self):
        pass

    def is_bijective(self):
        pass

    def show_mapping(self):
        # show the mapping details for all elements in G1 and G2
        pass

    def map_to(self, g1):
        if g1 not in self.G1:
            return 'this element is not in the domain group of this map'
        else:
            return self.func(g1)

    def is_function(self):
        # check if actually all elements in G1 maps to some elements in G2,
        # and does not exist any element in G1 that maps to multiple elements
        # in G2 (i.e. cannot be '1 to multiple' for all elements between G1 and G2)
        # the maps element for every element in G1 cannot be greater than 1
        pass

    def is_morphism(self):
        pass


def rotate(pol, direction='ccw', times=1):
    pol.rotate(direction, times)


def vertical_flip(pol, i=1):
    pol.vertical_flip(i)


def horizontal_flip(pol):
    pol.horizontal_flip()


def diagonal(pol, i):
    pol.diagonal(i)


def identity(pol):
    pol.identity()


class polygon:
    def __init__(self, size, info=None):
        self.size = size
        self.info = info
        self.graph = [i for i in range(1, size + 1)]
        self.original = copy.deepcopy(self.graph)

    def __str__(self):
        return (f'{self.info}\n' if self.info != None else
                '') + f'polygon D{self.size} \ncurrent graph \
(counterclockwise): {self.graph} \ngroup element of \
D{self.size}:\n{self.get_element()}'

    __repr__ = __str__

    def __getitem__(self, ind):
        while ind >= len(self.graph):
            ind -= len(self.graph)
        return self.graph[ind]

    def __setitem__(self, ind, x):
        while ind >= len(self.graph):
            ind -= len(self.graph)
        self.graph[ind] = x

    def runs(self, f1, f2):
        pass

    def number(self):
        return 2 * self.size

    def times(self, f, i, param=None, get_return=False):
        if param == None:
            for t in range(i):
                result = f()
        else:
            for t in range(i):
                result = f(*param)
        if get_return:
            return result

    def rotate(self, direction='ccw', times=1):
        # a 1-unit rotation of the polygon, counterclockwise in default,
        # set direction to 'cw' to do clockwise rotation
        # if specified rotate times, rotate as the times matched
        if times > 1:
            for i in range(times):
                self.rotate(direction, 1)
        else:
            if direction == 'ccw':
                self.graph.insert(0, self.graph.pop())
            elif direction == 'cw':
                self.graph.append(self.graph.pop(0))

    def vertical_flip(self, i=1):
        if self.size % 2 != 0:
            self.graph = [self.graph[0]] + self.graph[1:][::-1]
        else:
            if i == 1:
                self.graph = self.graph[:2][::-1] + self.graph[2:][::-1]
            else:
                self.graph.insert(i, self.size + 1)
                self.size += 1
                self.diagonal(self.size)
                self.graph.remove(self.size)
                self.size -= 1

    def horizontal_flip(self):
        if self.size % 2 != 0:
            return 'odd polygon does not have horizontal flip that keeps the shape'
        else:
            if self.size % 3 == 0:
                return 'this polygon does not have horizontal flip that keeps the shape'
            self.runs(self.times(self.rotate, self.size // 2),
                      self.vertical_flip())

    def diagonal(self, i):
        # if the polygon is an odd polygon, it has n diagonals where n is the size;
        # if the polygon is an even polygon, it has n/2 diagonals where n is the size.
        # i represents one of the point number in the polygon like 1,2,3,4,5,6,
        # if i is a valid point in this polygon, flip the polygon with the center
        # of this point.
        if i not in range(1, self.size + 1):
            return 'this diagonal does not exist in this polygon'
        else:
            exchange = 0
            step = 1
            i = self.graph.index(i)
            MAX = self.size - 1 if self.size % 2 != 0 else self.size - 2
            while exchange != MAX:
                self[i - step], self[i + step] = self[i + step], self[i - step]
                exchange += 2
                step += 1

    def identity(self):
        pass

    def get_element(self):
        # note that an even polygon with size divided by 4 has horizontal flip,
        # with size divided by 3 does not.
        size = self.size
        angle = (self.size - 2) * 180 / self.size
        angle = int(angle) if angle.is_integer() else fractions.Fraction(
            angle).limit_denominator()
        rotate_items = [f'R{angle*i}' for i in range(self.size)]
        if self.size % 2 != 0:
            flip_items = ['V'] + [f'D{i}' for i in range(2, self.size + 1)]
        else:
            if self.size % 3 == 0:
                flip_items = [
                    f'V{i}' for i in range(1, (self.size // 2) + 1)
                ] + [f'D{i}' for i in range(1, (self.size // 2) + 1)]
            else:
                flip_items = ([f'V{i}' for i in range(1, (self.size // 2))]
                              if self.size != 4 else ['V']) + ['H'] + [
                                  f'D{i}'
                                  for i in range(1, (self.size // 2) + 1)
                              ]
        items = rotate_items + flip_items
        return items

    def get_element_functions(self):
        size = self.size
        angle = (self.size - 2) * 180 / self.size
        angle = int(angle) if angle.is_integer() else fractions.Fraction(
            angle).limit_denominator()
        rotate_items = [[identity]] + [[rotate, 'ccw', t]
                                       for t in range(1, size)]
        if self.size % 2 != 0:
            flip_items = [[vertical_flip, 1]
                          ] + [[diagonal, i] for i in range(2, self.size + 1)]
        else:
            if self.size % 3 == 0:
                flip_items = [[vertical_flip, i]
                              for i in range(1, (self.size // 2) + 1)
                              ] + [[diagonal, i]
                                   for i in range(1, (self.size // 2) + 1)]
            else:
                flip_items = ([[vertical_flip, i]
                               for i in range(1, (self.size // 2))]
                              if self.size != 4 else [[vertical_flip, 1]]) + [[
                                  horizontal_flip
                              ]] + [[diagonal, i]
                                    for i in range(1, (self.size // 2) + 1)]
        items = rotate_items + flip_items
        return items

    def reset(self):
        self.graph = [i for i in range(1, self.size + 1)]

    def get_equivalent(self):
        functions = self.get_element_functions()
        funcname = self.get_element()
        temp = polygon(self.size)
        equivalent = dict()
        print(functions)
        for i in range(len(functions)):
            func = functions[i][0]
            arg = [temp] + functions[i][1:]
            func(*arg)
            equivalent[repr(temp.graph)] = funcname[i]
            temp.reset()
        return equivalent


class permutation:
    def __init__(self, pdict):
        self.pdict = pdict

    def size(self):
        return max(list(self.pdict.keys()))

    def get_next(self, g):
        if g not in self.pdict:
            return 'this element is not in this permutation'
        else:
            return self.pdict[g]

    def get_cycles(self):
        result = []
        checked = []
        for i in self.pdict.keys():
            if i not in checked:
                checked.append(i)
                now = i
                temp = [i]
                while self.pdict[now] != i:
                    if self.pdict[now] == now:
                        return 'this is not a valid permutation'
                    temp.append(self.pdict[now])
                    checked.append(self.pdict[now])
                    now = self.pdict[now]
                result.append(temp)
        return result

    def twocycles(self):
        result = self.get_cycles()
        two = []
        for t in range(len(result)):
            cycle = result[t]
            for h in range(1, len(cycle)):
                two.append((cycle[0], cycle[h]))
        return two

    def cycle_type(self):
        cycles = self.get_cycles()
        result = tuple([len(i) for i in cycles])
        return result

    def parity(self):
        if len(self.twocycles()) % 2 == 0:
            return 'even'
        else:
            return 'odd'

    def __eq__(self, other):
        return self.pdict == other.pdict

    def __pow__(self, number):
        temp = copy.deepcopy(self)
        for i in range(number - 1):
            temp *= self
        return temp

    def __mul__(self, other):
        if not isinstance(other, permutation):
            return 'permutation combination is valid between permutations'
        else:
            newdict = {
                i: other.pdict[self.pdict[i]]
                for i in self.pdict.keys()
            }
            return copy.deepcopy(permutation(newdict))

    def __str__(self):
        result = ''
        checked = []
        for i in self.pdict.keys():
            if i not in checked:
                checked.append(i)
                if self.pdict[i] != i:
                    now = i
                    temp = [i]
                    while self.pdict[now] != i:
                        if self.pdict[now] == now:
                            return 'this is not a valid permutation'
                        temp.append(self.pdict[now])
                        checked.append(self.pdict[now])
                        now = self.pdict[now]
                    result += str(tuple(temp))
        if result == '':
            return '(1)'
        return result

    __repr__ = __str__


def per(*cycles):
    newdict = {}
    for i in range(len(cycles)):
        cycle = cycles[i]
        for j in range(len(cycle)):
            if j == len(cycle) - 1:
                newdict[cycle[j]] = cycle[0]
            else:
                newdict[cycle[j]] = cycle[j + 1]
    return permutation(newdict)


def empty():
    pass


def composition(f1, f2, diffarg=False):
    # take some functions and run in the order of arguments.
    # default requires that f1 and f2 have same number of arguments,
    # or at least f2's return fits the number of f1's parameters.
    # f1 and f2 can be functions with no return values, or no input values,
    # but both of them should be in one kind.
    # if f1 and f2 not satisfy above requirements, you can set diffarg = True,
    # then ensure f1 and f2 both are a list with function name as the first element
    # and all of the parameters as the remaining elements.
    if diffarg:
        # run the functions from inner to outer (i.e. first run f2(x) and then run f1(x))
        # and return the return values of f2 and f1 if not both of them are None
        result2 = f2[0](*f2[1:])
        result1 = f1[0](*f1[1:])
        if any(x != None for x in [result1, result2]):
            return result2, result1
    else:
        # with same number of function arguments, this program can return a composite function
        # with f1 and f2
        try:
            q = lambda x: f1(f2(x))
            h = 'a'
            h = q(h)
            return q
        except:
            try:
                f2()
                f1()
                #return empty
            except:

                def combine(*x):
                    f2(*x)
                    f1(*x)

                return combine


class Set:
    def __init__(self, conditions=None, elements=None, description=None):
        if conditions is not None:
            try:
                x = len(conditions)
            except:
                conditions = [conditions]
        self.conditions = conditions
        self.elements = elements
        self.description = description

    def cat(self, a, b):
        if b == 'linebreak':
            return a + '\n'
        return a + b

    def __contains__(self, x):
        return all(cond(x) for cond in self.conditions
                   ) if self.conditions is not None else x in self.elements

    def __repr__(self):
        return f"{'description: ' + self.cat(self.description, 'linebreak') if self.description is not None else ''}elements: {'infinite' if self.elements is None else self.elements}"

    def __getitem__(self, ind):
        if self.elements is None:
            print('this set has infinite elements')
        else:
            return self.elements[ind]

    def __setitem__(self, ind, value):
        if self.elements is None:
            print('this set has infinite elements')
        else:
            self.elements[ind] = value

    def __delitem__(self, ind):
        if self.elements is None:
            print('this set has infinite elements')
        else:
            del self.elements[ind]

    def testin(self, alist):
        return [i in self for i in alist]

    def pickin(self, alist):
        return [i for i in alist if i in self]

    def picknotin(self, alist):
        return [i for i in alist if i not in self]

    def splitin(self, alist):
        return [[i for i in alist if i in self],
                [i for i in alist if i not in self]]


class group:
    ''' Some Important Instructions of the Class Group
    
        1. About group intialization
       
            sets the elements in the group from a set together with a binary operation,
            the identity can be specially indicated. You can also set the general form
            of the elements in the group and the inverse form of them.
            The operation could be a function, in which to perform the steps
            you want to deal with elements in the group.
            And elements can also be a list of functions or any class objects.
            
        2. Some Standard Operators
        
            Below are some special cases that you can simplify the operation:
            if operation is '+' or 'add': translate as add(x, y)
            if operation is '-' or 'subtract': translate as sub(x, y)
            if operation is '*' or 'mult': translate as mult(x, y)
            if operation is '/' or 'divide': translate as divide(x, y)
            if you want operation to be like '+ mod 8' or '* mod 17',
            then just set the operation as 'mod('+', 8)' or 'mod('*', 17)'.
            P.S. actually, lambda is a easy way to set the operation as what you
            want to do, for example: set the operation as "lambda x, y: x*y"
            means multiply each two elements in the group, and "lambda x, y: x+y"
            is for additive case. For relatively simple operations, using lambda will be a chill.
        
        3. Composition Cases
        
            for permutations or D3 for example, you can set the operation as 'composition',
            and make every element of the group is a function (in dihedral group case)
            or a permutation object (in permutation group case).
            and function elements is in much more cases of groups with compositions,
            you can design your own functions that dealing with your group and set them as elements
            permutation is a class implemented for permutation groups together with their calculations
            and evaluations. For Dihedral groups Dn, you can set obj = D(n), here I provide
            a function D(n) which returns a polygon object Dn with group elements (for more
            information, please check the class description of polygon in this file),
            and the element of the group will be automatically set to the group elements of Dn.
            When the program receives these functions, it will check the first carrying variables
            of each function, (so you should keep every funtion with a same first variable)
            and generate a dynamic polygon object which data can be changed during every operation
            from function elements. in D4 you can also add H(4) which stands for horizontal flip,
            and in D5, D6, ..., they are all following the same roles of implementation.
            
        4. General Form and Inverse Form
        
            general form and inverse form is not required as you set the element to be something,
            but if you want to set conditions that if an element is a valid element inside the
            group, you can make a function that returns True if the element satisfies
            some conditions else return False, for multiple conditions,
            you can either make them all inside a function or make
            a list contains all of the functions that checks a condition for each function.
            Note that if you keep the element as None (if you do not set element, the default is None),
            a general form is required, because in this case this group is considered to be an infinite group.
        
        5. Add an element to the group
        
            To add an element to a group, the program will first check if the element
            is valid, otherwise return warning; cannot add this element because it does not
            satisfies the conditions of the group. To get inverse of each element in the group,
            just simply go through every element in the group, do the operation and see if the
            result is equal to the identity.
        
        6. Object in the group
        
            with special kinds of group, sometimes an object is required, as an example, for dihedral groups,
            when the elements are settled for Dn, the program will set the obj to a polygon object.
            you can also set object by yourself fitting with elements and group operations.
            you can also add some infomartion for this map that describes the types and
            attributes of this group, and how this group works, etc.
        
        7. Infinite Group Case
            For infinite groups, which means the number of elements are infinite,
            you can leave the elment as None, but in this case this class requires
            a general form which holds all of the conditions that the elements
            in this group must satisfy. The general form could be a function or
            a list of functions that returns True or False.
            When the program want to show if the group is finite or infinite,
            it will check if the type of elements is None, if so then this group
            is infinite, otherwise is finite.
            there is a method called get_element(m, n) in this class that could
            take the element subset from a range which satisfies the conditions of
            the group, which is only applicable for infinite group, which means
            the elements of the group should be None. So at any time you want to
            change a finite group to an infinite group, just set the element to None,
            and then make sure you have set the general form for this group.
            
        8. Inverse
        
            Inverse is a function which is the reverse-form of operation function.
            If this is an infinite group (i.e. the element is a function or None),
            inverse should be settled, otherwise when use inverse(g) to find an inverse
            of an element g in the group, the program will return a warning.
        
        '''
    def __init__(self,
                 element=None,
                 operation=None,
                 identity=None,
                 general=None,
                 inverses=None,
                 obj=None,
                 info=None):
        ''' set up a group project with element, group operation, identity, general form(functions that have some conditions to check if a given element
            belongs to the group or in other words, is valid to be in the group), inverse form (a function to calculate the inverse of an element in the group),
            object if needed, information or description of the group, if any one of these is provided. To set up a group project, at least a group operation is required.'''
        self.isgroup = False
        self.obj = obj
        if isinstance(obj, polygon):
            element = {
                self.obj.get_element()[i]: self.obj.get_element_functions()[i]
                for i in range(self.obj.number())
            }
            operation = composition
            general = lambda x: x in self.element
        self.element = element
        # you must at least have an operation
        if operation == None:
            raise ValueError('missing a group operation')
        # there is a special kind of group operation called composition, which is
        # take two elements which both make an action, say a o b, and do in the order of
        # b, a, which means do the inner element first and then the outer.
        # Let think if you take two functions f(x) and g(x), and then f(x) o g(x)
        # = f(g(x)), which is firstly perform g(x) to an object and then perform f(x).
        if operation in ['o', 'composition']:
            # composition is a function which can relatively-flexibly do the composition
            # of two elements (here the elements will be functions) of the group with
            # composition as the group operation. For more details, please see the
            # comments of the function composition.
            self.operation = composition
        else:
            # This program will provide with some basic group operation that you can
            # using an abbreviation to set them, including additive group,
            # multiplicative group, and subtraction, division, add modulo n,
            # multiply modulo n (for modulo n, use "mod('+', n) or mod('*', n)"
            # with add modulo n and multiply modulo n respectively)
            if operation not in ['+', '-', '*', '/']:
                self.operation = operation
            else:
                if operation == '+':
                    self.operation = lambda x, y: x + y
                elif operation == '-':
                    self.operation = lambda x, y: x - y
                elif operation == '*':
                    self.operation = lambda x, y: x * y
                elif operation == '/':
                    self.operation = lambda x, y: (
                        x / y) if y != 0 else 'does not exist'
        self.identity = identity
        # you don't need a general form if your group is a finite group (if you do not
        # set the element to be anything, the element of the group will be set to None
        # as default, the group will be considered as an infinite group only if the element
        # is None) If you choose your group to be infinite (you just leave the element unsettled),
        # a general form is required to build up a group object.
        if general == None:
            if self.element == None:
                raise ValueError(
                    'for infinite group initialization, missing a general form'
                )
            else:
                self.general = general
        else:
            # general form must be either a function of a list of functions,
            # where each function only returns only True or False to judge
            #  whether an element satisfies one or more of the conditions
            # to be in the group.
            if callable(general):
                self.general = [general]
            elif isinstance(general, list):
                if all(callable(x) for x in general):
                    self.general = general
                else:
                    raise ValueError(
                        'some of the elements in the list is not a function or not callable'
                    )
            else:
                raise ValueError(
                    'general form should a function or a list of functions')
        self.inverses = inverses
        self.info = info

    def __str__(self):
        return f'group elements: {set(self.element) if self.is_finite() else "infinite"}\n\
group operation: {self.operation.__name__}\n\
group identity: {"not indicated" if self.identity == None else self.identity}\n\
general form: {"not indicated" if self.general == None else self.general}\n\
inverse form: {"not indicated" if self.inverses == None else self.inverses}\n'

    __repr__ = __str__

    def __contains__(self, g):
        if self.is_finite():
            return g in self.element
        else:
            return all(x(g) is True for x in self.general)

    def e(self):
        return self.identity

    def all_inverse(self, subset=None):
        # return the sets of inverses of each element in the group following
        # the implemented inverse form in the group, if no inverse form implemented,
        # use the group operation to find them
        if self.is_finite():
            return {i: self.inverse(i) for i in self.element}
        else:
            if subset == None:
                return 'since this is an infinite group, an element subset is required.'
            return {i: self.inverse(i) for i in subset}

    def __setattr__(self, name, value):
        if name in self.__dict__:
            if name == 'general':
                if self.general == None:
                    if callable(value):
                        self.__dict__[name] = [value]
                    elif isinstance(value, list):
                        self.__dict__[name] = value
                    else:
                        raise ValueError(
                            'must assign a function or a list of functions to general form'
                        )
            else:
                self.__dict__[name] = value
        else:
            self.__dict__[name] = value

    def inverse(self, g):
        if g not in self:
            return 'this element is not in this group'
        # return the inverse of g in the group
        if self.is_finite():
            if self.inverses == None:
                if self.identity == None:
                    return 'the identity is not yet settled'
                for i in self.element:
                    if self.operation(g, i) == self.identity:
                        return i
                return 'no inverse is found in given group elements, so this is not a valid group'
            else:
                return self.inverses(g)
        else:
            if self.inverses == None:
                return 'since this is an infinite group, an inverse function is needed'
            else:
                return self.inverses(g)

    def all_element(self):
        if not self.is_finite():
            return 'this is an infinite group which means its elements are\
infinite, you can use get_element(m, n) to get an elements subset\
from m to n.'

        else:
            return self.element

    def get_operation(self):
        return self.operation

    def get_general(self):
        return self.general

    def find_identity(self, g=None):
        # if the group is finite, firstly checked if the group has an inverse
        # function implemented, if so, pick the first element in the group
        # and make an operation between this element and its inverse and then
        # get the identity, and then implemented, return the identity.
        # if not, then go through all elements in the group and check
        # if there is an element e satisfies ge = eg = g for all g in the group.
        # once this element is found, set and return the identity.
        # if this group is an infinite group, an element is required in the parameters,
        # if this element is not in the group, then return warning;
        # else check if the group has inverse function, if not, return warning;
        # if so, use this element to make an operation with its inverse,
        # and then get the identity, set and return the identity.
        # you can also set an identity manually by G.identity = e
        if self.is_finite():
            if self.inverses != None:
                e = self.operation(element[0], self.inverses(element[0]))
                self.identity = e
                return e
            else:
                for i in self.element:
                    if all(
                            self.operation(i, x) == self.operation(x, i) == x
                            for x in self.element):
                        self.identity = i
                        return i
        else:
            if g == None:
                return 'since this is an infinite group, an element belongs to this group is required'
            else:
                if g not in self:
                    return 'this element does not belong to this group'
                else:
                    if self.inverses == None:
                        return 'since this is an infinite group, an inverse function is needed'
                    e = self.operation(g, self.inverses(g))
                    self.identity = e
                    return e

    def find_inverse(self, g):
        pass

    def order(self, g=None, isgroup=False):
        # return the order of the group if not set an element g,
        # return the order of the element g in the group if an element g is set.
        if g == None:
            if self.is_finite():
                return len(self.element)
            else:
                return 'this is an infinite group, so the order of the group is infinity'
        else:
            if self.is_finite():
                if g not in self.element:
                    return 'this element does not belong to this group'
                if not self.is_group():
                    return 'this is not a group, so the order of an element is not meaningful'
            else:
                if not all(x(g) is True for x in self.general):
                    return 'this element g does not match the conditions of this group'
                if isgroup == False:
                    return 'this is an infinite group which is not declared to be a group, you can add isgroup = True to this function'
                else:
                    self.is_group(True)
            if self.identity == None:
                return 'this group has no identity yet, please set the identity\
by using G.identity = e where G is the name of your group and e is\
the identity element you want to set, or if you have a general form\
or element function in this group, use find_identity() to find the identity,\
once it is found, the identity of this group will be automatically settled.'

            temp = copy.deepcopy(g)
            result = 1
            while temp != self.identity:
                temp = self.operation(temp, g)
                result += 1
            return result

    def is_abelian(self):
        pass

    def is_cyclic(self):
        pass

    def is_group(self, isgroup=False):
        '''check if this is a group
        In is_group function the program will check if:
        1. the group is non-empty (length of element != 0);
        2. the group has closure (x*y in element for all x, y in element, including self);
        3. the group has an identity (can find an element e such that ex = xe = x)
        4. all elements has inverses (can find an element y for every element x such that x*y = e)
        5. the group has associativity ((x*y)*z == x*(y*z) for every element x, y, z, including self)
        if all of the 5 conditions are satisfied, return True, otherwise return False.
        Currently only works for finite groups, for infinite groups (which means the element is set to None),
        sometimes it is hard to show the closure of the group (while for finite group it is easy),
        and actually for elements which are polynomials, matrices, permuations, polygons, I have written
        some classes and packages to deal with these cases, so for infinite groups with elements of these
        types you can use this function too. If not, and you still want to indicate this is a group,
        just add True in the function parameter. This parameter will only
        be checked when the group is an infinite group. Then this group will have a new attribute
        declaring that it is a group.
        '''
        if not self.is_finite():
            if self.identity == None:
                # this infinite "group" has no identity yet, so this is not a group
                return False
            if self.inverses == None:
                # this infinite "group" has no inverses function yet, so this is not a group
                return False
            if isgroup == True:
                self.isgroup = True
            else:
                return 'this function currently only works for finite groups, if you want to set this group\
                to be used as a group, just add a True in this function\'s parameter'

        else:
            if len(self.element) == 0:
                # the group cannot be empty
                return False
            whole = [(i, j) for i in self.element for j in self.element]
            # this group should has closure under the operation
            if any(self.operation(x[0], x[1]) not in self for x in whole):
                return False
            asso = [(i, j, k) for i in self.element for j in self.element
                    for k in self.element]
            # this group should has associativity for all elements
            if any(
                    self.operation(self.operation(x[0], x[1]), x[2]) !=
                    self.operation(x[0], self.operation(x[1], x[2]))
                    for x in asso):
                return False
            if self.identity == None:
                self.find_identity()
                # this infinite "group" has no identity yet, so this is not a group
                if self.identity == None:
                    return False
            for t in self.element:
                found = False
                if any(
                        self.operation(t, x) == self.operation(x, t) ==
                        self.identity for x in self.element):
                    found = True
                # every element in the group should has an inverse
                if found == False:
                    return False
            return True

    def is_isomorphic(self, other):
        pass

    def subgroup(self):
        pass

    def quotient_group(self):
        pass

    def normal_group(self):
        pass

    def is_additive(self):
        return True if self.operation == '+' else False

    def is_mult(self):
        return True if self.operation == '*' else False

    def is_finite(self):
        if self.element != None:
            return True
        else:
            return False

    def __getitem__(self, ind):
        if self.is_finite():
            return self.element[ind]
        else:
            return 'this is an infinite group'

    def __delitem__(self, g):
        if g in self:
            if self.is_finite():
                self.element.remove(g)
            else:
                print('this is an infinite group')

    def __setitem__(self, ind, g):
        if self.is_finite():
            self.element[ind] = g
        else:
            print('this is an infinite group')

    def perform(self, g, h):
        if any(x not in self for x in [g, h]):
            return 'some element is not in g'
        if not isinstance(self.obj, polygon):
            if self.operation == composition:
                result = self.operation(g, h)
                if result != None:
                    return result
            else:
                return self.operation(g, h)
        else:
            param1 = self.element[h]
            param2 = self.element[g]
            f1 = param1[0]
            f2 = param2[0]
            arg1 = [self.obj] + param1[1:]
            arg2 = [self.obj] + param2[1:]
            f1(*arg1)
            f2(*arg2)

    def add(self, g):
        if self.general == None:
            return 'this group does not have a general form to check if an element is valid in this group yet'
        if any(x(g) is False for x in self.general):
            return 'this element does not meet the requirements for this group'
        else:
            if self.is_finite():
                self.element.append(g)
            else:
                return 'this group is an infinite group'

    def get_obj(self):
        return self.obj if self.obj != None else 'this group has no treating object'

    def get_info(self):
        return self.info if self.info != None else 'this group has no descriptions yet'

    def get_element(self, m=None, n=None, condition=None):
        result = []
        if self.is_finite():
            return 'this group is not an infinite group, which means you cannot take elements subset from it'
        else:
            if m == None and n == None:
                if condition == None:
                    return 'since the range is not settled, you should set a condition as a\
                    list/set/dictionary which to demonstrate the more abstract range.'

                else:
                    if any(
                            isinstance(condition, x)
                            for x in [list, set, dict]):
                        for k in condition:
                            if all(x(k) is True for x in self.general):
                                result.append(k)
                    else:
                        return 'please ensure the condition is a list/set/dictionary'
            else:
                for i in range(m, n):
                    if all(x(i) is True for x in self.general):
                        result.append(i)
            return result

    def cayley_table(self, subset=None):
        if self.is_finite():
            if subset != None:
                element = subset
            else:
                element = self.element
        else:
            if subset == None:
                return 'since this group is an infinite group, an element subset is needed.'
            element = subset
        table = matrix.build(len(element) + 1, len(element) + 1, 0)
        table.change_row(1, [0] + [f'{i}' for i in element])
        table.change_column(1, [0] + [f'{i}|' for i in element])
        table.row[0][0] = 'xx'
        if not isinstance(self.obj, polygon):
            for i in range(1, table.row_number):
                for j in range(1, table.column_number):
                    table.row[i][j] = self.perform(element[i - 1],
                                                   element[j - 1])
        else:
            equivalent = self.obj.get_equivalent()
            temp = group(obj=D(self.obj.size))
            for i in range(1, table.row_number):
                for j in range(1, table.column_number):
                    temp.perform(
                        list(element.keys())[i - 1],
                        list(element.keys())[j - 1])
                    table.row[i][j] = equivalent[repr(temp.obj.graph)]
                    temp.obj.reset()
        return table

    def rep(self):
        '''Choose an abstract element from a class object which represents
        the general form of the group, this function is a bit awkward to understand
        what had how it is doing, here I will give some examples.
        Now let's say we have a group GL(2,R) (this is a group with 2x2 matrices and
        every matrix's determinant is not equal to 0). This group is of course
        an infinite group, and it is easy to set conditions for this group,
        namely, a matrix with both of its row number and column number is 2 and
        has a non-zero determinant. But when we are trying to prove it is a group,
        some of the conditions is hard to justify without setting a representative
        element of this group beforehand. Usually, for all cases of an infinite group,
        setting a representative element requires a polynomial object that labels
        with the attributes of the elements in the group, and satisfies the conditions
        of the group. For the group GL(2,R), this function will return a 2x2 matrix
        (we can call it A) with elements a, b, c, d (a,b in the first row and c,d in the second row)
        and det(A) = ad - bc != 0, here we will be using inequality class which is also
        written by me in the polynomial module (and this module has an equation parameter too)
        When we use is_group function to prove that GL(2,R) is a group, or using
        is_cyclic, is_abelian and so on to prove some groups is of some special kinds
        of groups, this function will be used very frequently.
        
        '''
        pass
