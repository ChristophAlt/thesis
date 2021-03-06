all: thesis.pdf

clean:
	rm -f *~ *.bak *.bbl *.aux *.log *.dvi *.ps *.blg *.out *.lof *.lot chapters/*.aux img/*.eps

thesis.pdf: thesis.ps
	ps2pdf thesis.ps thesis.pdf

thesis.ps: thesis.dvi
	dvips -t a4 -o thesis.ps thesis.dvi 

thesis.dvi: eps_conversion thesis.bib *.tex chapters/*.tex# img/*.eps 
	-latex thesis.tex
	bibtex thesis
	latex thesis.tex
	latex thesis.tex

eps_conversion:
	for image in img/*.png ; do \
        	convert $$image $${image%%.*}.eps ; \
	done
