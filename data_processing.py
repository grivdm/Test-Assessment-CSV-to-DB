from sqlalchemy import desc, func
import matplotlib.pyplot as plt
import pandas as pd

from models import Restaurant, Category, FoodItem, SubCategory, FoodItemSubcategory
from session import DBSession


class DataVizualizer:
    '''
    This class is responsible for visualizing the data
    '''

    def __init__(self) -> None:
        pass

    def query(self, session):
        # Get data from  DB
        return session.query(
            Restaurant.name,
            func.avg(FoodItem.calories).label('avg_calories'),
            func.min(FoodItem.calories).label('min_calories'),
            func.max(FoodItem.calories).label('max_calories'),
            func.avg(FoodItem.total_carb).label('avg_carbs')
        ).join(FoodItem).group_by(Restaurant.name).order_by('avg_carbs').limit(5).all()

    def visualize_data(self, query):
        df = pd.DataFrame(query, columns=[
                          'Restaurant', 'Average Calories', 'Min Calories', 'Max Calories', 'Average Carbs'])
        df['Average Calories'] = pd.to_numeric(
            df['Average Calories'], errors='coerce')
        df['Average Carbs'] = pd.to_numeric(
            df['Average Carbs'], errors='coerce')
        print(df)

        # Visualize the data
        df.plot(x='Restaurant', kind='bar')
        plt.title('Top 5 restaurants  that have the least amount of carbs')
        plt.ylabel('Carbs')
        plt.xlabel('Restaurant')
        plt.show()


class DataExporter:
    '''
    This class is responsible for exporting the data
    '''

    def __init__(self) -> None:
        pass

    def export_data(self, query, file_name: str = 'food_cats.csv'):
        # Convert the query result to a DataFrame
        df = pd.read_sql(query.statement, query.session.bind)

        # Export the DataFrame to CSV
        df.to_csv(file_name, index=False)


class DataProcessor:
    '''
    This class is responsible for processing the data
    '''

    def __init__(self) -> None:
        pass

    def query(self, session):
        '''
        This query returns the data about food items, categories and subcategories
        REMARK: items with multiple subcategories are repeated
        '''
        query = session.query(
            Restaurant.name.label('restaurant'),
            FoodItem.name.label('food_item'),
            FoodItem.calories.label('calories'),
            FoodItem.cal_fat.label('cal_fat'),
            FoodItem.total_fat.label('total_fat'),
            FoodItem.sat_fat.label('sat_fat'),
            FoodItem.trans_fat.label('trans_fat'),
            FoodItem.cholesterol.label('cholesterol'),
            FoodItem.sodium.label('sodium'),
            FoodItem.total_carb.label('total_carb'),
            FoodItem.fiber.label('fiber'),
            FoodItem.sugar.label('sugar'),
            FoodItem.protein.label('protein'),
            FoodItem.vit_a.label('vit_a'),
            FoodItem.vit_c.label('vit_c'),
            FoodItem.calcium.label('calcium'),
            FoodItem.salad.label('salad'),
            Category.name.label('category'),
            SubCategory.name.label('subcategory')


        ).join(
            Restaurant, FoodItem.restaurant_id == Restaurant.id).join(
            Category, FoodItem.category_id == Category.id).outerjoin(
            FoodItemSubcategory, FoodItem.id == FoodItemSubcategory.food_item_id).outerjoin(
            SubCategory, FoodItemSubcategory.subcategory_id == SubCategory.id).order_by('restaurant')
        return query


def calculate_rank_and_upload():
    # Get the data
    data_vizualizer = DataVizualizer()
    data_exporter = DataExporter()
    data_processor = DataProcessor()

    with DBSession() as session:
        query_vizualization = data_vizualizer.query(session)

        query_processor = data_processor.query(session)

    data_vizualizer.visualize_data(query_vizualization)
    data_exporter.export_data(query_processor)


if __name__ == "__main__":
    calculate_rank_and_upload()
