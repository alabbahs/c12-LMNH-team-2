import pandas as pd
import os
import streamlit as st
import altair as alt
import pyodbc
import logging
from dotenv import load_dotenv

load_dotenv('.env')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:

    @staticmethod
    def connect_to_db(db_host: str = DB_HOST, db_port: str = DB_PORT,
                      db_user: str = DB_USER, db_password: str = DB_PASSWORD,
                      db_name: str = DB_NAME):
        """Connects to the Microsoft SQL Server database"""
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={
                db_host},{db_port};DATABASE={db_name};UID={db_user};PWD={db_password}"
            connection = pyodbc.connect(connection_string)
            logger.info("Database connection established successfully.")
            return connection
        except Exception as e:
            logger.error("Failed to connect to the database: %s", e)
            raise

    @staticmethod
    def fetch_data_from_tables(connection):
        """Fetches data from two tables and returns as dataframes"""
        try:
            query1 = "SELECT * FROM beta.reading"
            query2 = "SELECT * FROM beta.plant"
            query3 = "SELECT * FROM beta.region"
            query4 = "SELECT * FROM beta.botanist"

            reading_df = pd.read_sql(query1, connection)
            plant_df = pd.read_sql(query2, connection)
            region_df = pd.read_sql(query3, connection)
            botanist_df = pd.read_sql(query4, connection)

            logger.info("Data fetched successfully from tables.")
            return reading_df, plant_df, region_df, botanist_df
        except Exception as e:
            logger.error("Failed to fetch data from tables: %s", e)
            raise


class dashboard:
    def __init__(self) -> None:
        pass

    def fetch_data(self) -> pd.DataFrame:
        return pd.read_parquet("test_data.parquet")

    def temp_graph(self, plant: pd.DataFrame) -> alt.Chart:
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
            color='salmon',
            clip=True  # Clip ensures area does not exceed axis bounds
        ).properties(title="Soil Temperature over time")

        points = base_chart.mark_point(
            filled=True,
            color='red'
        )

        return area_chart + points

    def moisture_graph(self, plant: pd.DataFrame) -> alt.Chart:

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

    def generate_dashboard(self, reading_df, plant_df, region_df, botanist_df) -> None:
        st.set_page_config(layout="wide")
        st.title("Liverpool Natural History Museum Plant Health Monitor")
        st.write(
            "Welcome to the plant health monitor!, to start please choose a plant to monitor")
        id_selected = st.selectbox(
            "Select a Plant ID", plant_df["plant_id"])

        if id_selected:

            plant_reading = reading_df.loc[reading_df['plant_id']
                                           == id_selected]
            plant_info = plant_df.loc[plant_df['plant_id']
                                      == id_selected]
            plant_botanist = botanist_df.loc[botanist_df['botanist_id']
                                             == plant_info.iloc[0]['botanist_id']]
            plant_region = region_df.loc[region_df['region_id']
                                         == plant_info.iloc[0]['region_id']]
            st.header(f"{plant_info.iloc[0]['name']}")
            if plant_info.iloc[0]['scientific_name']:
                st.write(plant_info.iloc[0]['scientific_name'])
            col1, col2, = st.columns(2)
            with col1:
                st.altair_chart(self.moisture_graph(plant_reading))
            with col2:
                st.altair_chart(self.temp_graph(plant_reading))

            with st.expander("Botanist Details"):
                st.write(f"Name: {
                         plant_botanist.iloc[0]["name"]}")
                st.write(f"Phone Number: {
                         plant_botanist.iloc[0]["phone"]}")
                st.write(f"Email: {
                         plant_botanist.iloc[0]["email"]}")
            with st.expander("Location Details "):
                st.write(f"Region: {
                         plant_region.iloc[0]["name"]}")
                st.write(f"City: {
                         plant_info.iloc[0]["origin_city"]}")
                st.write(f"Country Code: {
                         plant_info.iloc[0]["origin_country"]}")
                st.write(f"Longitude: {
                    plant_info.iloc[0]["origin_lon"]}")
                st.write(f"Latitude: {
                    plant_info.iloc[0]["origin_lat"]}")


if __name__ == "__main__":
    logger.info("Connecting to the database..")
    connection = DataLoader.connect_to_db()
    logger.info("Fetching data from tables..")
    reading_df, plant_df, region_df, botanist_df = DataLoader.fetch_data_from_tables(
        connection)

    plant_dashboard = dashboard()
    logger.info("Generating dashboard")
    plant_dashboard.generate_dashboard(
        reading_df, plant_df, region_df, botanist_df)
