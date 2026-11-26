# Taxi Booking Report (LaTeX)

## Build PDF

From project root:

```bash
cd report
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If you have `latexmk`:

```bash
cd report
latexmk -pdf main.tex
```

## Notes

- Section order follows the required project report structure.
- Missing images are shown as placeholder boxes so compile does not fail.
- Add your final diagrams/screenshots in `report/assets/`.
