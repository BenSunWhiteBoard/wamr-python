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
    def test_wasm_valkind_pos(self):
        self.assertEqual(
            [WASM_I32, WASM_I64, WASM_F32, WASM_F64, WASM_ANYREF, WASM_FUNCREF],
            [0, 1, 2, 3, 4, 128, 129],
        )

    def test_wasm_valkind_neg(self):
        pass

    def test_wasm_valkind_is_num_pos(self):
        self.assertTrue(wasm_valkind_is_num(WASM_I64))
        self.assertTrue(wasm_valkind_is_num(WASM_F64))
        self.assertFalse(wasm_valkind_is_num(WASM_ANYREF))
        self.assertFalse(wasm_valkind_is_num(WASM_FUNCREF))

    def test_wasm_valkind_is_num_neg(self):
        self.assertFalse(wasm_valkind_is_num(None))
        self.assertFalse(wasm_valkind_is_num(7))

    def test_wasm_valkind_is_ref_pos(self):
        self.assertFalse(wasm_valkind_is_ref(WASM_I64))
        self.assertFalse(wasm_valkind_is_ref(WASM_F64))
        self.assertTrue(wasm_valkind_is_ref(WASM_ANYREF))
        self.assertTrue(wasm_valkind_is_ref(WASM_FUNCREF))

    def test_wasm_valkind_is_ref_neg(self):
        self.assertFalse(wasm_valkind_is_ref(None))
        self.assertFalse(wasm_valkind_is_ref(199))

    def test_wasm_valtype_new_pos(self):
        self.assertIsNone(wasm_valtype_new(WASM_I32))

    def test_wasm_valtype_new_neg(self):
        self.assertIsNone(wasm_valtype_new(None))
        self.assertIsNone(wasm_valtype_new(37))

    def test_wasm_valtype_kind_pos(self):
        self.assertEqual(wasm_valtype_kind(wasm_valtype_new(WASM_I64)), WASM_I64)

    def test_wasm_valtype_kind_neg(self):
        self.assertNotEqual(wasm_valtype_kind(wasm_valtype_new(5)), WASM_I32)

    def test_wasm_valtype_is_num_pos(self):
        self.assertTrue(wasm_valtype_is_num(wasm_valtype_new(WASM_F32)))
        self.assertTrue(wasm_valtype_is_num(wasm_valtype_new(WASM_F64)))

    def test_wasm_valtype_is_num_neg(self):
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(None)))
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(5)))
        self.assertFalse(wasm_valtype_is_num(wasm_valtype_new(130)))

    def test_wasm_valtype_is_ref_pos(self):
        self.assertTrue(wasm_valtype_is_ref(wasm_valtype_new(WASM_ANYREF)))
        self.assertTrue(wasm_valtype_is_ref(wasm_valtype_new(WASM_FUNCREF)))

    def test_wasm_valtype_is_ref_neg(self):
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(None)))
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(5)))
        self.assertFalse(wasm_valtype_is_ref(wasm_valtype_new(130)))

    def test_wasm_valtype_delete_pos(self):
        self.assertIsNone(wasm_valtype_delete(wasm_valtype_new(WASM_ANYREF)))

    def test_wasm_valtype_delete_neg(self):
        self.assertIsNone(wasm_valtype_delete(None))

    def test_wasm_valtype_copy_pos(self):
        vt1 = wasm_valtype_new(WASM_FUNCREF)
        vt2 = wasm_valtype_copy(vt1)
        self.assertEqual(wasm_valtype_kind(vt1), wasm_valtype_kind(vt2))

    def test_wasm_valtype_copy_neg(self):
        self.assertIsNone(wasm_valtype_copy(None))

    def test_wasm_valtype_vec_new_pos(self):
        data = wasm_valtype_t * 3
        data[0] = wasm_valtype_new(WASM_I32)
        data[1] = wasm_valtype_new(WASM_F64)
        data[2] = wasm_valtype_new(WASM_ANYREF)

        v = wasm_valtype_vec()
        wasm_valtype_vec_new(byref(v), 3, byref(data))

    def test_wasm_valtype_vec_new_neg(self):
        # should not raise any exception
        wasm_valtype_vec_new(None, 0, None)
        wasm_valtype_vec_new(None, 10, None)

        v = wasm_valtype_vec()
        wasm_valtype_vec_new(v, 0, None)
        wasm_valtype_vec_new(v, 0, None)

        data = wasm_valtype_t * 3
        data[0] = wasm_valtype_new(WASM_I32)
        data[1] = wasm_valtype_new(WASM_F64)
        data[2] = wasm_valtype_new(WASM_ANYREF)

        v = wasm_valtype_vec()
        wasm_valtype_vec_new(v, 0, data)
        wasm_valtype_vec_new(v, 10, data)

    def test_wasm_valtype_vec_new_uninitialized_pos(self):
        v = wasm_valtype_vec()
        wasm_valtype_vec_new_uninitialized(byref(v), 10)

        self.assertIsNotNone(v)
        self.assertIsNone(v.data)
        self.assertEqual(10, v.size)

    def test_wasm_valtype_vec_new_uninitialized_neg(self):
        wasm_valtype_vec_new_uninitialized(None)

    def test_wasm_valtype_vec_new_empty_pos(self):
        v = wasm_valtype_vec()
        wasm_valtype_vec_new_empty(byref(v))

        self.assertIsNotNone(v)
        self.assertIsNone(v.data)
        self.assertEqual(0, v.size)

    def test_wasm_valtype_vec_new_empty_neg(self):
        wasm_valtype_vec_new_empty(None)

    def test_wasm_valtype_vec_copy_pos(self):
        v1 = wasm_valtype_vec()
        wasm_valtype_vec_new_empty(byref(v1))

        v2 = wasm_valtype_vec()
        wasm_valtype_vec_copy(byref(v2))

        self.assertEqual(v1, v2)

        v1 = wasm_valtype_vec()
        wasm_valtype_vec_new_uninitialized(byref(v1), 3)

        v2 = wasm_valtype_vec()
        wasm_valtype_vec_copy(byref(v2))

        self.assertEqual(v1, v2)

        # more cases with wasm_valtype_vec_new

    def test_wasm_valtype_vec_copy_neg(self):
        wasm_valtype_vec_copy(None)

    def test_wasm_valtype_vec_delete_pos(self):
        v = wasm_valtype_vec()
        wasm_valtype_vec_new_uninitialized(byref(v), 10)
        wasm_valtype_vec_delete(v)

        self.assertIsNotNone(v)
        self.assertEqual(0, v.size)
        self.assertIsNone(v.data)

    def test_wasm_valtype_vec_delete_neg(self):
        wasm_valtype_vec_delete(None)

    def test_wasm_globaltype_new_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        self.assertIsNotNone(wasm_globaltype_new(vt, True))

    def test_wasm_globaltype_new_neg(self):
        vt = wasm_valtype_new(None)
        self.assertIsNone(wasm_globaltype_new(vt, True))

    def test_wasm_globaltype_delete_pos(self):
        vt = wasm_valtype_new(WASM_ANYREF)
        self.assertIsNone(wasm_globaltype_delete(wasm_globaltype_new(vt, True)))

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
        limits = limits(min=0, max=0xFFFFFFFF)
        self.assertIsNotNone(wasm_tabletype_new(vt, limits))

    def test_wasm_tabletype_new_neg(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        self.assertIsNone(wasm_tabletype_new(vt, None))

    def test_wasm_tabletype_delete_pos(self):
        vt = wasm_valtype_new(WASM_F32)
        self.assertIsNone(
            wasm_tabletype_delete(wasm_tabletype_new(vt, limits(0, 0xFFFFFFFF)))
        )

    def test_wasm_tabletype_delete_neg(self):
        self.assertIsNone(wasm_tabletype_delete(None))

    def test_wasm_tabletype_element_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        tt = wasm_tabletype_new(vt, limits(0, 0xFFFFFFFF))
        self.assertEqual(vt, wasm_tabletype_element(tt))

    def test_wasm_tabletype_element_neg(self):
        self.assertIsNone(wasm_tabletype_element(None))

    def test_wasm_tabletype_limits_pos(self):
        limits = limits(min=0, max=0x0000FFFF)
        tt = wasm_tabletype_new(wasm_valtype_new(WASM_FUNCREF), limits)
        self.assertEqual(limits, wasm_tabletype_limits(tt))

    def test_wasm_tabletype_limits_neg(self):
        self.assertIsNone(wasm_tabletype_limits(None))

    def test_wasm_tabletype_copy_pos(self):
        vt = wasm_valtype_new(WASM_FUNCREF)
        tt1 = wasm_tabletype_new(vt, limits(0, 0xFFFFFFFF))
        tt2 = wasm_tabletype_copy(tt1)
        self.assertEqual(tt1, tt2)

    def test_wasm_tabletype_copy_neg(self):
        self.assertIsNone(wasm_tabletype_copy(None))

    def test_wasm_engine_new_pos(self):
        self.assertIsNotNone(wasm_engine_new())

    # wasm_egnine_new() should always return a wasm_engine_t
    def test_wasm_engine_new_neg(self):
        pass

    def test_wasm_store_new_pos(self):
        engine = wasm_engine_new()
        self.assertIsNotNone(wasm_store_new(engine))

    def test_wasm_store_new_neg(self):
        self.assertIsNone(wasm_store_new(None))


if __name__ == "__main__":
    unittest.main()
