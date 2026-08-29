# Migration Scope

This repository is a curated refactor of reusable finetuning behavior from a
larger private working project. Logic was reorganized into a Python package,
covered with generated-fixture tests, and made path/configuration driven.

Included: panel bbox parsing and extraction, text whiteout, normalized spread
layouts and resume helpers, dHash dataset preparation, trigger processing,
character camera captions and validation, Kohya style/character wrappers,
v-pred checkpoint evaluation, and artifact/run manifests.

Excluded: web applications, raw manga, image acquisition and scraping,
credentials, dialogue and lettering, page composition, general image
generation, galleries, checkpoints, weights, archives, logs, agent files, and
all derived copyrighted datasets. No source artifact was copied into this
repository.
