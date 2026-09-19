# avanness213.github.io

Personal site and resume for Alexander Van Ness. Static Astro site deployed to GitHub Pages.

Run `npm install && npm run dev` to preview. Push to `main` to deploy.

## Editing

- **Page content** lives in `src/pages/index.astro`.
- **Resume PDF** is generated. Edit `.claude/skills/resume-pdf/resume_content.py`, then run
  `python .claude/skills/resume-pdf/build_resume.py` and `python .claude/skills/resume-pdf/verify_layout.py`.
- **Triptych photo**: replace `public/images/triptych.png` with a 3:2 image (three vertical panels
  side by side, roughly 1536×1024 or larger). Keep the file name and the site picks it up.
- **Rebuilding the triptych** from new photos: `python .claude/image-generation/composite_triptych.py LEFT MID RIGHT` (add `--stitch` for panels that are already graded 1:2 portraits).
