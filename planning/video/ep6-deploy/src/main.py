"""
Viam Essentials Ep 6: Manage Deployments
Module version of the detect-and-move logic from Ep 5.
Runs as a managed service inside viam-server.
"""

import asyncio
from typing import Any, ClassVar, Mapping, Optional, Sequence, Tuple

from viam.module.module import Module
from viam.resource.base import ResourceBase
from viam.services.generic import Generic
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.utils import ValueTypes
from viam.components.arm import Arm
from viam.services.vision import VisionClient
from viam.proto.component.arm import JointPositions
from viam.resource.easy_resource import EasyResource
from viam.logging import getLogger

LOGGER = getLogger(__name__)


class DetectAndMove(Generic, EasyResource):
    MODEL = "YOUR-ORG-ID:wrench-finder:detect-and-move"

    arm: Arm
    detector: VisionClient
    camera_name: str
    confidence_threshold: float
    move_scale: float

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        required_deps = []

        for attr in ["arm_name", "camera_name", "detector_name"]:
            if attr not in fields:
                raise ValueError(f"Missing required attribute: {attr}")
            if not fields[attr].string_value:
                raise ValueError(f"{attr} cannot be empty")

        required_deps.append(fields["arm_name"].string_value)
        required_deps.append(fields["detector_name"].string_value)
        return required_deps, []

    def reconfigure(
        self,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase],
    ):
        fields = config.attributes.fields

        arm_name = fields["arm_name"].string_value
        detector_name = fields["detector_name"].string_value
        self.camera_name = fields["camera_name"].string_value

        self.confidence_threshold = (
            fields["confidence_threshold"].number_value
            if "confidence_threshold" in fields
            else 0.7
        )
        self.move_scale = (
            fields["move_scale"].number_value
            if "move_scale" in fields
            else 10.0
        )

        arm_resource = Arm.get_resource_name(arm_name)
        self.arm = dependencies[arm_resource]

        detector_resource = VisionClient.get_resource_name(detector_name)
        self.detector = dependencies[detector_resource]

        LOGGER.info(
            f"Configured: arm={arm_name}, camera={self.camera_name}, "
            f"detector={detector_name}, threshold={self.confidence_threshold}, "
            f"scale={self.move_scale}"
        )

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        if command.get("action") == "detect_and_move":
            result = await self._detect_and_move()
            return {"result": result}
        return {"error": "Unknown command. Use {'action': 'detect_and_move'}"}

    async def _detect_and_move(self) -> str:
        detections = await self.detector.get_detections_from_camera(
            self.camera_name
        )

        wrench = None
        for d in detections:
            if (d.class_name == "wrench"
                    and d.confidence > self.confidence_threshold):
                wrench = d
                break

        if wrench is None:
            return "No wrench detected"

        center_x = (wrench.x_min + wrench.x_max) / 2
        positions = await self.arm.get_joint_positions()
        new_values = list(positions.values)
        offset = (center_x - 320) / 320
        new_values[0] += offset * self.move_scale

        await self.arm.move_to_joint_positions(
            JointPositions(values=new_values)
        )
        return (
            f"Moved toward wrench ({wrench.confidence:.2f}) "
            f"by {offset * self.move_scale:.1f} degrees"
        )


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
