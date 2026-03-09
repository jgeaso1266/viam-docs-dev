"""
Viam Essentials Ep 5: Develop Remotely
Demo script — detects an object with the vision service, then moves
the arm toward it. Runs on a laptop, controls hardware remotely.
"""

import asyncio

from viam.robot.client import RobotClient
from viam.components.arm import Arm
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.proto.component.arm import JointPositions


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    arm = Arm.from_robot(robot, "my-arm")
    detector = VisionClient.from_robot(robot, "my-detector")

    # Detect objects from camera
    detections = await detector.get_detections_from_camera("my-camera")

    wrench = None
    for d in detections:
        if d.class_name == "wrench" and d.confidence > 0.7:
            wrench = d
            break

    if wrench is None:
        print("No wrench detected.")
        await robot.close()
        return

    print(f"Found wrench: {wrench.confidence:.2f} "
          f"at ({wrench.x_min}, {wrench.y_min}, "
          f"{wrench.x_max}, {wrench.y_max})")

    # Calculate center of detection in image coordinates
    center_x = (wrench.x_min + wrench.x_max) / 2
    center_y = (wrench.y_min + wrench.y_max) / 2
    print(f"Detection center: ({center_x:.0f}, {center_y:.0f})")

    # Simple proportional joint move based on detection position
    # This is a demonstration — real applications would use the
    # motion service for proper path planning
    positions = await arm.get_joint_positions()
    new_values = list(positions.values)

    # Adjust joint 1 (base rotation) based on horizontal position
    # Image center is 320 for a 640px-wide image
    offset = (center_x - 320) / 320  # Normalize to [-1, 1]
    new_values[0] += offset * 10  # Scale to degrees

    print(f"Moving arm joint 1 by {offset * 10:.1f} degrees...")
    await arm.move_to_joint_positions(JointPositions(values=new_values))
    print("Arm moved toward wrench.")

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
