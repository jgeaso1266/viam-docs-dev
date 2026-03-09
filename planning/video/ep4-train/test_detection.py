"""
Viam Essentials Ep 4: Train and Deploy Models
Test script — verifies the trained model detects objects from the camera.
"""

import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    detector = VisionClient.from_robot(robot, "my-detector")

    # Get detections from camera
    detections = await detector.get_detections_from_camera("my-camera")

    if not detections:
        print("No detections found.")
    else:
        for d in detections:
            print(f"{d.class_name}: {d.confidence:.2f} "
                  f"at ({d.x_min}, {d.y_min}, {d.x_max}, {d.y_max})")

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
