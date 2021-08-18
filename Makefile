src=src/render.c
obj=bin/render.o
lib=bin/render.so

$(lib): $(src)
	gcc -c $(src) -o $(obj) -fPIC
	gcc -shared -o $(lib) $(obj)

.PHONY: clean

clean:
	rm bin/*.o
