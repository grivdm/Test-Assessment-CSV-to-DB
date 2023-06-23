from typing import Any, Dict, List
import pandas as pd
import sqlalchemy
from models import Restaurant, Category, FoodItem, SubCategory, FoodItemSubcategory
from session import DBSession


'''
Because of free-interpretation of choosing categories, I will use the following rules:
- Main: if the item name contains any of the following keywords: burger, sandwich, chicken, beef, fish, sub, taco, or if the calories are greater than 199
- Side: if the item name contains any of the following keywords: fries, salad, piece, and the calories are less than 199, protein is less than or equal to 10, and sugar is less than or equal to 15
- Dessert: if the item name contains any of the following keywords: cake, ice cream, pie, or if the sugar is greater than 15
- Other: if the item does not fall into any of the above categories
The same approach as in categorizing will be used and for the subcategories:
- Beef: if the item name contains any of the following keywords: beef, burger
- Chicken: if the item name contains any of the following keywords: chicken, sandwich
- Seafood: if the item name contains any of the following keywords: fish, seafood
- Pork: if the item name contains any of the following keywords: pork, ham
'''
category_rules: Dict[str, Dict[str, Any]] = {
    'Main': {'keywords': ['burger', 'sandwich', 'chicken', 'beef', 'fish', 'sub', 'taco'], 'calories': 199},
    'Side': {'keywords': ['fries', 'salad', 'piece'], 'calories': 199, 'protein': 10, 'sugar': 15},
    'Dessert': {'keywords': ['cake', 'ice cream', 'pie'], 'sugar': 15}
}

# Define the keywords for each subcategory in a dict
subcategory_rules: Dict[str, List[str]] = {
    'Beef': ['beef', 'burger'],
    'Chicken': ['chicken', 'sandwich'],
    'Seafood': ['fish', 'seafood'],
    'Pork': ['pork', 'ham', 'bacon']
}

categories_list: List = ['Main', 'Side', 'Dessert', 'Other']
subcategories_list: List = [
    'Beef', 'Chicken', 'Seafood', 'Pork', 'Other']
column_list: List = ('restaurant', 'item', 'calories', 'cal_fat', 'total_fat', 'sat_fat', 'trans_fat',
                      'cholesterol', 'sodium', 'total_carb', 'fiber', 'sugar', 'protein', 'vit_a', 'vit_c', 'calcium', 'salad')


class RestaurantMenuHandler:
    def __init__(self, name: str, restarunt_data: pd.DataFrame):
        self.name = name
        self.data = restarunt_data  # data from CSV

    def get_items_names(self) -> List[str]:
        return self.data['item'].tolist()

    def get_existed_items_from_db(self, session) -> set:

        # Fetch names of existing food items from the database for a specific restaurant and a specific list of food items
        existed_items = session.query(FoodItem.name).join(Restaurant).filter(
            (Restaurant.name == self.name) & FoodItem.name.in_(self.get_items_names())).all()

        # Create a set of food item names
        existed_items = {item_name for item_name, in existed_items}
        return existed_items

    def find_nonexisted_items(self, session) -> set:
        return set(self.get_items_names()) - self.get_existed_items_from_db(session)

    def get_nonexisted_items(self, session) -> pd.DataFrame:
        return self.data[self.data['item'].isin(self.find_nonexisted_items(session))]

    @staticmethod
    def _categorize_food(row: pd.Series) -> str:

        if any(kword in row['item'].lower() for kword in category_rules['Side']['keywords']) and (row['calories'] < category_rules['Side']['calories'] or row['protein'] <= category_rules['Side']['protein'] or row['sugar'] <= category_rules['Side']['sugar']):
            return 'Side'
        elif any(kword in row['item'].lower() for kword in category_rules['Main']['keywords']) or row['calories'] > category_rules['Main']['calories']:
            return 'Main'
        elif any(kword in row['item'].lower() for kword in category_rules['Dessert']['keywords']) or row['sugar'] > category_rules['Dessert']['sugar']:
            return 'Dessert'
        else:
            return 'Other'

    @staticmethod
    def _subcategorize_main_food(row: pd.Series) -> List[str]:

        subCategories: List[str] = []

        if any(kword in row['item'].lower() for kword in subcategory_rules['Beef']):
            subCategories.append('Beef')
        if any(kword in row['item'].lower() for kword in subcategory_rules['Chicken']):
            subCategories.append('Chicken')
        if any(kword in row['item'].lower() for kword in subcategory_rules['Seafood']):
            subCategories.append('Seafood')
        if any(kword in row['item'].lower() for kword in subcategory_rules['Pork']):
            subCategories.append('Pork')

        if not subCategories:
            subCategories.append('Other')
        return subCategories

    def attach_category_and_subcategories(self, item_row: pd.Series,
                                          categories_dict: Dict[str, Category],
                                          subcategories_dict: Dict[str, SubCategory]) -> List[Category | List[SubCategory]]:
        '''
        Attach a category and subcategories to a food item
        '''
        # Get the item category

        category = categories_dict.get(self._categorize_food(item_row))
        # Get the item subcategories if the category is Main
        subcategories = [subcategories_dict.get(name) for name in self._subcategorize_main_food(
            item_row)] if category.name == 'Main' else []
        return category, subcategories


class EntityHandler:
    '''
    Universal entity handler for creating and getting entities (restaurants, categories, subcategories) in DB
    '''
    def __init__(self, session) -> None:
        self.session = session

    def get_or_create_entities(self, entities: List[str], entity_type: str) -> Dict[str, Any]:

        if entity_type == 'Restaurant':
            existing_entities = {
                entity.name: entity for entity in self.session.query(Restaurant).all()}
            Entity = Restaurant
        elif entity_type == 'Category':
            existing_entities = {
                entity.name: entity for entity in self.session.query(Category).all()}
            Entity = Category
        elif entity_type == 'SubCategory':
            existing_entities = {
                entity.name: entity for entity in self.session.query(SubCategory).all()}
            Entity = SubCategory

        for _entity in entities:
            entity = existing_entities.get(_entity)
            if not entity:
                entity = Entity(name=_entity)
                self.session.add(entity)
                existing_entities[_entity] = entity
        self.session.flush()
        return existing_entities


class DataParser:
    '''
    Data parser for reading and validating the data from CSV
    '''
    def __init__(self, filename: str):
        self.filename = filename

    def read_csv(self) -> pd.DataFrame:
        # Read the CSV file
        try:
            return pd.read_csv(self.filename)
        except FileNotFoundError:
            raise FileNotFoundError('File not found in the root directory')

    def validate_data(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        '''validate and clean the data (change NaN values to 0)'''
        # Check if the data frame is empty
        if data_frame.empty:
            raise ValueError('The data frame is empty')

        # Check if the data frame contains the required columns

        if not all(column in data_frame.columns for column in column_list):
            raise ValueError(
                'The DataFrame does not contains the required columns')

        return data_frame.fillna(sqlalchemy.sql.null())

    # ->  DataFrameGroupBy[Scalar]
    def group_by_restaurant(self) -> pd.DataFrame:
        # Group the data by restaurant
        grouped = self.validate_data(self.read_csv()).groupby('restaurant')
        return grouped

    def get_restaurants_names(self) -> List[str]:
        # Get the names of restaurants
        return self.group_by_restaurant().groups.keys()

    def get_restaurant_data(self, restaurant_name: str) -> pd.DataFrame:

        # Get the data for a specific restaurant
        return self.group_by_restaurant().get_group(restaurant_name)


def load_restaurants_data_from_csv_to_db(filename: str):
    # Create a data parser
    data_parser = DataParser(filename)

    # Get the names of restaurants
    restaurants_names = data_parser.get_restaurants_names()

    # Open a DB session
    with DBSession() as session:

        # Create a DB entity handler and get or create the entities (restaurants, categories, subcategories)
        handler = EntityHandler(session)

        restaurant_entities = handler.get_or_create_entities(
            restaurants_names, 'Restaurant')
        category_entities = handler.get_or_create_entities(
            categories_list, 'Category')
        subcategory_entities = handler.get_or_create_entities(
            subcategories_list, 'SubCategory')

        # Iterate over the restaurants names
        for restaurant_name in restaurants_names:

            restaurant_menu = RestaurantMenuHandler(
                restaurant_name, data_parser.get_restaurant_data(restaurant_name))

    # Iterate over non-existed items in DB
            for _, item_row in restaurant_menu.get_nonexisted_items(session).iterrows():

                # Get the category and subcategories of the food item
                category, subcategories = restaurant_menu.attach_category_and_subcategories(
                    item_row, category_entities, subcategory_entities)
                # Create a new food item and add it to the session
                food_item = FoodItem(
                    name=item_row['item'],
                    calories=item_row['calories'],
                    cal_fat=item_row['cal_fat'],
                    total_fat=item_row['total_fat'],
                    sat_fat=item_row['sat_fat'],
                    trans_fat=item_row['trans_fat'],
                    cholesterol=item_row['cholesterol'],
                    sodium=item_row['sodium'],
                    total_carb=item_row['total_carb'],
                    fiber=item_row['fiber'],
                    sugar=item_row['sugar'],
                    protein=item_row['protein'],
                    vit_a=item_row['vit_a'],
                    vit_c=item_row['vit_c'],
                    calcium=item_row['calcium'],
                    salad=item_row['salad'],
                    restaurant_id=restaurant_entities[restaurant_name].id,
                    category_id=category.id,
                )
                session.add(food_item)

                session.flush()

                # Add the food item to the corresponding subcategories
                for subcategory in subcategories:
                    food_item_subcategory = FoodItemSubcategory(
                        food_item_id=food_item.id, subcategory_id=subcategory.id)
                    session.add(food_item_subcategory)

                session.flush()

            session.commit()
