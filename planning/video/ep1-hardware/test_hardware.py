"""
Viam Essentials Ep 1: Get Hardware Running
Test script — verifies arm and camera are connected and responding.
Run from laptop against the configured machine.
"""

import asyncio

from viam.robot.client import RobotClient
from viam.components.arm import Arm
from viam.components.camera import Camera


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    # --- Arm check ---
    arm = Arm.from_robot(robot, "my-arm")
    joint_positions = await arm.get_joint_positions()
    print(f"Arm joint positions: {joint_positions.values}")

    end_position = await arm.get_end_position()
    print(f"Arm end position: x={end_position.x:.1f}, "
          f"y={end_position.y:.1f}, z={end_position.z:.1f}")

    # --- Camera check ---
    camera = Camera.from_robot(robot, "my-camera")
    image = await camera.get_image()
    print(f"Camera image: {image.width}x{image.height}, "
          f"mime_type={image.mime_type}")

    # Get both color and depth streams
    images, metadata = await camera.get_images()
    for img in images:
        print(f"  Stream '{img.name}': {img.width}x{img.height}")

    print("\nAll hardware responding.")
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
