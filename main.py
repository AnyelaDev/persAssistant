#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.app import PersonalAssistantApp

if __name__ == '__main__':
    PersonalAssistantApp().run()