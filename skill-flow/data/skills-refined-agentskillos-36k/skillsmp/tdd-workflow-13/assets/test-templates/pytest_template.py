# ruff: noqa: F841
"""
pytest 테스트 템플릿

Usage:
    cp pytest_template.py tests/test_<module>.py

TDD 규칙:
    1. Red Phase: 이 템플릿으로 실패하는 테스트 먼저 작성
    2. Green Phase: 테스트 통과하는 최소 구현
    3. Refactor Phase: 코드 정리 (테스트 유지)
"""

import pytest


class TestClassName:
    """테스트 클래스 설명

    테스트 대상: <module>.<ClassName>
    """

    @pytest.fixture
    def setup_data(self):
        """테스트 데이터 설정"""
        return {"key": "value"}

    @pytest.fixture
    def mock_dependency(self, mocker):
        """의존성 모킹 (pytest-mock 필요)"""
        return mocker.patch("module.dependency")

    # === 정상 케이스 ===

    def test_should_return_expected_when_valid_input(self, setup_data):
        """Given-When-Then 패턴: 유효한 입력 시 예상 결과 반환"""
        # Given
        input_data = setup_data

        # When
        # result = function_under_test(input_data)

        # Then
        # assert result == expected_value
        pytest.skip("TODO: 구현 필요")

    def test_should_handle_empty_input(self):
        """빈 입력 처리"""
        # Given
        input_data = {}

        # When
        # result = function_under_test(input_data)

        # Then
        # assert result is not None
        pytest.skip("TODO: 구현 필요")

    # === 예외 케이스 ===

    def test_should_raise_error_when_invalid_input(self):
        """잘못된 입력 시 예외 발생"""
        # Given
        invalid_input = None

        # When / Then
        with pytest.raises(ValueError):
            # function_under_test(invalid_input)
            raise ValueError("TODO: 구현 필요")

    def test_should_raise_type_error_when_wrong_type(self):
        """타입 오류 시 TypeError 발생"""
        # Given
        wrong_type_input = 12345  # 문자열이어야 하는데 정수

        # When / Then
        with pytest.raises(TypeError):
            # function_under_test(wrong_type_input)
            raise TypeError("TODO: 구현 필요")

    # === 경계 케이스 ===

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            ("", ""),  # 빈 문자열
            ("a", "a"),  # 단일 문자
            ("abc", "abc"),  # 일반 문자열
            ("a" * 1000, None),  # 긴 문자열
        ],
    )
    def test_boundary_conditions(self, input_value, expected):
        """경계 조건 파라미터화 테스트"""
        # When
        # result = function_under_test(input_value)

        # Then
        # assert result == expected
        pytest.skip("TODO: 구현 필요")


# === 단독 함수 테스트 ===


def test_standalone_function():
    """단독 함수 테스트"""
    # Given
    input_data = "test"

    # When
    # result = standalone_function(input_data)

    # Then
    # assert result == "expected"
    pytest.skip("TODO: 구현 필요")


# === 비동기 테스트 (pytest-asyncio 필요) ===


@pytest.mark.asyncio
async def test_async_function():
    """비동기 함수 테스트"""
    # Given
    input_data = "test"

    # When
    # result = await async_function(input_data)

    # Then
    # assert result == "expected"
    pytest.skip("TODO: 구현 필요")
