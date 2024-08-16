export default function HabetTelemetryPlugin() {
    return function install(openmct) {
        const socket = new WebSocket('ws://localhost:8080');

        // Object to store telemetry data keyed by timestamp
        let latestData = {};

        // WebSocket message handler
        socket.onmessage = function(event) {
            try {
                const parsedData = JSON.parse(event.data);
                const timestamp = parsedData.timestamp;
                const telemetryValues = parsedData.data;

                // Update latestData
                latestData = {
                    timestamp: timestamp,
                    ...telemetryValues
                };

                // Notify OpenMCT that new telemetry data is available
                openmct.telemetry.addDatum({
                    identifier: {
                        key: 'websocket.telemetry',
                        namespace: 'example.telemetry'
                    },
                    ...latestData
                });
            } catch (error) {
                console.error('Failed to parse WebSocket message:', error);
            }
        };

        // Define a basic telemetry provider
        openmct.telemetry.addProvider({
            supportsSubscribe: function(domainObject) {
                return domainObject.type === 'example.telemetry' && domainObject.identifier.key === 'websocket.telemetry';
            },
            subscribe: function(domainObject, callback) {
                const intervalId = setInterval(() => {
                    if (latestData.timestamp) {
                        callback(latestData);
                    }
                }, 1000);

                return function unsubscribe() {
                    clearInterval(intervalId);
                };
            }
        });

        // Register the telemetry object
        openmct.objects.addProvider('example.telemetry', {
            get: function(identifier) {
                if (identifier.key === 'websocket.telemetry') {
                    return Promise.resolve({
                        identifier: identifier,
                        name: 'WebSocket Telemetry',
                        type: 'example.telemetry',
                        telemetry: {
                            values: [
                                {
                                    key: 'timestamp',
                                    name: 'Timestamp',
                                    format: 'utc',
                                    hints: {
                                        domain: 1
                                    }
                                },
                                {
                                    key: 'latitude',
                                    name: 'Latitude',
                                    format: 'float',
                                    hints: {
                                        range: 1
                                    }
                                },
                                {
                                    key: 'longitude',
                                    name: 'Longitude',
                                    format: 'float',
                                    hints: {
                                        range: 2
                                    }
                                },
                                // Add other telemetry fields here
                            ]
                        }
                    });
                }
            }
        });

        openmct.objects.addRoot({
            namespace: 'example.telemetry',
            key: 'root'
        });

        openmct.objects.addProvider('example.telemetry', {
            get: function(identifier) {
                if (identifier.key === 'root') {
                    return Promise.resolve({
                        identifier: identifier,
                        name: 'Example Telemetry',
                        type: 'folder',
                        location: 'ROOT'
                    });
                }
            }
        });
    };
}
