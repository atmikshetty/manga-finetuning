---
license: other
base_model: Laxhar/noobai-XL-Vpred-1.0
base_model_relation: adapter
library_name: diffusers
pipeline_tag: text-to-image
instance_prompt: blcmanga, blccolor, jjbamanga
tags:
  - stable-diffusion-xl
  - diffusers
  - lora
  - text-to-image
  - v-prediction
  - manga
  - monochrome
  - color
  - multistyle
  - copyrighted-training-data
---

# Bleach and JoJo Multistyle NoobAI XL V-Pred LoRA

This SDXL LoRA provides three separately prompted manga registers on NoobAI XL
V-Pred. It is provided only for personal, research, and educational use.

## Artifact

- Repository: `sleephashira/bleach-jojo-multistyle-noobai-xl-vpred-lora`
- File: `multi3_lora.safetensors`
- Size: `456519428` bytes
- SHA-256: `bdedd00bcbd33deff9a4159d7db977a5def6cfb9b2bad11887d1e27b0aa1fba5`
- Base model: `Laxhar/noobai-XL-Vpred-1.0`
- Triggers: `blcmanga`, `blccolor`, `jjbamanga`

## Training Summary

The training set contained 1,800 cleaned, extracted, copyrighted panels:

- 600 monochrome Bleach panels for `blcmanga`
- 600 official-color Bleach panels for `blccolor`
- 600 JoJo panels for `jjbamanga`

Checkpoint step 3600 was selected for this release.

## Tested Usage

NoobAI XL V-Pred requires **Euler**, `prediction_type="v_prediction"`,
`rescale_betas_zero_snr=True`, `guidance_rescale=0.7`, and CFG 4-5. Other
samplers or epsilon-prediction settings do not provide the intended inference
behavior. Start with one trigger; prompts may combine triggers experimentally.
Use `monochrome, greyscale` with `blcmanga` or `jjbamanga`, and explicit color
tags with `blccolor`. A tested starting point is 28 steps, CFG 5, and LoRA scale
0.75 at approximately 1024x1024 total pixel area.

```python
from diffusers import EulerDiscreteScheduler

pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config,
    prediction_type="v_prediction",
    rescale_betas_zero_snr=True,
)
pipe.load_lora_weights(
    "sleephashira/bleach-jojo-multistyle-noobai-xl-vpred-lora",
    weight_name="multi3_lora.safetensors",
)
pipe.fuse_lora(lora_scale=0.75)

image = pipe(
    "blcmanga, monochrome, greyscale, 1boy, sword, rain",
    width=832,
    height=1216,
    num_inference_steps=28,
    guidance_scale=5.0,
    guidance_rescale=0.7,
).images[0]
```

Results vary by prompt, seed, resolution, and adapter strength. The model can
reproduce biases, visual motifs, or character associations from its training
set and may produce malformed anatomy, text, borders, or panel details.

## Terms, Rights, and Disclaimer

This adapter was trained on extracted Bleach and JoJo panels. The source
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
the [NoobAI XL V-Pred 1.0 model card and terms](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0),
the upstream [Illustrious XL model card](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0),
its [terms of use](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0/blob/main/TERM_OF_USE),
and the linked [Fair AI Public License 1.0-SD](https://freedevproject.org/faipl-1.0-sd/)
before downloading or using this adapter.
