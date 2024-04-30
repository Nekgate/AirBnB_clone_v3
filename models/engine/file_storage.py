#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of
all class instances effectively
"""
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

# New import
from models.engine.db_storage import classes

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """handles long term storage of all class instances"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """
    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """returns private attribute: __objects"""
        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """sets / updates in __objects the obj with key <obj class name>.id"""
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        with open(fname, mode='w+', encoding='utf-8') as f_io:
            json.dump(d, f_io)

    def reload(self):
        """if file exists, deserializes JSON file to __objects, else nothing"""
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except Exception:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            d.pop("__class__", None)
            d["created_at"] = datetime.strptime(d["created_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            d["updated_at"] = datetime.strptime(d["updated_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """deletes obj"""
        if obj is None:
            return
        for k in list(FileStorage.__objects.keys()):
            if obj.id == k.split(".")[1] and k.split(".")[0] in str(obj):
                FileStorage.__objects.pop(k, None)
                self.save()

    def close(self):
        """
            calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or None if not found
        """
        if cls and id:
            if cls in classes.values():
                all_objects = self.all(cls)

                for value in all_objects.values():
                    if value.id == id:
                        return value
            return
        return

    def count(self, cls=None):
        """
        Counts the number of objects in storage.
         """
        if not cls:
            inst_of_all_cls = self.all()
            return len(inst_of_all_cls)

        for class_name, value in classes.items():
            if cls == class_name or cls == value:
                all_inst_of_prov_cls = self.all(cls)
                return len(all_inst_of_prov_cls)

        if cls not in classes.values():

            return
