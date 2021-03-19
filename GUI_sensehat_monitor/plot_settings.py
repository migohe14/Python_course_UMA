class Plot_settings:

    FACECOLOR = '#005a87'
    LABEL_X = 'Tiempo'
    SUBPLOT = 111
    TITLE = 'Práctica GUI Sensehat'
    LABEL = 'Gráfica'
    ROTATION_X = 45
    TIME = 'time'
    SENSOR = 'sensor'


    def __init__(self):
        pass

    def tags_canvas(self):
        # Sensor seleccionado (1-> Temp, 2-> Pres, 3-> Hume)
        return {
            "1": {
                self.TITLE: "Temperatura",
                self.LABEL: "(ºC)"
            },
            "2": {
                self.TITLE: "Presión",
                self.LABEL: "(mmHg)"
            },
            "3": {
                self.TITLE: "Humedad",
                self.LABEL: "(%)"
            },
        }

    def dimensions_canvas(self):
        return {
            'x':85, 
            'y':10,
            'width':650,
            'height':550
        }

    def plot_style_temp(self):
        return {
            'color': '#005a87',
            'marker': 'o',
            'linestyle': 'dashed',
            'linewidth': 1,
            'markersize': 5,
            'label': 'Temperatura'
        }
    
    def plot_style_pres(self):
        return {
            'color': 'green',
            'marker': 'v',
            'linestyle': 'dashed',
            'linewidth': 1,
            'markersize': 5,
            'label': 'Presión'
        }

    def plot_style_humd(self):
        return {
            'color': 'blue',
            'marker': '*',
            'linestyle': 'dashed',
            'linewidth': 1,
            'markersize': 5,
            'label': 'Humedad'
        }

    def get_style_sensor(self, value):
        styles = {
            '1': self.plot_style_temp(),
            '2': self.plot_style_pres(),
            '3': self.plot_style_humd(),
        }
        return styles[value]