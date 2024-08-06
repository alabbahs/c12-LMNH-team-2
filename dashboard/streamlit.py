import pandas as pd
import streamlit as st
import altair as alt


class dashboard:
    def __init__(self) -> None:
        pass

    def fetch_data(self) -> pd.DataFrame:
        return pd.read_parquet("test_data.parquet")

    def temp_graph(self, plant: pd.DataFrame):
        temp_stats = plant[["recording_taken", "temperature"]]

        min_temperature = temp_stats["temperature"].min(
        ) - temp_stats['temperature'].min()*0.01
        max_temperature = temp_stats["temperature"].max(
        ) + temp_stats["temperature"].max()*0.01

        base_chart = alt.Chart(temp_stats).encode(
            x=alt.X('recording_taken:T', title='Time'),
            y=alt.Y('temperature:Q', title='Temperature', scale=alt.Scale(
                domain=[min_temperature, max_temperature]))
        )

        area_chart = base_chart.mark_area(
            line={'color': 'red'},
            interpolate='step-after',
            color='salmon',  # Using a solid fill color
            clip=True  # Clip ensures area does not exceed axis bounds
        ).properties(title="Soil Temperature over time")

        points = base_chart.mark_point(
            filled=True,
            color='red'
        )

        return area_chart + points

    def moisture_graph(self, plant: pd.DataFrame):

        moisture_stats = plant[["recording_taken", "soil_moisture"]]

        min_soil_moisture = moisture_stats["soil_moisture"].min(
        ) - moisture_stats["soil_moisture"].min()*0.01
        max_soil_moisture = moisture_stats["soil_moisture"].max(
        ) + moisture_stats["soil_moisture"].max()*0.01

        base_chart = alt.Chart(moisture_stats).encode(
            x=alt.X('recording_taken:T', title='Time'),
            y=alt.Y('soil_moisture:Q', title='Soil Moisture', scale=alt.Scale(
                domain=[min_soil_moisture, max_soil_moisture]))
        )

        area_chart = base_chart.mark_area(
            line={'color': 'blue'},
            interpolate='step-after',
            color='lightblue',
            clip=True
        ).properties(title="Soil Moisture over time")

        points = base_chart.mark_point(
            filled=True,
            color='blue'
        )
        return area_chart + points

    def generate_dashboard(self, data: pd.DataFrame) -> None:
        st.set_page_config(layout="wide")
        st.title("Liverpool Natural History Museum Plant Heath Monitor")
        st.write(
            "Welcome to the plant heath monitor!, to start please choose a plant to monitor")
        id_selected = st.selectbox(
            "Select a Plant ID", data["plant_id"])

        if id_selected:
            plant = data.loc[data['plant_id'] == id_selected]
            st.header(next(iter(set(plant["name"].values))))
            col1, col2, = st.columns(2)
            with col1:
                st.altair_chart(self.moisture_graph(plant))
            with col2:
                st.altair_chart(self.temp_graph(plant))
            with st.expander("Botantist Details"):
                st.write(f"Name:{
                         next(iter(set(plant["botanist_name"])))}")
                st.write(f"Phone Number:{
                         next(iter(set(plant["botanist_phone"])))}")
                st.write(f"Email:{
                         next(iter(set(plant["botanist_email"])))}")
            with st.expander("Location Details"):
                st.write(f"Region:{
                         next(iter(set(plant["origin_location_region"])))}")
                st.write(f"City:{
                         next(iter(set(plant["origin_location_city_name"])))}")
                st.write(f"Country Code:{
                         next(iter(set(plant["origin_location_country_code"])))}")
                st.write(f"Longitude:{
                    next(iter(set(plant["origin_location_longitude"])))}")
                st.write(f"Latitude:{
                    next(iter(set(plant["origin_location_latitude"])))}")


if __name__ == "__main__":
    plant_dashboard = dashboard()
    data = plant_dashboard.fetch_data()
    plant_dashboard.generate_dashboard(data)
