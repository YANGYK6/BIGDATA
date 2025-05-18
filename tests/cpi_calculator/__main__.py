# 导入可能需要用的包
from src.cpi_generator.__main__ import main
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
import pandas as pd

@pytest.fixture
def mock_settings():
    """
    测试场景：模拟 settings 模块
    预期结果：返回模拟的 settings 模块
    """
    with patch('src.cpi_generator.__main__.settings') as mock_settings:
        yield mock_settings

@pytest.fixture
def mock_calculator():
    """
    测试场景：模拟 CPICalculator 类
    预期结果：返回模拟的 CPICalculator 实例
    """
    with patch('src.cpi_generator.__main__.CPICalculator') as mock_calculator:
        yield mock_calculator

@pytest.fixture
def mock_visualize():
    """
    测试场景：模拟 visualize 函数
    预期结果：返回模拟的 visualize 函数
    """
    with patch('src.cpi_generator.__main__.visualize') as mock_visualize:
        yield mock_visualize

def test_main_normal(mock_settings, mock_calculator, mock_visualize):
    """
    测试场景：正常执行 main 函数
    预期结果：正确调用相关函数并打印结果
    """
    mock_calculator_instance = MagicMock()
    mock_calculator.return_value = mock_calculator_instance
    mock_calculator_instance.compute_daily_cpi.return_value = {'data': 'mock_data'}

    main()

    mock_settings.from_env.assert_called_once_with('prod')
    mock_calculator.assert_called_once_with(db_config=mock_settings.CLICKHOUSE)
    mock_calculator_instance.compute_daily_cpi.assert_called_once_with(date(2025, 5, 17), date(2028, 5, 15))
    mock_visualize.assert_called_once_with(pd.DataFrame({'data': 'mock_data'}))

def test_main_exception(mock_settings, mock_calculator, mock_visualize):
    """
    测试场景：main 函数执行时发生异常
    预期结果：捕获异常并处理
    """
    mock_calculator_instance = MagicMock()
    mock_calculator.return_value = mock_calculator_instance
    mock_calculator_instance.compute_daily_cpi.side_effect = Exception('Mock Error')

    with pytest.raises(Exception):
        main()

    mock_settings.from_env.assert_called_once_with('prod')
    mock_calculator.assert_called_once_with(db_config=mock_settings.CLICKHOUSE)
    mock_calculator_instance.compute_daily_cpi.assert_called_once_with(date(2025, 5, 17), date(2028, 5, 15))
    mock_visualize.assert_not_called()

if __name__ == '__main__':
    pytest.main()
