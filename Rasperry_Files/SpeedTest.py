from MCP import MCP3008
import time
adc = MCP3008()

while True:
    time.sleep(0.1)
    value = adc.read(2)
    print(value)

