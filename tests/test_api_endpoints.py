import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models

# Create an isolated in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Creates fresh tables and seeds sample data before each test, then drops tables."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    mosque_1 = models.Mosque(
        id=1,
        google_places_id="gpid_brooklyn_1",
        name="Al-Farooq Mosque",
        address="554 Atlantic Ave, Brooklyn, NY 11217",
        latitude=40.6845,
        longitude=-73.9788,
        rating=4.8,
        reviews=[],
    )
    mosque_2 = models.Mosque(
        id=2,
        google_places_id="gpid_queens_2",
        name="Queens Islamic Center",
        address="123 Queens Blvd, Queens, NY 11375",
        latitude=40.7214,
        longitude=-73.8448,
        rating=4.6,
        reviews=[],
    )
    review_1 = models.Review(
        id=1,
        google_places_id="gpid_brooklyn_1",
        author="Amina K.",
        rating=5.0,
        review_text="Clean wudu area and great sisters entrance upstairs.",
        review_date=datetime(2026, 10, 15, 12, 0, 0),
    )

    db.add_all([mosque_1, mosque_2, review_1])
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)


def test_root_endpoint_returns_welcome_message():
    """Core workflow: verifies root health-check endpoint returns 200 OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Masjid Navigator API!"}


def test_get_all_mosques_returns_seeded_list():
    """Core workflow: verifies GET /mosques/ returns all mosques in valid schema format."""
    response = client.get("/mosques/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Al-Farooq Mosque"


def test_search_mosques_by_name_query_param():
    """Core workflow: verifies ?search= query parameter filters mosques accurately."""
    response = client.get("/mosques/?search=Queens")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["google_places_id"] == "gpid_queens_2"


def test_get_mosques_pagination_limit_and_skip():
    """Boundary condition: verifies limit and skip pagination parameters."""
    response = client.get("/mosques/?limit=1&skip=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["google_places_id"] == "gpid_queens_2"


def test_get_single_mosque_by_gpid():
    """Core workflow: verifies retrieving a single mosque by google_places_id."""
    response = client.get("/mosques/gpid_brooklyn_1")
    assert response.status_code == 200
    assert response.json()["name"] == "Al-Farooq Mosque"


def test_get_nonexistent_mosque_returns_404():
    """Error scenario: requesting an unknown google_places_id returns 404 Not Found."""
    response = client.get("/mosques/nonexistent_id_999")
    assert response.status_code == 404
    assert "was not found" in response.json()["detail"]


def test_get_reviews_for_mosque():
    """Core workflow: verifies GET /review/{google_places_id} returns linked reviews."""
    response = client.get("/review/gpid_brooklyn_1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["author"] == "Amina K."


def test_get_reviews_for_mosque_without_reviews_returns_404():
    """Error scenario: requesting reviews for a mosque with none returns 404 Not Found."""
    response = client.get("/review/gpid_queens_2")
    assert response.status_code == 404