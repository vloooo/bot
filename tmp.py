class Cat:
    _catCount = 0

    def set_cat_count(self, count):
        self._catCount = count

cat = Cat()
cat.set_cat_count(20)
print(cat._catCount)
