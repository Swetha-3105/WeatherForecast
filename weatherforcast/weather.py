import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("Weather Forcast App")
city = st.text_input("Enter City Name : ")
if city :
    st.session_state["city"]=city
if 'weather' not in st.session_state:
    st.session_state['weather'] = None
if 'graph_data' not in st.session_state:
    st.session_state['graph_data'] = None
#print(type(a))
if st.button("Get Weather"):
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=87f2ab18ad43dd7a4e058ffb31ef69a7"
    request=requests.get(api)
    if request.status_code==200:
        st.session_state['weather']=request.json()
        if 'weather' in st.session_state:
            
            data=st.session_state['weather']
            kelvin=data['main']['temp']
            celcius=round(kelvin-273.15,2)
            fahrenheit=round((kelvin-273.15)*(9/5)+32,2)
            st.subheader(f"{city} Temperature")
            st.write("Temperature in celcius:",celcius)
            st.write("Temperature in fahrenheit:",fahrenheit)
            st.write("Temperature in kelvin:",kelvin)
            st.write(f"Description : {data['weather'][0]['description']}")
            st.write(f"Pressure : {data['main']['pressure']}")
            st.markdown(f"Humidity : {data['main']['humidity']}")
            icon = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        #st.image(icon_url)
            st.markdown(
            f"""
            <div style="background-color: skyblue;border-radius: 10px; display: inline-block;">
            <img src="{icon_url}";>
            </div>
            """,
            unsafe_allow_html=True
            )

    else:
        if city =="":
            st.write("Please enter city name")
        else:
            st.write("City not found! Enter valid city name")
if st.button("Show graph"):
    if not city:
        st.write("Enter valid city and Get weather details to get graph")
    city = st.session_state.get("city","")
    if city:
        graph_url=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=87f2ab18ad43dd7a4e058ffb31ef69a7"
        r=requests.get(graph_url)
        data=r.json()
        temps=[]
        times=[]
        for item in data['list']:
            temp=item['main']['temp']
            temp=round(temp-273.15,2)
            temps.append(temp)
            time=item['dt_txt']
            dt = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
            times.append(dt.strftime("%m-%d %H:%M"))
        graph_data = pd.DataFrame({"Temperature (°C)": temps}, index=times)
        st.line_chart(graph_data)