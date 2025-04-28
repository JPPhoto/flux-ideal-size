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


@invocation("flux_ideal_size", title="Flux Ideal Size", tags=["math", "ideal_size", "flux"], version="1.0.1")
class FluxIdealSizeInvocation(BaseInvocation):
    """Calculates the ideal size for generation to avoid duplication"""

    width: int = InputField(default=1024, description="Target width")
    height: int = InputField(default=576, description="Target height")
    multiplier: float = InputField(default=1.0, description="Dimensional multiplier")

    def trim_to_multiple_of(self, x, multiple_of=16):
        x = math.floor(x)
        return int(x - x % multiple_of)

    def invoke(self, context: InvocationContext) -> FluxIdealSizeOutput:
        aspect = self.width / self.height
        dimension = 1024
        dimension = dimension * self.multiplier
        min_dimension = math.floor(dimension * 0.5)
        model_area = dimension * dimension  # hardcoded for now since all models are trained on square images

        if aspect > 1.0:
            scaled_height = self.trim_to_multiple_of(max(min_dimension, math.sqrt(model_area / aspect)))
            scaled_width = self.trim_to_multiple_of(scaled_height * aspect)
        else:
            scaled_width = self.trim_to_multiple_of(max(min_dimension, math.sqrt(model_area * aspect)))
            scaled_height = self.trim_to_multiple_of(scaled_width / aspect)

        return FluxIdealSizeOutput(width=scaled_width, height=scaled_height)
