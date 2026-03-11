"""Capability 1 demo: camera API abstraction.

Run this script before and after swapping the camera hardware.
Same code, different camera, same results.
"""

import asyncio

import open3d as o3d
from PIL import Image
from viam.robot.client import RobotClient
from viam.components.camera import Camera


async def main():
    robot = await RobotClient.at_address(
        "<ROBOT_ADDRESS>",
        RobotClient.Options.with_api_key(
            api_key="<API_KEY>",
            api_key_id="<API_KEY_ID>",
        ),
    )

    camera = Camera.from_robot(robot, "my-camera")

    # Get a 2D image
    image = await camera.get_image()
    image.save("output.png")
    print(f"Saved image: {image.size[0]}x{image.size[1]}")

    # Get a 3D point cloud
    pcd_bytes, _ = await camera.get_point_cloud()
    with open("output.pcd", "wb") as f:
        f.write(pcd_bytes)
    print(f"Saved point cloud: {len(pcd_bytes)} bytes")

    # Visualize the point cloud
    pcd = o3d.io.read_point_cloud("output.pcd")
    o3d.visualization.draw_geometries([pcd])

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
