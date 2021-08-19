src=src/render.c
obj=bin/render.o
lib=bin/render.so
flags= -fopenmp 

$(lib): $(src)
	gcc -c $(src) -o $(obj) -fPIC $(flags)
	gcc -shared -o $(lib) $(obj)  $(flags)

.PHONY: clean
clean:
	rm bin/*.o
