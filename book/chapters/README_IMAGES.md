# Bilder für LaTeX

## Bilder generieren

Um alle Bilder für das LaTeX-Dokument zu generieren, führen Sie aus:

```bash
cd code/chapter01
python generate_images_for_latex.py
```

Dies erstellt alle benötigten PNG-Dateien:
- `random_walk_analysis.png`
- `martingale_transform.png`
- `quadratic_variation.png`
- `optional_stopping.png`
- `boss_challenge_visualization.png`

## Bildpfade in LaTeX

Die Bilder werden in `chapter01.tex` mit folgenden Pfaden eingebunden:

```latex
\includegraphics[width=0.9\textwidth]{../code/chapter01/bildname.png}
```

**Wichtig:** Die Bilder müssen im Verzeichnis `code/chapter01/` sein, damit LaTeX sie findet.

## Alternative: Bilder in book/ Verzeichnis

Falls LaTeX die Bilder nicht findet, können Sie sie auch ins `book/` Verzeichnis kopieren:

```bash
cp code/chapter01/*.png book/
```

Dann ändern Sie die Pfade in `chapter01.tex` zu:

```latex
\includegraphics[width=0.9\textwidth]{bildname.png}
```
