# $Id: Makefile 466 2013-10-04 11:19:49Z coelho $
# compilation d'un compilateur

# export CLASSPATH=/usr/share/java/cup.jar:.

# executables
JAVAC	= javac -Xlint:unchecked
JAVA	= java
JLEX	= tools/jflex/bin/jflex
CUPJAR	= tools/cup/java-cup-11b.jar
JCUP	= java -jar $(CUPJAR)
JFLAGS	= -cp $(CUPJAR):.

# compilation & execution chain
PASCAL  = java $(JFLAGS) Parser
ASM     = ./asm.py
RUN     = ./mach.py

# source files
F.jlex	= $(wildcard *.jlex)
F.cup	= $(wildcard *.cup)

default: help

help:
	@echo "help: this small help"
	@echo "clean: clean generated files"
	@echo "compile: compile the compiler"

clean:
	$(RM) *~ *.class *.java *.i *.o .compile

compile: .compile
.compile: $(F.cup) $(F.jlex)
	$(JCUP) -parser Parser $(F.cup)
	$(JLEX) $(F.jlex)
	$(JAVAC) $(JFLAGS) *.java
	touch $@

# disable all default rules
.SUFFIXES:

# pascal compilation
%.i: %.p; $(PASCAL) < $< > $@
# show generated code
%.y: %.i; cat $<
# assembler
%.o: %.i; $(ASM) < $< > $@
# eXecution
%.x: %.o; $(RUN) $<

F.p	= $(wildcard *.p)
F.i	= $(F.p:%.p=%.i)
$(F.i): .compile
F.o	= $(F.i:%.i=%.o)
$(F.o): $(ASM)
F.x	= $(F.o:%.o=%.x)
$(F.x): $(RUN)

# distribution tar
.PHONY: tgz zip
tgz:
	tar -chvzf pascal.tgz Makefile *.py pascal.* test_00.p README

zip:
	zip compile.zip Makefile *.py pascal.* test_00.p README
