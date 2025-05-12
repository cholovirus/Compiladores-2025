def runTestStep(self, label, func):
        try:
            func()
            print(f"✅ [PASSED] {label}")
        except AssertionError as e:
            print(f"❌ [FAILED] {label} -> {str(e)}")
            raise