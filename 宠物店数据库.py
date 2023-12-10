import sqlite3
import pandas as pd
import random
import winsound
from colorama import Fore


class 宠物店数据库:
    def __init__(self, db_name="pets.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pets (
                ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Species TEXT,
                Breed TEXT,
                DateOfBirth DATE,
                HairType TEXT,
                HairColor TEXT,
                Size TEXT CHECK(Size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
                Castrated TEXT CHECK(Castrated IN ('Yes', 'No'))
            )
        """
        )
        self.conn.commit()
    
    #^the table :3

    def add_pet(self, data):
        valid_castrated_values = ["Yes", "No"]
        valid_size_values = ["XS", "S", "M", "L", "XL", "XXL"]
        valid_hair_type_values = ["Long", "Short"]

        castrated = data.get("Castrated")
        if castrated not in valid_castrated_values:
            print(
                f"Invalid value for Castrated. Valid options: {', '.join(valid_castrated_values)}."
            )
            return

        size = data.get("Size")
        if size not in valid_size_values:
            print(
                f"Invalid value for Size. Valid options: {', '.join(valid_size_values)}."
            )
            return

        hair_type = data.get("HairType")
        if hair_type not in valid_hair_type_values:
            print(
                f"Invalid value for HairType. Valid options: {', '.join(valid_hair_type_values)}."
            )
            return
        
        #^These lines of code up here make sure that you don't input something that I don't want in the table :3
        
        data["ID"] = random.randint(100000, 999999) 
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        values = tuple(data.values())

        self.cursor.execute(
            f"INSERT INTO pets ({columns}) VALUES ({placeholders})", values
        )
        self.conn.commit()

    def get_all_pets(self):
        self.cursor.execute("SELECT * FROM pets")
        columns = [desc[0] for desc in self.cursor.description]
        return pd.DataFrame(self.cursor.fetchall(), columns=columns)

    def remove_pet(self, pet_id):
        self.cursor.execute("DELETE FROM pets WHERE ID = ?", (pet_id,))
        self.conn.commit()

    def hard_reset(self):
        self.cursor.execute("DELETE FROM pets")
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


def main():
    pet_db = 宠物店数据库()

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Pet")
        print("2. Remove Pet")
        print("3. See Pets")
        print("4. 消灭野兽")
        print("5. Close")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            pet_data = {
                "Name": input("Enter pet's name: "),
                "Species": input("Enter species(Ex: Dog): "),
                "Breed": input("Enter breed: "),
                "DateOfBirth": input("Enter date of birth (DD/MM/YYYY): "),
                "HairType": input("Enter hair type(Long/Short): "),
                "HairColor": input("Enter hair color: "),
                "Size": input("Enter size(XS/S/M/L/XL/XXL): "),
                "Castrated": input("Is the pet castrated? (Yes/No): "),
            }
            pet_db.add_pet(pet_data)
            print("Pet added successfully!")
            winsound.PlaySound("Correct sound effect.wav", winsound.SND_FILENAME)

        elif choice == "2":
            pet_id = input("Enter the ID of the pet to remove: ")
            pet_db.remove_pet(pet_id)
            print("Pet removed successfully!")

        elif choice == "3":
            all_pets = pet_db.get_all_pets()
            print(all_pets)

        elif choice == "4":
            confirm = input("你想要灾难吗？(yes/no): ")
            if confirm.lower() == "yes":
                pet_db.hard_reset()
                print("结束了...")
            else:
                print("我不会说中文.")

        elif choice == "5":
            pet_db.close_connection()
            print("Exiting the program...")
            print("再见!")
            winsound.PlaySound("Half-Life Death Sound", winsound.SND_FILENAME)
            break

        else:
            print(Fore.RED + "LOUD INCORRECT BUZZER" + Fore.RESET)
            winsound.PlaySound("EXTREMELY LOUD INCORRECT BUZZER", winsound.SND_FILENAME)
            #DO NOT input anything that it is not inbetween 1-5 if you value your eardrums...

if __name__ == "__main__":
    main()
