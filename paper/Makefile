# make -C paper  -> regenerates tables from experiments/results and builds both PDFs
all: tables empirical tooldemo
tables:
	python3 scripts/make_paper_tables.py && python3 scripts/make_paper_extras.py && python3 scripts/make_figures.py
empirical tooldemo:
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	cd empirical && latexmk -C; cd tooldemo && latexmk -C
.PHONY: all tables empirical tooldemo clean
