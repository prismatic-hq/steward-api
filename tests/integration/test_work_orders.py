import uuid

from fastapi.testclient import TestClient

NEW_WORK_ORDER = {"site": "crater-rim-trail", "title": "Repair railing", "priority": "high"}


def create_work_order(client: TestClient, **overrides: object) -> dict:
    response = client.post("/work-orders", json={**NEW_WORK_ORDER, **overrides})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_work_order_returns_open_work_order(client: TestClient) -> None:
    work_order = create_work_order(client)

    assert work_order["site"] == "crater-rim-trail"
    assert work_order["status"] == "open"
    assert work_order["assigned_crew"] is None
    assert uuid.UUID(work_order["id"])


def test_create_work_order_rejects_unknown_priority(client: TestClient) -> None:
    response = client.post("/work-orders", json={**NEW_WORK_ORDER, "priority": "urgent-ish"})

    assert response.status_code == 422


def test_list_work_orders_returns_created_work_orders(client: TestClient) -> None:
    first = create_work_order(client)
    second = create_work_order(client, site="visitor-center")

    response = client.get("/work-orders")

    assert response.status_code == 200
    assert [w["id"] for w in response.json()] == [first["id"], second["id"]]


def test_get_work_order_by_id(client: TestClient) -> None:
    work_order = create_work_order(client)

    response = client.get(f"/work-orders/{work_order['id']}")

    assert response.status_code == 200
    assert response.json() == work_order


def test_get_missing_work_order_returns_404(client: TestClient) -> None:
    response = client.get(f"/work-orders/{uuid.uuid4()}")

    assert response.status_code == 404


def test_update_work_order_changes_only_given_fields(client: TestClient) -> None:
    work_order = create_work_order(client)

    response = client.patch(
        f"/work-orders/{work_order['id']}",
        json={"status": "in_progress", "assigned_crew": "trail-crew-2"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["assigned_crew"] == "trail-crew-2"
    assert response.json()["title"] == work_order["title"]


def test_delete_work_order_removes_it(client: TestClient) -> None:
    work_order = create_work_order(client)

    assert client.delete(f"/work-orders/{work_order['id']}").status_code == 204
    assert client.get(f"/work-orders/{work_order['id']}").status_code == 404
