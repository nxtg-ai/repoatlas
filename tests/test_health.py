"""Tests for health scoring."""
from atlas.health import compute_health
from atlas.models import GitInfo, HealthScore, Project, TechStack


def _make_project(**kwargs) -> Project:
    defaults = {
        "name": "test",
        "path": "/tmp/test",
        "test_file_count": 10,
        "source_file_count": 50,
        "total_file_count": 100,
    }
    defaults.update(kwargs)
    return Project(**defaults)


class TestHealthScore:
    def test_compute_grade_a(self):
        hs = HealthScore(tests=1.0, git_hygiene=0.9, documentation=0.9, structure=0.9)
        hs.compute()
        assert hs.grade == "A"
        assert hs.percent >= 90

    def test_compute_grade_f(self):
        hs = HealthScore(tests=0.0, git_hygiene=0.0, documentation=0.0, structure=0.0)
        hs.compute()
        assert hs.grade == "F"
        assert hs.percent == 0

    def test_compute_grade_c(self):
        hs = HealthScore(tests=0.5, git_hygiene=0.7, documentation=0.6, structure=0.7)
        hs.compute()
        assert hs.grade in ("C", "B")
        assert 55 <= hs.percent <= 75

    def test_icon(self):
        hs = HealthScore()
        hs.overall = 0.9
        assert "green" in hs.icon
        hs.overall = 0.65
        assert "yellow" in hs.icon
        hs.overall = 0.45
        assert "red" in hs.icon


class TestComputeHealth:
    def test_project_with_tests_scores_higher(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        proj.test_file_count = 10
        proj.source_file_count = 50
        health = compute_health(proj)
        assert health.tests > 0

    def test_project_without_tests(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        proj.test_file_count = 0
        proj.source_file_count = 50
        health = compute_health(proj)
        assert health.tests == 0.0

    def test_docs_score_with_readme(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        health = compute_health(proj)
        assert health.documentation > 0  # README exists

    def test_structure_with_ci(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        health = compute_health(proj)
        assert health.structure > 0  # .github/workflows exists
