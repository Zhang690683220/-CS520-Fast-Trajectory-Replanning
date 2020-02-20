import math

class MinHeap:
    def __init__(self, list):
        self.list = list

    def parent(self, i):
        return math.floor(i/2)

    def left(self, i):
        return 2*i

    def right(self, i):
        return 2*i+1

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)

        smallest = 0

        if(l < len(self.list) and self.list[l].f() < self.list[i].f()):
            smallest = l
        else:
            smallest = i

        if(r< len(self.list) and self.list[r].f() < self.list[smallest].f()):
            smallest = r

        if smallest != i:
            temp = self.list[i]
            self.list[i] = self.list[smallest]
            self.list[smallest] = temp
            self.min_heapify(smallest)

    def build_min_heap(self):
        for i in range(math.floor(self.list.len()/2), 0, -1):
            self.min_heapify(i)

    def min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1
        else:
            return self.list[0]

    def extract_min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1

        min = self.list[0]
        self.list[0] = self.list[len(self.list)-1]
        self.list.pop()
        self.min_heapify(0)
        return min

    def decrease_key(self, i, k):
        print("debug3")
        if k > self.list[i].f():
            print("new key is larger than current key")
            return 1
        self.list[i].g = k - self.list[i].h

        while(i > 0 and self.list[int(self.parent(i))].f() > self.list[i].f()):
            temp = self.list[i]
            self.list[i] = self.list[int(self.parent(i))]
            self.list[int(self.parent(i))] = temp
            i = int(self.parent(i))

    def insert(self, c):
        key = c.g + c.h
        c.g = float("inf")
        self.list.append(c)
        print("***")
        print(len(self.list)-1)
        self.decrease_key(int(len(self.list)-1), key)


class MinHeap_Large_g:
    def __init__(self, list):
        self.list = list

    def parent(self, i):
        return math.floor(i/2)

    def left(self, i):
        return 2*i

    def right(self, i):
        return 2*i+1

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)

        smallest = 0

        if(l < len(self.list) and self.list[l].f_large_g() < self.list[i].f_large_g()):
            smallest = l
        else:
            smallest = i

        if(r< len(self.list) and self.list[r].f_large_g() < self.list[smallest].f_large_g()):
            smallest = r

        if smallest != i:
            temp = self.list[i]
            self.list[i] = self.list[smallest]
            self.list[smallest] = temp
            self.min_heapify(smallest)

    def build_min_heap(self):
        for i in range(math.floor(self.list.len()/2), 0, -1):
            self.min_heapify(i)

    def min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1
        else:
            return self.list[0]

    def extract_min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1

        min = self.list[0]
        self.list[0] = self.list[len(self.list)-1]
        self.list.pop()
        self.min_heapify(0)
        return min

    def decrease_key(self, i, k):
        print("debug3")
        if k > self.list[i].f_large_g():
            print("new key is larger than current key")
            return 1
        self.list[i].g = (k - 300*self.list[i].h)/299

        while(i > 0 and self.list[int(self.parent(i))].f_large_g() > self.list[i].f_large_g()):
            temp = self.list[i]
            self.list[i] = self.list[int(self.parent(i))]
            self.list[int(self.parent(i))] = temp
            i = int(self.parent(i))

    def insert(self, c):
        key = c.f_large_g()
        c.g = float("inf")
        self.list.append(c)
        print("***")
        print(len(self.list)-1)
        self.decrease_key(int(len(self.list)-1), key)

class MinHeap_Small_g:
    def __init__(self, list):
        self.list = list

    def parent(self, i):
        return math.floor(i/2)

    def left(self, i):
        return 2*i

    def right(self, i):
        return 2*i+1

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)

        smallest = 0

        if(l < len(self.list) and self.list[l].f_small_g() < self.list[i].f_small_g()):
            smallest = l
        else:
            smallest = i

        if(r< len(self.list) and self.list[r].f_small_g() < self.list[smallest].f_small_g()):
            smallest = r

        if smallest != i:
            temp = self.list[i]
            self.list[i] = self.list[smallest]
            self.list[smallest] = temp
            self.min_heapify(smallest)

    def build_min_heap(self):
        for i in range(math.floor(self.list.len()/2), 0, -1):
            self.min_heapify(i)

    def min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1
        else:
            return self.list[0]

    def extract_min(self):
        if len(self.list) < 1:
            print("Sorry, The Heap is Empty!")
            return 1

        min = self.list[0]
        self.list[0] = self.list[len(self.list)-1]
        self.list.pop()
        self.min_heapify(0)
        return min

    def decrease_key(self, i, k):
        print("debug3")
        if k > self.list[i].f_small_g():
            print("new key is larger than current key")
            return 1
        self.list[i].g = (k - 300*self.list[i].h)/301

        while(i > 0 and self.list[int(self.parent(i))].f_small_g() > self.list[i].f_small_g()):
            temp = self.list[i]
            self.list[i] = self.list[int(self.parent(i))]
            self.list[int(self.parent(i))] = temp
            i = int(self.parent(i))

    def insert(self, c):
        key = c.f_small_g()
        c.g = float("inf")
        self.list.append(c)
        print("***")
        print(len(self.list)-1)
        self.decrease_key(int(len(self.list)-1), key)
