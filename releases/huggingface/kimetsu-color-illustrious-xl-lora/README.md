---
license: other
base_model: OnomaAIResearch/Illustrious-xl-early-release-v0
base_model_relation: adapter
library_name: diffusers
pipeline_tag: text-to-image
instance_prompt: dsmanga
tags:
  - stable-diffusion-xl
  - diffusers
  - lora
  - text-to-image
  - manga
  - anime
  - color
  - style
  - copyrighted-training-data
---

# Kimetsu Color Illustrious XL LoRA

This SDXL LoRA adapts Illustrious XL toward color manga rendering. It is
provided only for personal, research, and educational use.

## Artifact

- Repository: `sleephashira/kimetsu-color-illustrious-xl-lora`
- File: `kimetsu_color_lora.safetensors`
- Size: `228473556` bytes
- SHA-256: `dbfa9f883383b0b3ac09ecf6366be3433b2909513f5ab67fdb03cfadcbf8e6cf`
- Base model: `OnomaAIResearch/Illustrious-xl-early-release-v0`
- Trigger: `dsmanga`

## Training Summary

The training set contained **1,264 cleaned, extracted, copyrighted Demon
Slayer color panels**. This is the corrected panel count; earlier documentation
that reported a different count should not be used. Checkpoint step 1800 was
selected for this release.

## Tested Usage

Load the adapter with the exact filename and put `dsmanga` near the start of the
prompt. Use explicit color tags and put `monochrome, greyscale` in the negative
prompt when a color result is wanted. A practical tested starting point is LoRA
scale 0.85, Euler ancestral sampling, 30 steps, CFG 6.5, and 1024x1280.

```python
pipe.load_lora_weights(
    "sleephashira/kimetsu-color-illustrious-xl-lora",
    weight_name="kimetsu_color_lora.safetensors",
)
pipe.fuse_lora(lora_scale=0.85)

image = pipe(
    "dsmanga, vibrant colors, 1boy, holding katana, forest, sunlight",
    negative_prompt="monochrome, greyscale, photorealistic, blurry, text",
    width=1024,
    height=1280,
    num_inference_steps=30,
    guidance_scale=6.5,
).images[0]
```

Results vary by prompt, seed, scheduler, resolution, and adapter strength. The
model can reproduce biases, visual motifs, or character associations from its
training set and may produce malformed anatomy, text, or panel details.

## Terms, Rights, and Disclaimer

This adapter was trained on extracted Demon Slayer color panels. The source
artwork is copyrighted and was not licensed by its copyright holders for this
training or release. This is an unofficial release with no affiliation with or
endorsement by the authors, artists, publishers, rights holders, or upstream
model authors.

**Permitted scope:** personal, research, and educational use only.

**Prohibited scope:** commercial or monetized use, advertising, paid services,
resale, and any other revenue-generating use are prohibited.

`license: other` identifies non-standard model terms. These terms are a custom
use restriction, not an OSI-approved open-source license. No rights are granted
to any source artwork, characters, names, trademarks, datasets, or other
third-party material. Downloading the weights does not supply permission from
any copyright, trademark, publicity-right, or other rights holder.

The downloader and user are solely responsible for determining legality,
obtaining all necessary permissions, complying with local law, and following
all applicable platform and upstream terms. The software and artifact are
provided as-is, without warranties of any kind. To the maximum extent permitted
by law, the maintainer excludes liability for use, outputs, claims, damages, or
other consequences arising from the artifact.

This disclaimer and the custom restriction do not override applicable law or
upstream licenses. All applicable upstream base-model terms also govern. Review
the [Illustrious XL model card](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0),
its [terms of use](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0/blob/main/TERM_OF_USE),
and the linked [Fair AI Public License 1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
before downloading or using this adapter.
