# Copyright (c) 2025 Jonathan S. Pollack (https://github.com/JPPhoto)

import math

from invokeai.invocation_api import (
    BaseInvocation,
    BaseInvocationOutput,
    InputField,
    InvocationContext,
    OutputField,
    invocation,
    invocation_output,
)


@invocation_output("flux_ideal_size_output")
class FluxIdealSizeOutput(BaseInvocationOutput):
    """Base class for invocations that output an image"""

    width: int = OutputField(description="The ideal width of the image in pixels")
    height: int = OutputField(description="The ideal height of the image in pixels")


@invocation("flux_ideal_size", title="Flux Ideal Size", tags=["math", "ideal_size", "flux"], version="1.0.0")
class FluxIdealSizeInvocation(BaseInvocation):
    """Calculates the ideal size for generation to avoid duplication"""

    width: int = InputField(default=1024, description="Target width")
    height: int = InputField(default=576, description="Target height")
    multiplier: float = InputField(default=1.0, description="Dimensional multiplier")

    def trim_to_multiple_of(self, *args, multiple_of=16):
        return tuple((x - x % multiple_of) for x in args)

    def invoke(self, context: InvocationContext) -> FluxIdealSizeOutput:
        aspect = self.width / self.height
        dimension = 1024
        dimension = dimension * self.multiplier
        min_dimension = math.floor(dimension * 0.5)
        model_area = dimension * dimension  # hardcoded for now since all models are trained on square images

        if aspect > 1.0:
            init_height = max(min_dimension, math.sqrt(model_area / aspect))
            init_width = init_height * aspect
        else:
            init_width = max(min_dimension, math.sqrt(model_area * aspect))
            init_height = init_width / aspect

        scaled_width, scaled_height = self.trim_to_multiple_of(
            math.floor(init_width),
            math.floor(init_height),
        )

        return FluxIdealSizeOutput(width=scaled_width, height=scaled_height)
