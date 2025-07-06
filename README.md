# flux-ideal-size
InvokeAI nodes for calculating ideal image sizes to avoid duplication and artifacts, **for Flux models only**.

Flux Ideal Size takes in your target dimensions and outputs a width and height for initial generation using Flux
models. You can generate with that resolution to avoid strange image compositions (especially useful for ultra-wide
or ultra-tall images), then upscale and enhance the resulting latents however you want.

Flux Kontext Ideal Size uses a preset list of Kontext sizes (from
https://github.com/black-forest-labs/flux/blob/main/src/flux/util.py) and finds the closest size with a similar
aspect ratio. You use this size as the target size for Kontext-based generation to avoid artifacts and best
preserve composition.
