#!/usr/bin/env python3
"""
测试配置文件调用的示例文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from settings.config import LLMConfig



if __name__ == "__main__":
    print(LLMConfig())