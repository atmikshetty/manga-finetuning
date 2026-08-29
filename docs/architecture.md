# Architecture

`src/manga_finetuning` contains small modules with explicit boundaries:

- `panels`: pure bbox conversion, intersection, crop/whiteout, spread layout,
  and resume helpers.
- `panels_cli`: optional Magi/Torch integration and filesystem orchestration.
- `hashing` and `dataset`: dHash deduplication and aspect-preserving PNG prep.
- `captions` and `character`: deterministic style and camera captions.
- `checkpoints` and `evaluation`: safe header parsing, discovery, and GPU grids.
- `manifests`: SHA-256 artifact inventory and sanitized run metadata.

CLI modules import large dependencies only inside execution paths. Shell
wrappers contain Kohya-specific invocation but no machine-specific path. This
keeps core installation, tests, and downstream reuse compact.
