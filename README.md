# ideal-size-node
An InvokeAI node for calculating ideal image sizes to avoid duplication **for Flux models only**.
This InvokeAI node takes in your target dimensions and outputs a width and height for initial generation using Flux models. You can generate with that resolution to avoid strange image compositions (especially useful for ultra-wide or ultra-tall images), then upscale and enhance the resulting latents however you want.
