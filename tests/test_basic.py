# -*- coding: utf-8 -*-

from pickle import FALSE
from .context import wamr
from wamr.ffi import *

import unittest


class BasicTestSuite(unittest.TestCase):
    def test_wasm_valkind(self):
        self.assertEqual(
            [WASM_I32, WASM_I64, WASM_F32, WASM_F64, WASM_ANYREF, WASM_FUNCREF],
            [0, 1, 2, 3, 4, 128, 129],
        )

    def test_wasm_mutability(self):
        self.assertEqual(
            [WASM_CONST, WASM_VAR],
            [0, 1],
        )

    def test_wasm_valkind_ex(self):
        pass

    def test_wasm_valkind_is_num(self):
        self.assertTrue(wasm_valkind_is_num(WASM_I64))
        self.assertTrue(wasm_valkind_is_num(WASM_F64))
        self.assertFalse(wasm_valkind_is_num(WASM_ANYREF))
        self.assertFalse(wasm_valkind_is_num(WASM_FUNCREF))

    def test_wasm_valkind_is_num_ex(self):
        self.assertFalse(wasm_valkind_is_num(None))
        self.assertFalse(wasm_valkind_is_num(7))

    def test_wasm_valkind_is_ref(self):
        self.assertFalse(wasm_valkind_is_ref(WASM_I64))
        self.assertFalse(wasm_valkind_is_ref(WASM_F64))
        self.assertTrue(wasm_valkind_is_ref(WASM_ANYREF))
        self.assertTrue(wasm_valkind_is_ref(WASM_FUNCREF))

    def test_wasm_valkind_is_ref_ex(self):
        self.assertFalse(wasm_valkind_is_ref(None))
        self.assertFalse(wasm_valkind_is_ref(199))

    def test_wasm_valtype_new(self):
        self.assertIsNone(wasm_valtype_new(WASM_I32))

    def test_wasm_valtype_new_ex(self):
        self.assertIsNone(wasm_valtype_new(None))
        self.assertIsNone(wasm_valtype_new(37))

    def test_wasm_valtype_kind(self):
        self.assertEqual(wasm_valtype_kind(wasm_valtype_new(WASM_I64)), WASM_I64)

    def test_wasm_valtype_kind_ex(self):
        self.assertNotEqual(wasm_valtype_kind(wasm_valtype_new(5)), WASM_I32)

    def test_wasm_valtype_is_num(self):
        self.assertTrue(wasm_valtype_is_num(wasm_valtype_new(WASM_F32)))
        self.assertTrue(wasm_valtype_is_num(wasm_valtype_new(WASM_F64)))

    def test_wasm_valtype_is_num_ex(self):
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(None)))
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(5)))
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(130)))

    def test_wasm_valtype_is_ref(self):
        self.assertTrue(wasm_valtype_is_ref(wasm_valtype_new(WASM_ANYREF)))
        self.assertTrue(wasm_valtype_is_ref(wasm_valtype_new(WASM_FUNCREF)))

    def test_wasm_valtype_is_ref_ex(self):
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(None)))
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(5)))
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(130)))

    def test_wasm_valtype_delete(self):
        self.assertIsNone(wasm_valtype_delete(wasm_valtype_new(WASM_ANYREF)))

    def test_wasm_valtype_delete_ex(self):
        self.assertIsNone(wasm_valtype_delete(None))

    def test_wasm_valtype_copy(self):
        vt1 = wasm_valtype_new(WASM_FUNCREF)
        vt2 = wasm_valtype_copy(vt1)
        self.assertEqual(wasm_valtype_kind(vt1), wasm_valtype_kind(vt2))

    def test_wasm_valtype_copy_ex(self):
        self.assertIsNone(wasm_valtype_copy(None))
    
    def test_wasm_globaltype_new_happy_path(self):
        vt = wasm_valtype_new(WASM_FUNCREF) 
        mut = True
        self.assertIsNotNone(wasm_globaltype_new(vt, mut)) 

    def test_wasm_globaltype_new_sideway(self):
        vt = wasm_valtype_new(None) 
        mut = True
        self.assertIsNone(wasm_globaltype_new(vt, mut)) 

    def test_wasm_globaltype_delete_happy_path(self):
        vt = wasm_valtype_new(WASM_ANYREF) 
        mut = True
        self.assertIsNone(wasm_globaltype_delete(wasm_globaltype_new(vt, mut))) 

    def test_wasm_globaltype_delete_sideway(self):
        self.assertIsNone(wasm_globaltype_delete(None)) 

    def test_wasm_globaltype_content(self):
        vt = wasm_valtype_new(WASM_FUNCREF) 
        mut = True
        gt = wasm_globaltype_new(vt, mut)
        self.assertEqual(vt, wasm_globaltype_content(gt))

    def test_wasm_globaltype_mutability(self):
        vt1 = wasm_valtype_new(WASM_F32) 
        mut1 = FALSE
        gt1 = wasm_globaltype_new(vt1, mut1)
        self.assertEqual(WASM_CONST, wasm_globaltype_mutability(gt1))
        vt2 = wasm_valtype_new(WASM_F32) 
        mut2 = True
        gt2 = wasm_globaltype_new(vt2, mut2)
        self.assertEqual(WASM_VAR, wasm_globaltype_mutability(gt2))
    
    def test_wasm_globaltype_copy(self):
        vt = wasm_valtype_new(WASM_I32) 
        mut = True
        gt1 = wasm_globaltype_new(vt, mut)
        gt2 = wasm_globaltype_copy(gt1)
        self.assertEqual(gt1, gt2) 

    def test_wasm_engine_new(self):
        self.assertIsNotNone(wasm_engine_new())

    # wasm_egnine_new() should always return a wasm_engine_t
    def test_wasm_engine_new_ex(self):
        pass

    def test_wasm_store_new(self):
        engine = wasm_engine_new()
        self.assertIsNotNone(wasm_store_new(engine))

    def test_wasm_store_new_ex(self):
        self.assertIsNone(wasm_store_new(None))


if __name__ == "__main__":
    unittest.main()
