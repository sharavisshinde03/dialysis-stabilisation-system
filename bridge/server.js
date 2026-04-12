const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');
const WebSocket = require('ws');

const port = new SerialPort({
  path: '/dev/cu.usbmodem1101', // 🔴 CHANGE THIS (check Arduino IDE)
  baudRate: 115200,
});

const parser = port.pipe(new ReadlineParser({ delimiter: '\n' }));

const wss = new WebSocket.Server({ port: 8080 });

console.log("WebSocket running on ws://localhost:8080");

parser.on('data', (data) => {
  console.log("Arduino:", data);

  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
});