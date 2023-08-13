#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_mod1 = BaseModel()
        base_mod2 = BaseModel()
        self.assertNotEqual(base_mod1.id, base_mod2.id)

    def test_two_models_different_created_at(self):
        base_mod1 = BaseModel()
        sleep(0.05)
        base_mod2 = BaseModel()
        self.assertLess(base_mod1.created_at, base_mod2.created_at)

    def test_two_models_different_updated_at(self):
        base_mod1 = BaseModel()
        sleep(0.05)
        base_mod2 = BaseModel()
        self.assertLess(base_mod1.updated_at, base_mod2.updated_at)

    def test_str_representation(self):
        dat_time = datetime.today()
        dat_time_repr = repr(dat_time)
        base_mod = BaseModel()
        base_mod.id = "123456"
        base_mod.created_at = base_mod.updated_at = dat_time
        base_modstr = base_mod.__str__()
        self.assertIn("[BaseModel] (123456)", base_modstr)
        self.assertIn("'id': '123456'", base_modstr)
        self.assertIn("'created_at': " + dat_time_repr, base_modstr)
        self.assertIn("'updated_at': " + dat_time_repr, base_modstr)

    def test_args_unused(self):
        base_mod = BaseModel(None)
        self.assertNotIn(None, base_mod.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dat_time = datetime.today()
        dat_time_iso = dat_time.isoformat()
        base_mod = BaseModel(id="345", created_at=dat_time_iso, updated_at=dat_time_iso)
        self.assertEqual(base_mod.id, "345")
        self.assertEqual(base_mod.created_at, dat_time)
        self.assertEqual(base_mod.updated_at, dat_time)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dat_time = datetime.today()
        dat_time_iso = dat_time.isoformat()
        base_mod = BaseModel("12", id="345", created_at=dat_time_iso, updated_at=dat_time_iso)
        self.assertEqual(base_mod.id, "345")
        self.assertEqual(base_mod.created_at, dat_time)
        self.assertEqual(base_mod.updated_at, dat_time)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_mod = BaseModel()
        sleep(0.05)
        first_updated_at = base_mod.updated_at
        base_mod.save()
        self.assertLess(first_updated_at, base_mod.updated_at)

    def test_two_saves(self):
        base_mod = BaseModel()
        sleep(0.05)
        first_updated_at = base_mod.updated_at
        base_mod.save()
        second_updated_at = base_mod.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_mod.save()
        self.assertLess(second_updated_at, base_mod.updated_at)

    def test_save_with_arg(self):
        base_mod = BaseModel()
        with self.assertRaises(TypeError):
            base_mod.save(None)

    def test_save_updates_file(self):
        base_mod = BaseModel()
        base_mod.save()
        base_modid = "BaseModel." + base_mod.id
        with open("file.json", "r") as f:
            self.assertIn(base_modid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_mod = BaseModel()
        self.assertTrue(dict, type(base_mod.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        base_mod = BaseModel()
        self.assertIn("id", base_mod.to_dict())
        self.assertIn("created_at", base_mod.to_dict())
        self.assertIn("updated_at", base_mod.to_dict())
        self.assertIn("__class__", base_mod.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_mod = BaseModel()
        base_mod.name = "Holberton"
        base_mod.my_number = 98
        self.assertIn("name", base_mod.to_dict())
        self.assertIn("my_number", base_mod.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_mod = BaseModel()
        base_mod_dict = base_mod.to_dict()
        self.assertEqual(str, type(base_mod_dict["created_at"]))
        self.assertEqual(str, type(base_mod_dict["updated_at"]))

    def test_to_dict_output(self):
        dat_time = datetime.today()
        base_mod = BaseModel()
        base_mod.id = "123456"
        base_mod.created_at = base_mod.updated_at = dat_time
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dat_time.isoformat(),
            'updated_at': dat_time.isoformat()
        }
        self.assertDictEqual(base_mod.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        base_mod = BaseModel()
        self.assertNotEqual(base_mod.to_dict(), base_mod.__dict__)

    def test_to_dict_with_arg(self):
        base_mod = BaseModel()
        with self.assertRaises(TypeError):
            base_mod.to_dict(None)


if __name__ == "__main__":
    unittest.main()