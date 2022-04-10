# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) 2019 Intel Corporation.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#

from .context import wamr
from wamr.ffi import *

import unittest


class BasicTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._wasm_engine = wasm_engine_new()

    def assertIsNullPointer(self, pointer):
        self.assertFalse(pointer)

    def test_wasm_valkind_pos(self):
        self.assertEqual(
            [WASM_I32, WASM_I64, WASM_F32, WASM_F64, WASM_ANYREF, WASM_FUNCREF],
            [0, 1, 2, 3, 128, 129],
        )

    def test_wasm_valkind_neg(self):
        pass

    def test_wasm_valtype_new_pos(self):
        vt = wasm_valtype_new(WASM_I32)
        self.assertEqual(wasm_valtype_kind(vt), WASM_I32)

    def test_wasm_valtype_new_neg(self):
        self.assertIsNullPointer(wasm_valtype_new(37))

    def test_wasm_valtype_kind_pos(self):
        self.assertEqual(wasm_valtype_kind(wasm_valtype_new(WASM_I64)), WASM_I64)

    def test_wasm_valtype_kind_neg(self):
        self.assertIsNullPointer(wasm_valtype_new(5))

    def test_wasm_valtype_delete_pos(self):
        vt = wasm_valtype_new(WASM_ANYREF)
        wasm_valtype_delete(vt)
        self.assertNotEqual(wasm_valtype_kind(vt), WASM_ANYREF)

    def test_wasm_valtype_delete_neg(self):
        vt = wasm_valtype_new(37)
        wasm_valtype_delete(vt)
        self.assertIsNullPointer(vt)

    def test_wasm_valtype_copy_pos(self):
        vt1 = wasm_valtype_new(WASM_FUNCREF)
        vt2 = wasm_valtype_copy(vt1)
        self.assertEqual(wasm_valtype_kind(vt1), wasm_valtype_kind(vt2))

    def test_wasm_valtype_copy_neg(self):
        vt1 = wasm_valtype_new(37)
        vt2 = wasm_valtype_copy(vt1)
        self.assertIsNullPointer(vt2)

    def test_wasm_valtype_vec_new_pos(self):
        data_type = wasm_valtype_t * 3
        data = data_type()
        data[0] = wasm_valtype_new(WASM_I32)
        data[1] = wasm_valtype_new(WASM_F64)
        data[2] = wasm_valtype_new(WASM_ANYREF)

        v = wasm_valtype_vec_t()
        self.assertEqual(v.size, 0)
        wasm_valtype_vec_new(byref(v), 3, byref(data))
        self.assertEqual(v.size, 3)

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_new_neg(self):
        pass

    def test_wasm_valtype_vec_new_uninitialized_pos(self):
        v = wasm_valtype_vec_t()
        wasm_valtype_vec_new_uninitialized(byref(v), 10)

        self.assertIsNotNone(v)
        self.assertEqual(10, v.size)

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_new_uninitialized_neg(self):
        pass

    def test_wasm_valtype_vec_new_empty_pos(self):
        v = wasm_valtype_vec_t()
        wasm_valtype_vec_new_empty(byref(v))

        self.assertIsNotNone(v)
        self.assertEqual(0, v.size)

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_new_empty_neg(self):
        pass

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_copy_pos(self):
        pass

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_copy_neg(self):
        pass

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_delete_pos(self):
        pass

    @unittest.skip("TBD: redesign cases about wasm_xxx_vec_t")
    def test_wasm_valtype_vec_delete_neg(self):
        pass

    def test_wasm_globaltype_new_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        self.assertIsNotNone(wasm_globaltype_new(vt, True))

    def test_wasm_globaltype_new_neg(self):
        vt = wasm_valtype_new(None)
        self.assertIsNone(wasm_globaltype_new(vt, True))

    def test_wasm_globaltype_delete_pos(self):
        vt = wasm_valtype_new(WASM_ANYREF)
        gt = wasm_globaltype_new(vt, True)
        wasm_globaltype_delete(gt)

        self.assertIsNone(vt)
        self.assertIsNone(gt)

    def test_wasm_globaltype_delete_neg(self):
        self.assertIsNone(wasm_globaltype_delete(None))

    def test_wasm_globaltype_content_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        gt = wasm_globaltype_new(vt, True)
        self.assertEqual(vt, wasm_globaltype_content(gt))

    def test_wasm_globaltype_content_neg(self):
        self.assertIsNone(wasm_globaltype_content(None))

    def test_wasm_globaltype_mutability_pos(self):
        vt1 = wasm_valtype_new(WASM_F32)
        gt1 = wasm_globaltype_new(vt1, False)
        self.assertFalse(wasm_globaltype_mutability(gt1))

        vt2 = wasm_valtype_new(WASM_F32)
        gt2 = wasm_globaltype_new(vt2, True)
        self.assertTrue(wasm_globaltype_mutability(gt2))

    def test_wasm_globaltype_mutability_neg(self):
        self.assertIsNone(wasm_globaltype_mutability(None))

    def test_wasm_globaltype_copy_pos(self):
        vt = wasm_valtype_new(WASM_I32)
        gt1 = wasm_globaltype_new(vt, True)
        gt2 = wasm_globaltype_copy(gt1)
        self.assertEqual(gt1, gt2)

    def test_wasm_globaltype_copy_neg(self):
        self.assertIsNone(wasm_globaltype_copy(None))

    def test_wasm_tabletype_new_pos(self):
        vt = wasm_valtype_new(WASM_F32)
        wasm_limits_t = wasm_limits_t(min=0, max=0xFFFFFFFF)
        self.assertIsNotNone(wasm_tabletype_new(vt, wasm_limits_t))

    @unittest.skip("TBD: make sure if limits is null-able")
    def test_wasm_tabletype_new_neg(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        self.assertIsNone(wasm_tabletype_new(vt, None))

    def test_wasm_tabletype_delete_pos(self):
        vt = wasm_valtype_new(WASM_F32)
        tt = wasm_tabletype_new(vt, wasm_limits_t(0, 0xFFFFFFFF))
        wasm_tabletype_delete(tt)

        self.assertIsNone(vt)
        self.assertIsNone(tt)

    def test_wasm_tabletype_delete_neg(self):
        self.assertIsNone(wasm_tabletype_delete(None))

    def test_wasm_tabletype_element_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        tt = wasm_tabletype_new(vt, wasm_limits_t(0, 0xFFFFFFFF))
        self.assertEqual(vt, wasm_tabletype_element(tt))

    def test_wasm_tabletype_element_neg(self):
        self.assertIsNone(wasm_tabletype_element(None))

    def test_wasm_tabletype_limits_pos(self):
        wasm_limits_t = wasm_limits_t(min=0, max=0x0000FFFF)
        tt = wasm_tabletype_new(wasm_valtype_new(WASM_FUNCREF), wasm_limits_t)
        self.assertEqual(wasm_limits_t, wasm_tabletype_limits(tt))

    def test_wasm_tabletype_limits_neg(self):
        self.assertIsNone(wasm_tabletype_limits(None))

    def test_wasm_tabletype_copy_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        tt1 = wasm_tabletype_new(vt, wasm_limits_t(0, 0xFFFFFFFF))
        tt2 = wasm_tabletype_copy(tt1)
        self.assertEqual(tt1, tt2)

    def test_wasm_tabletype_copy_neg(self):
        self.assertIsNone(wasm_tabletype_copy(None))

    def test_wasm_memorytype_new_pos(self):
        wasm_limits_t = wasm_limits_t(min=0, max=0xFFFFFFFF)
        self.assertIsNotNone(wasm_memorytype_new(wasm_limits_t))

    def test_wasm_memorytype_new_neg(self):
        self.assertIsNone(wasm_memorytype_new(None))

    def test_wasm_memorytype_delete_pos(self):
        wasm_limits_t = wasm_limits_t(min=0, max=0xFFFFFFFF)
        mt = wasm_memorytype_new(wasm_limits_t)
        wasm_memorytype_delete(mt)

        self.assertIsNone(mt)

    def test_wasm_memorytype_delete_neg(self):
        self.assertIsNone(wasm_memorytype_delete(None))

    def test_wasm_memorytype_limits_pos(self):
        wasm_limits_t = wasm_limits_t(min=0, max=0xFFFFFFFF)
        mt = wasm_memorytype_new(wasm_limits_t)
        self.assertEqual(wasm_limits_t, wasm_memorytype_limits(mt))

    def test_wasm_memorytype_limits_neg(self):
        self.assertIsNone(wasm_memorytype_limits(None))

    def test_wasm_memorytype_copy_pos(self):
        wasm_limits_t = wasm_limits_t(min=0, max=0xFFFFFFFF)
        mt1 = wasm_memorytype_new(wasm_limits_t)
        mt2 = wasm_memorytype_copy(mt1)
        self.assertEqual(mt1, mt2)

    def test_wasm_memorytype_copy_neg(self):
        self.assertIsNone(wasm_memorytype_copy(None))

    # wasm_egnine_new() should always return a wasm_engine_t

    def test_wasm_store_new_pos(self):
        engine = wasm_engine_new()
        self.assertIsNotNone(wasm_store_new(engine))

    def test_wasm_store_new_neg(self):
        self.assertIsNone(wasm_store_new(None))

    @classmethod
    def tearDownClass(cls):
        wasm_engine_delete(cls._wasm_engine)


if __name__ == "__main__":
    unittest.main()
