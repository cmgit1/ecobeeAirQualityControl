import AirQualityReader

def ecobeeControl(iaq: float, iaq_accuracy: int):
    print(f'IAQ {iaq:.0f}, IAQ Accuracy {iaq_accuracy:d}')

AirQualityReader.run(ecobeeControl)