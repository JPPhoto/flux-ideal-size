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


@invocation(
    "flux_kontext_ideal_size",
    title="Flux Kontext Ideal Size",
    tags=["math", "ideal_size", "flux", "kontext"],
    version="1.0.1",
)
class FluxKontextIdealSizeInvocation(BaseInvocation):
    """Calculates the ideal size for generation using Flux Kontext"""

    width: int = InputField(default=1024, description="Target width")
    height: int = InputField(default=576, description="Target height")

    def invoke(self, context: InvocationContext) -> FluxIdealSizeOutput:
        aspect = self.width / self.height
        kontext_resolutions = [
            (672, 1568),
            (688, 1504),
            (720, 1456),
            (752, 1392),
            (800, 1328),
            (832, 1248),
            (880, 1184),
            (944, 1104),
            (1024, 1024),
            (1104, 944),
            (1184, 880),
            (1248, 832),
            (1328, 800),
            (1392, 752),
            (1456, 720),
            (1504, 688),
            (1568, 672),
        ]  # From https://github.com/black-forest-labs/flux/blob/main/src/flux/util.py, PREFERED_KONTEXT_RESOLUTIONS

        _, scaled_width, scaled_height = min(
            ((abs(aspect - w / h), w, h) for w, h in kontext_resolutions), key=lambda x: x[0]
        )

        return FluxIdealSizeOutput(width=scaled_width, height=scaled_height)
