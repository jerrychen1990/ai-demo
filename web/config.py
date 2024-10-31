import json
import os

AI_DEMO_COMPARE_ENV = os.environ.get("AI_DEMO_COMPARE_ENV", "default")

AI_DEMO_COMPARE_CONFIG = json.load(open(f"config/compare/{AI_DEMO_COMPARE_ENV}.json"))
