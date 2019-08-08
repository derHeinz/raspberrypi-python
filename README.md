# Python Scripts

Python scripts I use in conjunction with home automation system on Raspberry pi.

Scripts are written for Python2, some are updated to Python3.

Scripts for following UseCases are present:
===

BLE related:
* *read_flower_mate.py* Read Data from MiFlower compatible devices https://www.amazon.de/Ollivan-kabelloser-Pflanzen-Sensor-Bluetooth-N%C3%A4hrstoff/dp/B01LWYZUSJ
* *scan_results.py* Parse BLE advertisements to get their data. Use bluepy (https://github.com/IanHarvey/bluepy) the Scanner class and pass device.rawData to ScanResultParser.process_device_raw_data.
* *xiaomiTemphum.py" Read battery level, humidity and temperature from Xiaomi Temperature and Humidity Sensor (https://de.aliexpress.com/item/Original-Xiaomi-Mijia-Bluetooth-Temperatur-Intelligente-Luftfeuchtigkeit-Sensor-Lcd-bildschirm-Digitale-Thermometer-Feuchtigkeit-Meter-Mi-Hause/32843325647.html)
* *blue_scan.py* Scan for bluez devices and print the information.

Others:
* *phoneIntegration.py* Interact with my [other application for old smartphones](https://github.com/derHeinz/HouseholdHelper)
* *phoneNewsSpeech.py* Get some newsfeeds, read it out and send to household helper
* *phoneWeatherSpeech.py* Get some weather information and speak them out at household helper
* *postopenhab.py* Interact with openhab (get and set)
* *calendarparse.py* Parse events from .ics files, such as holidays
* *wakeonlan.py* Send some wake-on-lan packages to wake-up WOL device
* *wpgpio.py* Swicht some raspberrypi GPIOs
* *search_name.py* Finds IPs for mac or hostname via arp table
* *energenie_eg_pm2_lan.py* Energenie EG-PM2-LAN can be read/set with this little python class
* *error_hospital.py* general util for writing errors to file
* *radioalarmclockIntegration.py* cli integration to https://github.com/derHeinz/radioalarmclock
* *raspberryHealthIntegration.py* cli integration to https://github.com/derHeinz/raspberry_health

Python3.x compatibilty:
* *calendarparse.py*
* *error_hospital.py*
* *postopenhab.py*
* *radioalarmclockIntegration.py*
* *raspberryHealthIntegration.py*
* *search_name.py*
