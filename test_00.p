def fct(a)
print 3;
endf

def fcta(a)
gl b := 4;
b := 8;
print a + b;
endf

fct(3);
fcta(7);
print gl b;