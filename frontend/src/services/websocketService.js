class WebSocketService {
  constructor() {
    this.socket = null;

    this.messageCallbacks = [];
    this.notificationCallbacks = [];
    this.alertCallbacks = [];
    this.sensorCallbacks = [];

    this.shouldReconnect = true;
    this.reconnectInterval = 3000;
  }

  connect() {
    // Prevent duplicate connections
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN ||
        this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.shouldReconnect = true;

    this.socket = new WebSocket("ws://127.0.0.1:8000/ws/dashboard");

    this.socket.onopen = () => {
      console.log("✅ WebSocket Connected");
      this.send("Dashboard Connected");
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      console.log("📩 WebSocket:", data);

      this.messageCallbacks.forEach((callback) => callback(data));

      if (data.type === "notification") {
        this.notificationCallbacks.forEach((callback) =>
          callback(data.data)
        );
      }

      if (data.type === "alert") {
        this.alertCallbacks.forEach((callback) =>
          callback(data.data)
        );
      }

      if (
        data.type === "sensor_update" ||
        data.type === "sector_update"
      ) {
        this.sensorCallbacks.forEach((callback) =>
          callback(data.data)
        );
      }
    };

    this.socket.onerror = (error) => {
      console.error("❌ WebSocket Error:", error);
    };

    this.socket.onclose = () => {
      console.log("❌ WebSocket Closed");

      this.socket = null;

      if (this.shouldReconnect) {
        setTimeout(() => {
          this.connect();
        }, this.reconnectInterval);
      }
    };
  }

  onMessage(callback) {
    this.messageCallbacks.push(callback);
  }

  onNotification(callback) {
    this.notificationCallbacks.push(callback);
  }

  onAlert(callback) {
    this.alertCallbacks.push(callback);
  }

  onSensor(callback) {
    this.sensorCallbacks.push(callback);
  }

  send(data) {
    if (
      this.socket &&
      this.socket.readyState === WebSocket.OPEN
    ) {
      this.socket.send(data);
    }
  }

  disconnect() {
    this.shouldReconnect = false;

    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export default new WebSocketService();