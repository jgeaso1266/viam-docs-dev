"""
Viam Essentials Ep 2: Operate from Anywhere
Demo script — connects to a remote machine from a laptop, reads the
camera, and moves the arm. Shows that no VPN or port forwarding is needed.
"""

import asyncio

from viam.robot.client import RobotClient
from viam.components.arm import Arm
from viam.components.camera import Camera


async def main():
    # Connect from anywhere — no VPN, no port forwarding
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    # Read the camera from here
    camera = Camera.from_robot(robot, "my-camera")
    image = await camera.get_image()
    print(f"Got image: {image.width}x{image.height}")

    # Move the arm from here
    arm = Arm.from_robot(robot, "my-arm")
    positions = await arm.get_joint_positions()
    print(f"Current joints: {positions.values}")

    # Jog joint 1 by 15 degrees
    new_values = list(positions.values)
    new_values[0] += 15.0
    from viam.proto.component.arm import JointPositions
    await arm.move_to_joint_positions(JointPositions(values=new_values))
    print("Arm moved.")

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
