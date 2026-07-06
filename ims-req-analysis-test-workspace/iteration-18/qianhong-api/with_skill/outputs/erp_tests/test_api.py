"""
IMS API Test Suite - test_api.py
Generated from test_cases.md YAML block for the 千虹 interface document.

Usage:
    pytest erp_tests/test_api.py -m p0 -v         # Smoke tests
    pytest erp_tests/test_api.py -m "p0 or p1" -v # Functional tests
    pytest erp_tests/test_api.py -m "p0 or p1 or p2" -v # Full tests
    pytest erp_tests/test_api.py -m "p0 or p1 or p2 or p3" -v # Complete
"""
import uuid
import pytest
import httpx


# ============================================================
# P0 - Smoke Tests (must pass for every build)
# ============================================================


class TestAuth:
    """4.0 获取访问令牌"""

    @pytest.mark.p0
    def test_auth_success(self, unauth_client):
        """A-001: 正常获取Token"""
        resp = unauth_client.post(
            "/public/auth/authorization",
            json={"username": "admin", "password": "IMS@2026"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert isinstance(data["data"], str) and len(data["data"]) > 0

    @pytest.mark.p0
    def test_unauthorized_access_401(self, unauth_client):
        """A-008: 无Token访问业务API返回401"""
        resp = unauth_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "PALLET-001"},
        )
        assert resp.status_code == 401


class TestCarrierInfo:
    """4.1 载具信息查询"""

    @pytest.mark.p0
    def test_query_carrier_full_depth(self, api_client):
        """A-012: 查询存在载具(depth=3)"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "PALLET-001", "depth": 3},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert "data" in data


class TestCarrierTask:
    """4.3 载具任务执行下发"""

    @pytest.mark.p0
    def test_task_put_on(self, api_client):
        """A-019: 上架任务下发"""
        resp = api_client.post(
            "/wms/v3/carrier/task/execute",
            json={
                "taskType": "PUT_ON",
                "carrierNo": "PALLET-001",
                "sourceLocationCode": "WCS-A-01-01",
                "targetSpaceCode": "ZONE-STORAGE",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["taskType"] == "PUT_ON"


class TestWarehouseSpace:
    """4.2 库区查询"""

    @pytest.mark.p0
    def test_query_space_fuzzy(self, api_client):
        """A-035: 库区模糊查询"""
        resp = api_client.post(
            "/wms/v3/warehouse/space",
            json={"warehouseSpaceCode": "ZONE"},
        )
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

    @pytest.mark.p0
    def test_query_space_list_by_type(self, api_client):
        """A-041: 按面料仓类型查询库区"""
        resp = api_client.post(
            "/wms/v3/warehouse/space/list",
            json={"warehouseTypeCode": "A"},
        )
        assert resp.status_code == 200
        assert resp.json()["code"] == 0


class TestMaterialSync:
    """4.4 物料物品清单同步"""

    @pytest.mark.p0
    def test_sync_fabric_no_init(self, api_client):
        """A-046: 面料清单同步(不初始化库存)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "fabric",
                "initInventory": False,
                "itemList": [
                    {
                        "itemNo": f"FN-TEST-{req_id}",
                        "materialExtendCode": "MAT-TEST-001",
                        "materialName": "测试面料",
                        "batchNo": f"BATCH-{req_id}",
                        "itemUnit": "M",
                        "itemAmount": 1000.0,
                    }
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert data["data"]["syncState"] == "ACCEPTED"


class TestCarrierBind:
    """4.5 货载绑定/解绑"""

    @pytest.mark.p0
    def test_bind_incr(self, api_client):
        """A-063: 增量绑定(BIND+INCR)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "BIND",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0

    @pytest.mark.p0
    def test_bind_full(self, api_client):
        """A-064: 全量绑定(BIND+FULL)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "BIND",
                "linkMode": "FULL",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == 200
        assert resp.json()["code"] == 0


class TestStockFlow:
    """4.6 物料出入库"""

    @pytest.mark.p0
    def test_stock_inbound(self, api_client):
        """A-076: 物料入库(flowType=1)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/stock/flow",
            json={
                "requestId": req_id,
                "flowType": "1",
                "itemList": [
                    {
                        "itemNo": f"FN-INB-{req_id}",
                        "itemUnit": "M",
                        "itemAmount": 5000.0,
                    }
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0


class TestInventoryQuery:
    """4.7 物料库存查询"""

    @pytest.mark.p0
    def test_inventory_query_fabric(self, api_client):
        """A-091: 库存查询(面料仓)"""
        resp = api_client.post(
            "/wms/v3/material/item/inventory",
            json={"warehouseTypeCode": "A", "pageNo": 1, "pageSize": 20},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        assert "data" in data


class TestProductionOrder:
    """生产订单同步"""

    @pytest.mark.p0
    def test_production_order_minimal(self, api_client):
        """A-097: 生产订单最小必填"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/production/v3/save",
            json={
                "productionOrderNo": f"PO-TEST-{req_id}",
                "styleCode": "STYLE-001",
                "styleName": "测试款号",
            },
        )
        assert resp.status_code == 200


class TestSewingTask:
    """缝制任务单同步"""

    @pytest.mark.p0
    def test_sewing_task_minimal(self, api_client):
        """A-104: 缝制任务最小必填"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/sewing/v3/save",
            json={
                "sewingCode": f"SG-TEST-{req_id}",
                "productionOrderNo": "PO-TEST-001",
                "styleCode": "STYLE-001",
            },
        )
        assert resp.status_code == 200


# ============================================================
# P1 - Functional Tests
# ============================================================


class TestAuthP1:
    """认证功能测试"""

    @pytest.mark.p1
    @pytest.mark.parametrize(
        "username,password,expect_status",
        [
            ("admin", "WrongPassword123", 401),
            ("nonexistent_user", "any", 401),
        ],
    )
    def test_auth_failure(self, unauth_client, username, password, expect_status):
        """A-002, A-003: 错误密码/不存在用户"""
        resp = unauth_client.post(
            "/public/auth/authorization",
            json={"username": username, "password": password},
        )
        assert resp.status_code == expect_status

    @pytest.mark.p1
    def test_expired_token_401(self, unauth_client):
        """A-009: 过期Token返回401"""
        resp = unauth_client.post(
            "/wms/v3/carrier/info",
            headers={"Authorization": "Bearer expired-token-for-test"},
            json={"carrierNo": "PALLET-001"},
        )
        assert resp.status_code == 401


class TestCarrierInfoP1:
    """载具查询功能测试"""

    @pytest.mark.p1
    def test_query_empty_carrier_depth1(self, api_client):
        """A-013: 查询空载具(depth=1)"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "PALLET-002", "depth": 1},
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_query_bound_carrier_depth3(self, api_client):
        """A-014: 查询已绑定载具(depth=3)含物料列表"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "PALLET-001", "depth": 3},
        )
        assert resp.status_code == 200
        data = resp.json()
        if data["code"] == 0 and data.get("data", {}).get("carrierBindStatus") == 1:
            assert "itemList" in data["data"]


class TestCarrierTaskP1:
    """载具任务功能测试"""

    @pytest.mark.p1
    @pytest.mark.parametrize(
        "task_type",
        ["PUT_DOWN", "MOVE_OUTSIDE"],
    )
    def test_task_types(self, api_client, task_type):
        """A-020, A-021: 下架和库外移动任务"""
        resp = api_client.post(
            "/wms/v3/carrier/task/execute",
            json={
                "taskType": task_type,
                "carrierNo": "PALLET-001",
                "sourceLocationCode": "WCS-A-01-01",
                "targetSpaceCode": "ZONE-STORAGE",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

    @pytest.mark.p1
    def test_task_with_biz_id(self, api_client):
        """A-022: 带bizTaskId的任务下发"""
        resp = api_client.post(
            "/wms/v3/carrier/task/execute",
            json={
                "taskType": "PUT_ON",
                "carrierNo": "PALLET-001",
                "sourceLocationCode": "WCS-A-01-01",
                "targetSpaceCode": "ZONE-STORAGE",
                "bizTaskId": "BIZ-001",
            },
        )
        assert resp.status_code == 200


class TestWarehouseSpaceP1:
    """库区查询功能测试"""

    @pytest.mark.p1
    def test_query_space_with_attributes(self, api_client):
        """A-036: 库区属性精准匹配"""
        resp = api_client.post(
            "/wms/v3/warehouse/space",
            json={
                "spaceAttributes": [
                    {"attrKey": "RECEIVING", "attrVal": "收货区"}
                ]
            },
        )
        assert resp.status_code == 200
        assert resp.json()["code"] == 0

    @pytest.mark.p1
    def test_query_all_spaces(self, api_client):
        """A-037: 空参数查询所有库区"""
        resp = api_client.post("/wms/v3/warehouse/space", json={})
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_query_space_list_cutting(self, api_client):
        """A-042: 按裁片仓类型查询"""
        resp = api_client.post(
            "/wms/v3/warehouse/space/list",
            json={"warehouseTypeCode": "C"},
        )
        assert resp.status_code == 200


class TestMaterialSyncP1:
    """物料同步功能测试"""

    @pytest.mark.p1
    def test_sync_with_init_inventory(self, api_client):
        """A-047: 面料同步+初始化库存"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "fabric",
                "initInventory": True,
                "itemList": [
                    {
                        "itemNo": f"FN-INIT-{req_id}",
                        "materialExtendCode": "MAT-INIT-001",
                        "materialName": "初始化库存面料",
                        "batchNo": f"BATCH-{req_id}",
                        "itemUnit": "M",
                        "itemAmount": 5000.0,
                    }
                ],
            },
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_sync_trim(self, api_client):
        """A-048: 辅料清单同步"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "trim",
                "initInventory": False,
                "itemList": [
                    {
                        "itemNo": f"TR-TEST-{req_id}",
                        "materialExtendCode": "TRIM-TEST-001",
                        "materialName": "测试辅料",
                        "batchNo": f"BATCH-{req_id}",
                        "itemUnit": "PCS",
                    }
                ],
            },
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_sync_with_extended_attrs(self, api_client):
        """A-049: 含完整扩展属性同步"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "fabric",
                "initInventory": False,
                "itemList": [
                    {
                        "itemNo": f"FN-EXT-{req_id}",
                        "materialExtendCode": "MAT-EXT-001",
                        "materialName": "扩展属性面料",
                        "batchNo": f"BATCH-{req_id}",
                        "itemUnit": "M",
                        "itemAmount": 3000.0,
                        "vatCode": "VAT-001",
                        "lotCode": "LOT-A",
                        "fabricNo": "FAB-001",
                        "breadthValue": 150.0,
                        "breadthUnit": "M",
                        "weightValue": 250.0,
                        "weightUnit": "KG",
                        "ingredient": "100%涤纶",
                        "needInspection": "0",
                        "purveyor": "测试供应商",
                        "incomingDate": "2026-07-01",
                    }
                ],
            },
        )
        assert resp.status_code == 200


class TestCarrierBindP1:
    """货载绑定功能测试"""

    @pytest.mark.p1
    def test_unbind_incr(self, api_client):
        """A-065: 增量解绑(UNBIND+INCR)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "UNBIND",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_unbind_full(self, api_client):
        """A-066: 全量解绑(UNBIND+FULL)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "UNBIND",
                "linkMode": "FULL",
                "itemType": "fabric",
            },
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_bind_non_existent_item(self, api_client):
        """A-068: 绑定不存在的物料"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "BIND",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [{"itemNo": "NONEXIST-ITEM-999"}],
            },
        )
        assert resp.status_code in [200, 400]
        if resp.status_code == 200:
            assert resp.json()["code"] != 0


class TestStockFlowP1:
    """出入库功能测试"""

    @pytest.mark.p1
    def test_stock_outbound(self, api_client):
        """A-077: 物料出库(flowType=2)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/stock/flow",
            json={
                "requestId": req_id,
                "flowType": "2",
                "itemList": [
                    {
                        "itemNo": "FN-INVENTORY-001",
                        "itemUnit": "M",
                        "itemAmount": 500.0,
                    }
                ],
            },
        )
        assert resp.status_code == 200


class TestInventoryQueryP1:
    """库存查询功能测试"""

    @pytest.mark.p1
    def test_inventory_query_by_item(self, api_client):
        """A-092: 库存查询(按物料itemNo)"""
        resp = api_client.post(
            "/wms/v3/material/item/inventory",
            json={
                "warehouseTypeCode": "A",
                "itemNo": "FN20260604001",
            },
        )
        assert resp.status_code == 200


class TestProductionOrderP1:
    """生产订单功能测试"""

    @pytest.mark.p1
    def test_production_order_full(self, api_client):
        """A-098: 生产订单含色码和工序"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/production/v3/save",
            json={
                "productionOrderNo": f"PO-FULL-{req_id}",
                "styleCode": "STYLE-001",
                "styleName": "测试款号全字段",
                "brandName": "测试品牌",
                "detailList": [
                    {
                        "garmentColorCode": "RED001",
                        "garmentColorName": "红色",
                        "garmentSizeCode": "SIZE_M",
                        "garmentSizeName": "M",
                        "number": 100,
                    }
                ],
                "procedureList": [
                    {
                        "procedureNumber": "01",
                        "procedureName": "裁剪",
                        "procedureCode": "CUT-01",
                        "sam": "5.0",
                        "price": 10,
                    }
                ],
            },
        )
        assert resp.status_code == 200

    @pytest.mark.p1
    def test_production_order_empty_detail_list(self, api_client):
        """A-099: 生产订单空detailList"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/production/v3/save",
            json={
                "productionOrderNo": f"PO-EMPTY-{req_id}",
                "styleCode": "STYLE-001",
                "styleName": "空色码款号",
                "detailList": [],
            },
        )
        assert resp.status_code == 200


class TestSewingTaskP1:
    """缝制任务功能测试"""

    @pytest.mark.p1
    def test_sewing_task_with_details(self, api_client):
        """A-105: 缝制任务含色码明细"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/sewing/v3/save",
            json={
                "sewingCode": f"SG-FULL-{req_id}",
                "productionOrderNo": "PO-TEST-001",
                "styleCode": "STYLE-001",
                "detailList": [
                    {
                        "garmentColorCode": "RED001",
                        "garmentColorName": "红色",
                        "garmentSizeCode": "SIZE_M",
                        "garmentSizeName": "M",
                        "number": 100,
                        "orderNo": 1,
                    }
                ],
            },
        )
        assert resp.status_code == 200


# ============================================================
# P2 - Boundary Tests
# ============================================================


class TestAuthBoundary:
    """认证边界测试"""

    @pytest.mark.p2
    @pytest.mark.parametrize(
        "payload,expect_status",
        [
            ({"username": "", "password": ""}, 400),
            ({"password": "IMS@2026"}, 400),
            ({"username": "admin"}, 400),
        ],
    )
    def test_auth_boundary(self, unauth_client, payload, expect_status):
        """A-004, A-005, A-006: 空凭证/缺失必填字段"""
        resp = unauth_client.post("/public/auth/authorization", json=payload)
        assert resp.status_code == expect_status

    @pytest.mark.p2
    def test_token_format(self, unauth_client):
        """A-007: Token格式验证"""
        resp = unauth_client.post(
            "/public/auth/authorization",
            json={"username": "admin", "password": "IMS@2026"},
        )
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("data", "")
            assert isinstance(token, str)
            assert len(token) > 0

    @pytest.mark.p2
    def test_tampered_token_401(self, unauth_client):
        """A-010: 篡改Token返回401"""
        resp = unauth_client.post(
            "/wms/v3/carrier/info",
            headers={"Authorization": "Bearer fake-invalid-token-12345"},
            json={"carrierNo": "PALLET-001"},
        )
        assert resp.status_code == 401


class TestCarrierInfoBoundary:
    """载具查询边界测试"""

    @pytest.mark.p2
    def test_query_nonexist_carrier(self, api_client):
        """A-015: 查询不存在的载具"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "NONEXIST-CARRIER-999"},
        )
        assert resp.status_code == 200

    @pytest.mark.p2
    def test_query_empty_carrier_no(self, api_client):
        """A-016: 空carrierNo查询"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": ""},
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    @pytest.mark.parametrize("depth", [0, 99])
    def test_query_boundary_depth(self, api_client, depth):
        """A-017, A-018: depth=0和超范围查询"""
        resp = api_client.post(
            "/wms/v3/carrier/info",
            json={"carrierNo": "PALLET-001", "depth": depth},
        )
        assert resp.status_code == 200


class TestCarrierTaskBoundary:
    """载具任务边界测试"""

    @pytest.mark.p2
    def test_invalid_task_type(self, api_client):
        """A-023: 非法taskType"""
        resp = api_client.post(
            "/wms/v3/carrier/task/execute",
            json={
                "taskType": "INVALID_TYPE",
                "carrierNo": "PALLET-001",
                "sourceLocationCode": "WCS-A-01-01",
                "targetSpaceCode": "ZONE-STORAGE",
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    @pytest.mark.parametrize(
        "field_to_empty",
        ["carrierNo", "sourceLocationCode", "targetSpaceCode"],
    )
    def test_task_empty_required_fields(self, api_client, field_to_empty):
        """A-024, A-025, A-026: 空必填字段"""
        payload = {
            "taskType": "PUT_ON",
            "carrierNo": "PALLET-001",
            "sourceLocationCode": "WCS-A-01-01",
            "targetSpaceCode": "ZONE-STORAGE",
        }
        payload[field_to_empty] = ""
        resp = api_client.post("/wms/v3/carrier/task/execute", json=payload)
        assert resp.status_code == 400


class TestWarehouseSpaceBoundary:
    """库区查询边界测试"""

    @pytest.mark.p2
    def test_query_nonexist_space_code(self, api_client):
        """A-038: 不存在的库区编码"""
        resp = api_client.post(
            "/wms/v3/warehouse/space",
            json={"warehouseSpaceCode": "NONEXIST_SPACE_999"},
        )
        assert resp.status_code == 200

    @pytest.mark.p2
    def test_query_empty_attributes(self, api_client):
        """A-039: 空spaceAttributes"""
        resp = api_client.post(
            "/wms/v3/warehouse/space",
            json={"spaceAttributes": []},
        )
        assert resp.status_code == 200

    @pytest.mark.p2
    def test_query_space_list_invalid_type(self, api_client):
        """A-044: 非法仓库类型"""
        resp = api_client.post(
            "/wms/v3/warehouse/space/list",
            json={"warehouseTypeCode": "X"},
        )
        assert resp.status_code in [200, 400]

    @pytest.mark.p2
    def test_query_space_list_missing_type(self, api_client):
        """A-045: 缺失warehouseTypeCode"""
        resp = api_client.post("/wms/v3/warehouse/space/list", json={})
        assert resp.status_code == 400


class TestMaterialSyncBoundary:
    """物料同步边界测试"""

    @pytest.mark.p2
    def test_sync_missing_request_id(self, api_client):
        """A-050: 缺失requestId"""
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "itemType": "fabric",
                "itemList": [
                    {
                        "itemNo": "FN-TEST-001",
                        "materialExtendCode": "MAT-001",
                        "materialName": "测试",
                        "batchNo": "BATCH-001",
                        "itemUnit": "M",
                    }
                ],
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_sync_missing_item_type(self, api_client):
        """A-051: 缺失itemType"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemList": [
                    {
                        "itemNo": f"FN-TEST-{req_id}",
                        "materialExtendCode": "MAT-001",
                        "materialName": "测试",
                        "batchNo": "BATCH-001",
                        "itemUnit": "M",
                    }
                ],
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_sync_empty_item_list(self, api_client):
        """A-052: 空itemList"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "fabric",
                "itemList": [],
            },
        )
        assert resp.status_code in [200, 400]

    @pytest.mark.p2
    def test_sync_invalid_item_type(self, api_client):
        """A-054: 非法itemType"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/sync",
            json={
                "requestId": req_id,
                "itemType": "invalid_type",
                "itemList": [
                    {
                        "itemNo": f"FN-TEST-{req_id}",
                        "materialExtendCode": "MAT-001",
                        "materialName": "测试",
                        "batchNo": "BATCH-001",
                        "itemUnit": "M",
                    }
                ],
            },
        )
        assert resp.status_code == 400


class TestCarrierBindBoundary:
    """货载绑定边界测试"""

    @pytest.mark.p2
    def test_bind_missing_carrier_no(self, api_client):
        """A-069: 缺失carrierNo"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "bindType": "BIND",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_bind_missing_bind_type(self, api_client):
        """A-070: 缺失bindType"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    @pytest.mark.parametrize(
        "bind_type,link_mode,expect_status",
        [
            ("INVALID", "INCR", 400),
            ("BIND", "INVALID", 400),
        ],
    )
    def test_bind_invalid_enums(self, api_client, bind_type, link_mode, expect_status):
        """A-071, A-072: 非法bindType/linkMode"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": bind_type,
                "linkMode": link_mode,
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code == expect_status

    @pytest.mark.p2
    def test_unbind_full_with_item_list(self, api_client):
        """A-073: UNBIND+FULL+传itemList(参数矛盾)"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "UNBIND",
                "linkMode": "FULL",
                "itemType": "fabric",
                "itemList": [{"itemNo": f"FN-TEST-{req_id}"}],
            },
        )
        assert resp.status_code in [200, 400]

    @pytest.mark.p2
    def test_bind_incr_empty_item_list(self, api_client):
        """A-074: BIND+INCR+空itemList"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/carrier/item/link",
            json={
                "requestId": req_id,
                "carrierNo": "PALLET-001",
                "bindType": "BIND",
                "linkMode": "INCR",
                "itemType": "fabric",
                "itemList": [],
            },
        )
        assert resp.status_code in [200, 400]


class TestStockFlowBoundary:
    """出入库边界测试"""

    @pytest.mark.p2
    def test_invalid_flow_type(self, api_client):
        """A-079: 非法flowType"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/stock/flow",
            json={
                "requestId": req_id,
                "flowType": "3",
                "itemList": [
                    {"itemNo": "FN-TEST-001"}
                ],
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_missing_flow_type(self, api_client):
        """A-080: 缺失flowType"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/wms/v3/material/item/stock/flow",
            json={
                "requestId": req_id,
                "itemList": [
                    {"itemNo": "FN-TEST-001"}
                ],
            },
        )
        assert resp.status_code == 400


class TestInventoryBoundary:
    """库存查询边界测试"""

    @pytest.mark.p2
    @pytest.mark.parametrize(
        "page_no,page_size",
        [
            (0, 20),
            (-1, 20),
            (1, 0),
            (1, 101),
        ],
    )
    def test_pagination_boundary(self, api_client, page_no, page_size):
        """A-093, A-094, A-095, A-096: 分页边界值"""
        resp = api_client.post(
            "/wms/v3/material/item/inventory",
            json={
                "warehouseTypeCode": "A",
                "pageNo": page_no,
                "pageSize": page_size,
            },
        )
        assert resp.status_code == 200


class TestProductionOrderBoundary:
    """生产订单边界测试"""

    @pytest.mark.p2
    def test_missing_production_order_no(self, api_client):
        """A-100: 缺失productionOrderNo"""
        resp = api_client.post(
            "/production/v3/save",
            json={
                "styleCode": "STYLE-001",
                "styleName": "测试款号",
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_missing_style_code(self, api_client):
        """A-101: 缺失styleCode"""
        resp = api_client.post(
            "/production/v3/save",
            json={
                "productionOrderNo": "PO-TEST-002",
                "styleName": "测试款号",
            },
        )
        assert resp.status_code == 400


class TestSewingTaskBoundary:
    """缝制任务边界测试"""

    @pytest.mark.p2
    def test_missing_sewing_code(self, api_client):
        """A-107: 缺失sewingCode"""
        resp = api_client.post(
            "/sewing/v3/save",
            json={
                "productionOrderNo": "PO-TEST-001",
                "styleCode": "STYLE-001",
            },
        )
        assert resp.status_code == 400

    @pytest.mark.p2
    def test_detail_missing_order_no(self, api_client):
        """A-108: detailList缺失orderNo"""
        req_id = str(uuid.uuid4())[:8]
        resp = api_client.post(
            "/sewing/v3/save",
            json={
                "sewingCode": f"SG-TEST-{req_id}",
                "productionOrderNo": "PO-TEST-001",
                "styleCode": "STYLE-001",
                "detailList": [
                    {
                        "garmentColorCode": "RED001",
                        "garmentColorName": "红色",
                        "garmentSizeCode": "SIZE_M",
                        "garmentSizeName": "M",
                        "number": 100,
                    }
                ],
            },
        )
        assert resp.status_code == 400


# ============================================================
# P3 - Integration Tests
# ============================================================


class TestIdempotency:
    """幂等性测试"""

    @pytest.mark.p3
    def test_duplicate_request_id(self, api_client):
        """A-055: 相同requestId重复提交"""
        req_id = str(uuid.uuid4())[:8]
        payload = {
            "requestId": req_id,
            "itemType": "fabric",
            "initInventory": False,
            "itemList": [
                {
                    "itemNo": f"FN-DUP-{req_id}",
                    "materialExtendCode": "MAT-DUP-001",
                    "materialName": "幂等测试",
                    "batchNo": f"BATCH-{req_id}",
                    "itemUnit": "M",
                    "itemAmount": 1000.0,
                }
            ],
        }
        resp1 = api_client.post("/wms/v3/material/item/sync", json=payload)
        resp2 = api_client.post("/wms/v3/material/item/sync", json=payload)
        assert resp1.status_code == 200
        # Second call should succeed (idempotent) or return conflict
        assert resp2.status_code in [200, 409]

    @pytest.mark.p3
    def test_duplicate_production_order_no(self, api_client):
        """A-103: 重复productionOrderNo"""
        req_id = str(uuid.uuid4())[:8]
        payload = {
            "productionOrderNo": f"PO-DUP-{req_id}",
            "styleCode": "STYLE-001",
            "styleName": "幂等测试订单",
        }
        resp1 = api_client.post("/production/v3/save", json=payload)
        resp2 = api_client.post("/production/v3/save", json=payload)
        assert resp1.status_code == 200
        assert resp2.status_code in [200, 409]

    @pytest.mark.p3
    def test_duplicate_sewing_code(self, api_client):
        """A-109: 重复sewingCode"""
        req_id = str(uuid.uuid4())[:8]
        payload = {
            "sewingCode": f"SG-DUP-{req_id}",
            "productionOrderNo": "PO-TEST-001",
            "styleCode": "STYLE-001",
        }
        resp1 = api_client.post("/sewing/v3/save", json=payload)
        resp2 = api_client.post("/sewing/v3/save", json=payload)
        assert resp1.status_code == 200
        assert resp2.status_code in [200, 409]
