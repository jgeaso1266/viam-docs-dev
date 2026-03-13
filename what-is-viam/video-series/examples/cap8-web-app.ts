// This code must be run in a browser environment.
import {
  createRobotClient,
  SensorClient,
  SwitchClient,
  StreamClient,
} from '@viamrobotics/sdk';
import Cookies from 'js-cookie';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Filler);

// ─── COMPONENT NAMES ──────────────────────────────────────────────────────────

const ENV_SENSOR   = "temp-moisture-sensor";
const SOIL_SENSORS = ["soil-sensor-2", "soil-sensor-3", "soil-sensor-4"];
const LIGHT_SWITCH = "light-smart-plug";
const CAMERA_NAME  = "tent-camera";

const POLL_INTERVAL_MS       = 5000;
const MAX_CHART_POINTS       = 60;  // 5 minutes at 5s intervals
const MAX_CONSECUTIVE_ERRORS = 3;

// ─── HEALTH THRESHOLDS ────────────────────────────────────────────────────────

const THRESHOLDS = {
  temp_c:   { ok: [18, 28],    warn: [12, 34]    },
  humidity: { ok: [50, 80],    warn: [35, 90]    },
  co2_ppm:  { ok: [400, 1200], warn: [300, 2000] },
  moisture: { ok: [500, 900],  warn: [350, 1000] },
};

type HealthLevel = "ok" | "warn" | "alert" | "neutral";

function healthClass(value: number, key: keyof typeof THRESHOLDS): HealthLevel {
  const t = THRESHOLDS[key];
  if (value >= t.ok[0]   && value <= t.ok[1])  return "ok";
  if (value >= t.warn[0] && value <= t.warn[1]) return "warn";
  return "alert";
}

// ─── DOM HELPERS ──────────────────────────────────────────────────────────────

function setStatus(msg: string, cls: "connecting" | "connected" | "error") {
  const el = document.getElementById("connection-status")!;
  el.textContent = `● ${msg}`;
  el.className = cls;
}

function setEnvReading(
  id: string,
  value: number,
  decimals: number,
  healthKey: keyof typeof THRESHOLDS
) {
  const el = document.getElementById(id);
  if (!el) return;
  el.className = `reading-cell__value ${healthClass(value, healthKey)}`;
  el.textContent = value.toFixed(decimals);
}

const MOISTURE_MIN = 200;
const MOISTURE_MAX = 1017;

function updateSoilRow(sensorName: string, val: number) {
  const row = document.querySelector<HTMLElement>(`[data-sensor="${sensorName}"]`);
  if (!row) return;

  const barPct = Math.min(100, Math.max(0,
    (val - MOISTURE_MIN) / (MOISTURE_MAX - MOISTURE_MIN) * 100
  ));
  const h = healthClass(val, "moisture");

  const bar = row.querySelector<HTMLElement>(".soil-bar")!;
  bar.style.width = `${barPct.toFixed(0)}%`;
  bar.className = `soil-bar ${h === "ok" ? "" : h}`;
  row.querySelector<HTMLElement>(".soil-val")!.textContent = String(val.toFixed(0));
}

function updateLastUpdated() {
  const el = document.getElementById("last-updated");
  if (el) el.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
}

// ─── CHARTS ───────────────────────────────────────────────────────────────────

function makeTimeLabel() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function pushPoint(chart: Chart, label: string, datasetIndex: number, value: number) {
  // Label is shared across datasets — only push it once per poll (on dataset 0)
  if (datasetIndex === 0) {
    chart.data.labels!.push(label);
    if (chart.data.labels!.length > MAX_CHART_POINTS) {
      chart.data.labels!.shift();
    }
  }
  const ds = chart.data.datasets[datasetIndex];
  (ds.data as number[]).push(value);
  if ((ds.data as number[]).length > MAX_CHART_POINTS) {
    (ds.data as number[]).shift();
  }
}

const CHART_RANGES = {
  co2:      { min: 0,            max: 2000        },
  temp:     { min: 0,            max: 50           },
  humidity: { min: 0,            max: 100          },
  soil:     { min: MOISTURE_MIN, max: MOISTURE_MAX },
};

function makeLineChart(
  canvasId: string,
  label: string,
  color: string,
  range: { min: number; max: number }
): Chart {
  const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  return new Chart(canvas, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label,
        data: [],
        borderColor: color,
        backgroundColor: color + "22",
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
        fill: true,
      }],
    },
    options: {
      animation: false,
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { mode: "index", intersect: false } },
      scales: {
        x: { ticks: { maxTicksLimit: 6, maxRotation: 0, font: { size: 11 } }, grid: { display: false } },
        y: { min: range.min, max: range.max, ticks: { font: { size: 11 } }, grid: { color: "#f0f0f0" } },
      },
    },
  });
}

function makeSoilChart(canvasId: string): Chart {
  const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  const seriesConfig = [
    { label: "Soil Moisture 2", color: "#16a34a" },
    { label: "Soil Moisture 3", color: "#4ade80" },
    { label: "Soil Moisture 4", color: "#eab308" },
  ];
  return new Chart(canvas, {
    type: "line",
    data: {
      labels: [],
      datasets: seriesConfig.map(({ label, color }) => ({
        label,
        data: [],
        borderColor: color,
        backgroundColor: "transparent",
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
      })),
    },
    options: {
      animation: false,
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: { mode: "index", intersect: false },
      },
      scales: {
        x: { ticks: { maxTicksLimit: 6, maxRotation: 0, font: { size: 11 } }, grid: { display: false } },
        y: { min: CHART_RANGES.soil.min, max: CHART_RANGES.soil.max, ticks: { font: { size: 11 } }, grid: { color: "#f0f0f0" } },
      },
    },
  });
}

// ─── CHART REGISTRY ───────────────────────────────────────────────────────────

const activeCharts: Chart[] = [];

function destroyCharts() {
  activeCharts.forEach(c => c.destroy());
  activeCharts.length = 0;
}

// ─── LIGHT STATE ──────────────────────────────────────────────────────────────

let lightIsOn = false;

function renderLightUI(isOn: boolean) {
  lightIsOn = isOn;
  const statusText = document.getElementById("light-status-text")!;
  const btn = document.getElementById("light-toggle") as HTMLButtonElement;
  statusText.textContent = isOn ? "Light is ON" : "Light is OFF";
  statusText.className   = `light-status-text ${isOn ? "light-on" : "light-off"}`;
  btn.textContent = isOn ? "Turn OFF" : "Turn ON";
  btn.className   = isOn ? "light-on-btn" : "light-off-btn";
  btn.disabled    = false;
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────

const main = async (apiKeyId: string, apiKeySecret: string, host: string): Promise<void> => {
  destroyCharts();
  setStatus("Connecting…", "connecting");

  let machine: Awaited<ReturnType<typeof createRobotClient>>;
  try {
    machine = await createRobotClient({
      host,
      credentials: { type: "api-key", payload: apiKeySecret, authEntity: apiKeyId },
      signalingAddress: "https://app.viam.com:443",
    });
    setStatus("Connected", "connected");
  } catch (err) {
    setStatus("Connection failed", "error");
    throw err;
  }

  const envSensor   = new SensorClient(machine, ENV_SENSOR);
  const soilClients = SOIL_SENSORS.map((n) => new SensorClient(machine, n));
  const lightSwitch = new SwitchClient(machine, LIGHT_SWITCH);
  const streamClient = new StreamClient(machine);

  // Charts
  const co2Chart   = makeLineChart("chart-co2",      "CO₂ (ppm)",    "#374151", CHART_RANGES.co2);
  const tempChart  = makeLineChart("chart-temp",     "Temperature",  "#2563eb", CHART_RANGES.temp);
  const humidChart = makeLineChart("chart-humidity", "Humidity (%)", "#0891b2", CHART_RANGES.humidity);
  const soilChart  = makeSoilChart("chart-soil");
  activeCharts.push(co2Chart, tempChart, humidChart, soilChart);

  // Light
  try {
    renderLightUI((await lightSwitch.getPosition()) === 1);
  } catch {
    renderLightUI(false);
  }

  // AbortController cleans up all event listeners when we disconnect or unload
  const abortController = new AbortController();
  const { signal } = abortController;

  const lightBtn = document.getElementById("light-toggle") as HTMLButtonElement;
  lightBtn.addEventListener("click", async () => {
    lightBtn.disabled = true;
    try {
      const newPos = lightIsOn ? 0 : 1;
      await lightSwitch.setPosition(newPos);
      renderLightUI(newPos === 1);
    } catch (err) {
      console.error("Error toggling light:", err);
      alert("Could not toggle light. Check the console for details.");
      lightBtn.disabled = false;
    }
  }, { signal });

  // Camera
  try {
    const cameraWrap = document.getElementById("camera-wrap")!;
    const video = document.createElement("video");
    video.autoplay = true;
    video.muted    = true;
    video.style.cssText = "width:100%;max-height:480px;object-fit:contain;display:block;";
    cameraWrap.innerHTML = "";
    cameraWrap.appendChild(video);
    const mediaStream = await streamClient.getStream(CAMERA_NAME);
    video.srcObject = mediaStream;
    await video.play().catch((e) => console.warn("Video autoplay blocked:", e));
  } catch {
    document.getElementById("camera-wrap")!.innerHTML =
      "<span style='color:#6b7280'>Camera unavailable</span>";
  }

  return new Promise<void>((resolve, reject) => {
    let consecutiveErrors = 0;

    const pollSensors = async () => {
      let hadError = false;
      const label = makeTimeLabel();

      // Env sensor — batch all three chart updates into one redraw
      try {
        const readings = await envSensor.getReadings();
        const temp  = readings["temperature_c"]    as number;
        const humid = readings["relative_humidity"] as number;
        const co2   = readings["co2_ppm"]           as number;

        if (temp  != null) { setEnvReading("val-temp",     temp,  1, "temp_c");   pushPoint(tempChart,  label, 0, temp);  }
        if (humid != null) { setEnvReading("val-humidity", humid, 0, "humidity"); pushPoint(humidChart, label, 0, humid); }
        if (co2   != null) { setEnvReading("val-co2",      co2,   0, "co2_ppm"); pushPoint(co2Chart,   label, 0, co2);   }

        tempChart.update();
        humidChart.update();
        co2Chart.update();
      } catch (err) {
        console.error("Error reading env sensor:", err);
        hadError = true;
      }

      // Soil sensors — always push the label on dataset 0 so charts stay aligned,
      // even if that sensor's reading was out of range
      let soilUpdated = false;
      for (let i = 0; i < soilClients.length; i++) {
        try {
          const readings = await soilClients[i].getReadings();
          const moisture = readings["moisture"];
          if (moisture != null) {
            const val = Number(moisture);
            if (val < MOISTURE_MIN || val > MOISTURE_MAX) {
              console.warn(`${SOIL_SENSORS[i]}: ignoring out-of-range reading (${val})`);
            } else {
              updateSoilRow(SOIL_SENSORS[i], val);
              pushPoint(soilChart, label, i, val);
              soilUpdated = true;
            }
          }
        } catch (err) {
          console.warn(`Error reading ${SOIL_SENSORS[i]}:`, err);
          hadError = true;
        }
      }
      if (soilUpdated) soilChart.update();

      if (hadError) {
        consecutiveErrors++;
        if (consecutiveErrors >= MAX_CONSECUTIVE_ERRORS) {
          clearInterval(pollTimer);
          abortController.abort();
          machine.disconnect();
          reject(new Error(`Lost connection after ${MAX_CONSECUTIVE_ERRORS} consecutive poll failures`));
          return;
        }
      } else {
        consecutiveErrors = 0;
      }

      updateLastUpdated();
    };

    pollSensors();
    const pollTimer = setInterval(pollSensors, POLL_INTERVAL_MS);

    window.addEventListener("beforeunload", () => {
      clearInterval(pollTimer);
      abortController.abort();
      machine.disconnect();
      resolve();
    }, { signal });
  });
};

// ─── RECONNECT LOOP ───────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  const machineCookieKey = window.location.pathname.split("/")[2];
  const cookie = Cookies.get(machineCookieKey);
  if (!cookie) {
    setStatus("No machine credentials found", "error");
    console.error("Expected a Viam machine cookie. Are you running through the Viam app proxy?");
    return;
  }

  let parsed: { apiKey: { id: string; key: string }; machineId: string; hostname: string };
  try {
    parsed = JSON.parse(cookie);
  } catch {
    setStatus("Invalid machine credentials", "error");
    console.error("Failed to parse machine cookie:", cookie);
    return;
  }

  const { apiKey: { id: apiKeyId, key: apiKeySecret }, hostname: host } = parsed;

  const connect = async () => {
    let attempt = 0;
    while (true) {
      try {
        await main(apiKeyId, apiKeySecret, host);
        return;
      } catch (err) {
        attempt++;
        const delaySec = Math.min(30, Math.pow(2, attempt - 1));
        console.error(`Attempt ${attempt} failed, retrying in ${delaySec}s:`, err);
        setStatus(`Reconnecting in ${delaySec}s… (attempt ${attempt})`, "error");
        await new Promise(r => setTimeout(r, delaySec * 1000));
      }
    }
  };

  connect();
});
