/**
 * Viam Essentials Ep 8: Productize with Apps
 * Minimal TypeScript SDK demo — connects to a machine and streams camera.
 *
 * This is a reference for what the demo dashboard must be able to do.
 * The actual dashboard will be a full web app with custom branding.
 */

import * as VIAM from "@viamrobotics/sdk";
import { CameraClient, StreamClient } from "@viamrobotics/sdk";

async function connectToMachine(host: string, apiKey: string,
                                 apiKeyId: string) {
  const machine = await VIAM.createRobotClient({
    host: host,
    credentials: {
      type: "api-key",
      payload: apiKey,
      authEntity: apiKeyId,
    },
    signalingAddress: "https://app.viam.com:443",
  });
  return machine;
}

async function streamCamera(machine: VIAM.RobotClient,
                             cameraName: string,
                             videoElement: HTMLVideoElement) {
  const stream = new StreamClient(machine);
  const mediaStream = await stream.getStream(cameraName);
  videoElement.srcObject = mediaStream;
  await videoElement.play();
}

async function getMachineStatus(machine: VIAM.RobotClient) {
  const resources = await machine.resourceNames();
  return {
    online: true,
    resourceCount: resources.length,
    resources: resources.map((r) => r.name),
  };
}

// Dashboard would call these functions to:
// 1. Connect to each machine in the fleet
// 2. Show online/offline status
// 3. Stream camera feeds
// 4. Display detection results

export { connectToMachine, streamCamera, getMachineStatus };
