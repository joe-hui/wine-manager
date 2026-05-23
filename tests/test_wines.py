import pytest


WINERY_PAYLOAD = {"name": "Château Margaux", "country": "France", "region": "Bordeaux"}
WINE_PAYLOAD = {
    "name": "Château Margaux 2015",
    "winery_id": 1,
    "type": "red",
    "vintage": 2015,
    "price": 499.99,
    "abv": 13.5,
}
NOTE_PAYLOAD = {"wine_id": 1, "rating": 95, "notes": "Exceptional vintage", "reviewer": "Robert Parker"}


class TestWineries:
    def test_create_winery(self, client):
        resp = client.post("/wineries", json=WINERY_PAYLOAD)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Château Margaux"
        assert data["country"] == "France"
        assert "id" in data

    def test_create_duplicate_winery(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        resp = client.post("/wineries", json=WINERY_PAYLOAD)
        assert resp.status_code == 409

    def test_list_wineries(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        resp = client.get("/wineries")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Château Margaux"

    def test_get_winery(self, client):
        create_resp = client.post("/wineries", json=WINERY_PAYLOAD)
        winery_id = create_resp.json()["id"]
        resp = client.get(f"/wineries/{winery_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Château Margaux"

    def test_get_winery_not_found(self, client):
        resp = client.get("/wineries/999")
        assert resp.status_code == 404

    def test_delete_winery(self, client):
        create_resp = client.post("/wineries", json=WINERY_PAYLOAD)
        winery_id = create_resp.json()["id"]
        resp = client.delete(f"/wineries/{winery_id}")
        assert resp.status_code == 204
        # Verify it's gone
        get_resp = client.get(f"/wineries/{winery_id}")
        assert get_resp.status_code == 404


class TestWines:
    def test_create_wine(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        resp = client.post("/wines", json=WINE_PAYLOAD)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Château Margaux 2015"
        assert data["vintage"] == 2015

    def test_create_wine_missing_winery(self, client):
        payload = {**WINE_PAYLOAD, "winery_id": 999}
        resp = client.post("/wines", json=payload)
        assert resp.status_code == 404

    def test_list_wines(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        client.post("/wines", json=WINE_PAYLOAD)
        resp = client.get("/wines")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_list_wines_filter_by_type(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        client.post("/wines", json=WINE_PAYLOAD)
        resp = client.get("/wines?type=red")
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        resp = client.get("/wines?type=white")
        assert len(resp.json()) == 0

    def test_get_wine(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        create_resp = client.post("/wines", json=WINE_PAYLOAD)
        wine_id = create_resp.json()["id"]
        resp = client.get(f"/wines/{wine_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Château Margaux 2015"

    def test_delete_wine(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        create_resp = client.post("/wines", json=WINE_PAYLOAD)
        wine_id = create_resp.json()["id"]
        resp = client.delete(f"/wines/{wine_id}")
        assert resp.status_code == 204


class TestTastingNotes:
    def test_create_note(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        wine_resp = client.post("/wines", json=WINE_PAYLOAD)
        note_payload = {**NOTE_PAYLOAD, "wine_id": wine_resp.json()["id"]}
        resp = client.post("/notes", json=note_payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["rating"] == 95
        assert data["reviewer"] == "Robert Parker"

    def test_create_note_missing_wine(self, client):
        resp = client.post("/notes", json=NOTE_PAYLOAD)
        assert resp.status_code == 404

    def test_list_notes(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        wine_resp = client.post("/wines", json=WINE_PAYLOAD)
        note_payload = {**NOTE_PAYLOAD, "wine_id": wine_resp.json()["id"]}
        client.post("/notes", json=note_payload)
        resp = client.get("/notes")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_list_notes_filter_by_wine(self, client):
        client.post("/wineries", json=WINERY_PAYLOAD)
        wine_resp = client.post("/wines", json=WINE_PAYLOAD)
        note_payload = {**NOTE_PAYLOAD, "wine_id": wine_resp.json()["id"]}
        client.post("/notes", json=note_payload)
        resp = client.get(f"/notes?wine_id={wine_resp.json()['id']}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1
