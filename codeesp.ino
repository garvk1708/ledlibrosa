#include <ESP8266WiFi.h>

const char* ssid = "agh";            
const char* password = "blackniqqa";  

WiFiServer server(80);
const int ledPin = LED_BUILTIN;       

void setup() {
    Serial.begin(115200);
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());  
    server.begin();  
}

void loop() {
    WiFiClient client = server.available();  
    if (client) {
        String request = client.readStringUntil('\r');  
        client.flush();
        if (request.indexOf("/LED=ON") != -1) {
            digitalWrite(ledPin, LOW);  
        } else if (request.indexOf("/LED=OFF") != -1) {
            digitalWrite(ledPin, HIGH);  
        }
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.println();
        client.println("<html><body>LED control</body></html>");
        client.stop();  
    }
}
