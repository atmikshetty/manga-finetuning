---
license: other
base_model: Laxhar/noobai-XL-Vpred-1.0
base_model_relation: adapter
library_name: diffusers
pipeline_tag: text-to-image
instance_prompt: reichar
tags:
  - stable-diffusion-xl
  - diffusers
  - lora
  - text-to-image
  - v-prediction
  - character
  - synthetic-data
  - copyrighted-derived-lineage
---

# Rei Character NoobAI XL V-Pred LoRA

This SDXL character LoRA is an unofficial release with no affiliation with or
endorsement by any authors, artists, publishers, rights holders, or upstream
model authors. It is provided only for personal, research, and educational use.

![Generated example](examples/showcase.png)

## Artifact

- Repository: `sleephashira/rei-character-noobai-xl-vpred-lora`
- File: `reichar_noobai_vpred.safetensors`
- Size: `456487828` bytes
- SHA-256: `e7eddcd155cf34ea53c85160f8cdc2aa2e1902d087abab113965beb0915196c2`
- Base model: `Laxhar/noobai-XL-Vpred-1.0`
- Trigger: `reichar`

## Training Summary and Lineage

The adapter was trained on 28 synthetic images of Rei, an original project
character. Checkpoint step 1800 was selected for this release.

The 28 images were generated and restyled with the copyrighted-derived
`multi3_lora.safetensors` adapter. That adapter was trained on 600 monochrome
Bleach panels, 600 official-color Bleach panels, and 600 JoJo panels. Those
source panels are copyrighted and were not licensed by their copyright holders
for that training. Synthetic generation does not erase this provenance or
establish rights in any inherited visual material.

## Tested Usage

NoobAI XL V-Pred requires **Euler**, `prediction_type="v_prediction"`,
`rescale_betas_zero_snr=True`, `guidance_rescale=0.7`, and CFG 4-5. Other
samplers or epsilon-prediction settings do not provide the intended inference
behavior. Put `reichar` near the start of the prompt and describe clothing,
camera, expression, and scene explicitly. A tested starting point is 28 steps,
CFG 5, and character LoRA scale 0.7 at approximately 1024x1024 total pixel area.

```python
from diffusers import EulerDiscreteScheduler

pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config,
    prediction_type="v_prediction",
    rescale_betas_zero_snr=True,
)
pipe.load_lora_weights(
    "sleephashira/rei-character-noobai-xl-vpred-lora",
    weight_name="reichar_noobai_vpred.safetensors",
)
pipe.fuse_lora(lora_scale=0.7)

image = pipe(
    "reichar, 1boy, black hair, grey eyes, grey trench coat, portrait",
    width=832,
    height=1216,
    num_inference_steps=28,
    guidance_scale=5.0,
    guidance_rescale=0.7,
).images[0]
```

Results vary by prompt, seed, resolution, and adapter strength. The small
synthetic dataset can overfit poses, clothing, facial traits, or backgrounds and
can produce malformed anatomy or inconsistent character details.

## Terms, Rights, and Disclaimer

Rei is an original project character, and this adapter was trained on 28
synthetic images rather than directly extracted manga panels. However, those
images were generated and restyled using the `multi3` adapter, which was trained
on copyrighted, unlicensed Bleach and JoJo panels. No copyright holder licensed
or endorsed that source training, synthetic dataset, or this release.

**Permitted scope:** personal, research, and educational use only.

**Prohibited scope:** commercial or monetized use, advertising, paid services,
resale, and any other revenue-generating use are prohibited.

`license: other` identifies non-standard model terms. These terms are a custom
use restriction, not an OSI-approved open-source license. No rights are granted
to any source artwork, characters, names, trademarks, datasets, synthetic
training images, or other third-party material. The statement that Rei is an
original project character does not grant rights to the downloader and does not
remove rights or claims that may attach to the generation lineage. Downloading
the weights does not supply permission from any rights holder.

The downloader and user are solely responsible for determining legality,
obtaining all necessary permissions, complying with local law, and following
all applicable platform and upstream terms. The software and artifact are
provided as-is, without warranties of any kind. To the maximum extent permitted
by law, the maintainer excludes liability for use, outputs, claims, damages, or
other consequences arising from the artifact.

This disclaimer and the custom restriction do not override applicable law or
upstream licenses. All applicable upstream base-model terms also govern. Review
the [NoobAI XL V-Pred 1.0 model card and terms](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0),
the upstream [Illustrious XL model card](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0),
its [terms of use](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0/blob/main/TERM_OF_USE),
and the linked [Fair AI Public License 1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
before downloading or using this adapter.
