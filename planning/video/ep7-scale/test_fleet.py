"""
Viam Essentials Ep 7: Scale Your Fleet
Test script — connects to two machines and verifies they both have
the same detection capability from the shared fragment.
"""

import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def check_machine(address: str, api_key: str, api_key_id: str,
                        label: str):
    opts = RobotClient.Options.with_api_key(
        api_key=api_key, api_key_id=api_key_id
    )
    robot = await RobotClient.at_address(address, opts)

    detector = VisionClient.from_robot(robot, "my-detector")
    detections = await detector.get_detections_from_camera("my-camera")

    print(f"[{label}] {len(detections)} detections:")
    for d in detections:
        if d.confidence > 0.5:
            print(f"  {d.class_name}: {d.confidence:.2f}")

    await robot.close()


async def main():
    await asyncio.gather(
        check_machine(
            "MACHINE-1-ADDRESS",
            "MACHINE-1-API-KEY",
            "MACHINE-1-API-KEY-ID",
            "Machine 1"
        ),
        check_machine(
            "MACHINE-2-ADDRESS",
            "MACHINE-2-API-KEY",
            "MACHINE-2-API-KEY-ID",
            "Machine 2"
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
