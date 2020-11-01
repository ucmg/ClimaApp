import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt

owm=pyowm.OWM('ca58563a751adf230b62342a533c7375')
mgr=owm.weather_manager()

degree_sign= u'\N{DEGREE SIGN}'

st.title("Análise Climática para os próximos 5 dias")
st.write("## Tecnologias de Código Aberto da UCMG")

st.write("### Escreva o nome de uma cidade, selecione a unidade de temperatura e o tipo de gráfico na barra lateral")

place=st.text_input("Nome da Cidade", "")


if place == None:
    st.write("Insira uma CIDADE!")



unit=st.selectbox("Selecione uma Unidade de Temperatura",("Celsius","Fahrenheit"))

g_type=st.selectbox("Selecione o tipo de gráfico",("Gráfico de Linhas","Gráfico de Barras"))

if unit == 'Celsius':
    unit_c = 'celsius'
else:
    unit_c = 'fahrenheit'


def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast=forecaster.forecast
    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        #day = gmt_to_eastern(weather.reference_time())
        date = day.date()
        if date not in dates:
            dates.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return(days, temp_min, temp_max)

def init_plot():
     plt.figure('PyOWM Weather', figsize=(5,4))
     plt.xlabel('Day')
     plt.ylabel(f'Temperature ({degree_sign}F)')
     plt.title('Weekly Forecast')



def plot_temperatures(days, temp_min, temp_max):
    days = dates.date2num(days)
    bar_min = plt.bar(days-.25, temp_min, width=0.5, color='#4286f4')
    bar_max = plt.bar(days+.25, temp_max, width=0.5, color='#e58510')
    return (bar_min, bar_max)

def plot_temperatures_line(days, temp_min, temp_max):
    days = dates.date2num(days)
    bar_min = plt.plot(days, temp_min)
    bar_max = plt.plot(days, temp_max)
    return (bar_min, bar_max)

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)

def write_temperatures_on_bar_chart(bar_min, bar_max):
    axes = plt.gca()
    y_axis_max = axes.get_ylim()[1]
    label_offset = y_axis_max * .1
    # Write the temperatures on the chart
    for bar_chart in [bar_min, bar_max]:
        for index, bar in enumerate(bar_chart):
            height = bar.get_height()
            xpos = bar.get_x() + bar.get_width()/2.0
            ypos = height - label_offset
            label_text = str(int(height)) + degree_sign
            plt.text(xpos, ypos, label_text,
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='white')

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    bar_min, bar_max = plot_temperatures(days, temp_min, temp_max)
    label_xaxis(days)
    write_temperatures_on_bar_chart(bar_min, bar_max)
    st.pyplot()
    st.title("Temperaturas Máximas e Mínimas")
    for i in range (0,5):
        st.write("#### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    bar_min, bar_max = plot_temperatures_line(days, temp_min, temp_max)
    label_xaxis(days)
    st.pyplot()
    st.title("Temperaturas Máximas e Mínimas")
    for i in range (0,5):
        st.write("#### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Mudanças de Temperatura Eminentes")
    if forecaster.will_have_fog():
        st.write("#### Alerta de nevoeiro 🌫️")
    if forecaster.will_have_rain():
        st.write("#### Alerta de chuva 🌧️")
    if forecaster.will_have_storm():
        st.write("#### Alerta de tempestade 🌩️")
    if forecaster.will_have_snow():
        st.write("#### Alerta de neve ❄️")
    if forecaster.will_have_tornado():
        st.write("#### Alerta de tornado 🌪️")
    if forecaster.will_have_hurricane():
        st.write("#### Alerta de furacão 🌀")
    if forecaster.will_have_clouds():
        st.write("#### Céu nublado ☁️")    
    if forecaster.will_have_clear():
        st.write("#### Tempo limpo ☀️")

def cloud_and_wind():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    cloud_cov=weather.clouds
    winds=weather.wind()['speed']
    st.title("Cobertura de nuvens e velocidade do vento")
    st.write('#### A cobertura de nuvem atual para',place,'é',cloud_cov,'%')
    st.write('#### A velocidade atual do vento para',place,'é',winds,'mph')

def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title("Hora do nascer e pôr do sol")
    Brazil = pytz.timezone("America/Sao_Paulo")
    ss=weather.sunset_time(timeformat='iso')
    sr=weather.sunrise_time(timeformat='iso')  
    st.write("#### Hora do nascer do sol em",place,"é",sr)
    st.write("#### Hora do pôr do sol em",place,"é",ss)

def updates():
    other_weather_updates()
    cloud_and_wind()
    sunrise_and_sunset()


if __name__ == '__main__':
    
    if st.button("ENVIAR"):
        if g_type == 'Line Graph':
            draw_line_chart()    
        else:
            draw_bar_chart()
        updates()
        
    
        
        
    
    
